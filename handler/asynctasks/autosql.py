#!/bin/env python
#coding=utf-8
#by dongzerun 
#automan平台,SQL自动化上线处理模块
#主要功能:
#1.确认SQL上线的文件名
#2.解析SQL语法,并重写SQL
#3.根据规则将sql进行过滤
#4.符合规则进行sim预执行
#5.sim预执行成功后备份
#6.备份成功或无需备份后进行上线
from __future__ import absolute_import

import sys
import os
sys.path.append("/data/mysql/automan/handler")
import time
import MySQLdb
import pika
import string
import json
import torndb
import datetime
import urllib
import urllib2
import decimal
import tornado.ioloop
import tornado.web
import tornado.gen
#import asynctasks.tasks.submittask
from asynctasks.autorule import Rule, RuleError
from MySQLHandler import MySQLHandler
from asynctasks.parser import SQLParser
from asynctasks.parser import SQLError
import asynctasks.sqlconfig as sqlconfig

class AutoSql(object):
    name = "automan autosql"
    dbhandler = None
    p = SQLParser(debug=False)
    files = None
    port = None
    classes = None
    backupsql = None
    backupfile = None
    backupsql_f = None
    backupfile_f = None
    wrongfile = None
    wrongfile_f = None
    ruleerror = False
    delay = False
    needdelay = 0
    sim = False
    ignoresteps = []

    def __init__(self, task_id, classes=None, delay=False, ignoresteps=[]):
        self.task_id = task_id
        self.dbhandler = MySQLHandler()
        self.files = self.getfiles()
        self.sleeptime = sqlconfig.exespeed
       
        if delay:
            self.delay = delay
        if ignoresteps:
            self.ignoresteps = ignoresteps

        if classes:
            self.classes = classes
        if len(self.files) > 0:
            self.backupsql = '_bamXsp_'.join(self.files[0].split('_bamXsp_')[:-1]) + '_bamXsp_' + 'backup.sql'
            self.backupfile = '_bamXsp_'.join(self.files[0].split('_bamXsp_')[:-1]) + '_bamXsp_' + 'backup.txt'
            self.wrongfile = '_bamXsp_'.join(self.files[0].split('_bamXsp_')[:-1]) + '_bamXsp_' + 'wrong.txt'
            self.backupsql_f = open(self.backupsql, 'wb+')
            self.backupfile_f = open(self.backupfile, 'wb+')
            self.wrongfile_f = open(self.wrongfile, 'wb+')

        

    def getfiles(self):
        files = []
        sql = "select file_url from autosql_tasks_files where task_status = 0 and task_id = %s;" % self.task_id
        res = self.dbhandler.find(sql)
        if not res:
            return files
        for i in res:
            files.append(i['file_url'])
        return files

    def sendmq(self, type, success, message):
        connection = pika.BlockingConnection(pika.ConnectionParameters(
                                            host='localhost'))
        channel = connection.channel()
        channel.exchange_declare(exchange='automan_websocket',type='fanout')
        message = {'task_id': self.task_id, 'type':type, 'success':success,'data': message}
        channel.basic_publish(exchange='automan_websocket',
                              routing_key='for_websocket',
                              body=json.dumps(message))
    def senddb(self, type, success,message):
        if type == "delay":
            sql = "update dba_stats.autosql_ddl_tasks set %s = '%s' where task_id = '%s'" % ('online', success, self.task_id)
        else:
            sql = "update dba_stats.autosql_ddl_tasks set %s = '%s' where task_id = '%s'" % (type, success, self.task_id)
        self.dbhandler.execute(sql)

    def notify(self, type, success, message):
        """对于延迟调度,无需时时发送消息队列"""
        try:
            if not self.delay:
                self.sendmq(type, success, message)
            self.senddb(type,success,message)
            self.wrongfile_f.write(message)
            self.wrongfile_f.write("\n")
        except Exception,e:
            return

    def invalidtask(self):
        sql = "update dba_stats.autosql_tasks_files  set task_status =3 where task_id='%s';" % self.task_id
        self.dbhandler.execute(sql)
        sql = "update dba_stats.autosql_ddl_tasks  set task_status =7 where task_id='%s';" % self.task_id
        self.dbhandler.execute(sql)

    def closetask(self):
        if not self.delay and self.needdelay == 1:
            self.delaytask()
        else:
            sql = "update dba_stats.autosql_tasks_files  set task_status =1 where task_id='%s';" % self.task_id
            self.dbhandler.execute(sql)
            sql = "update dba_stats.autosql_ddl_tasks  set task_status =1 where task_id='%s';" % self.task_id
            self.dbhandler.execute(sql)
        sql = "update dba_stats.autosql_ddl_tasks  set delay = 0 where task_id='%s';" % self.task_id
        self.dbhandler.execute(sql)

    def delaytask(self):
        sql = "update dba_stats.autosql_ddl_tasks  set task_status =4 where task_id='%s';" % self.task_id
        self.dbhandler.execute(sql)
        

    def run(self):
        if not self.sqlsave():
            self.invalidtask()
            return "in sqlsave 0"
        if not self.sqlparser():
            self.invalidtask()
            return "in sqlparser 0"
        if not self.ruleparser():
            self.invalidtask()
            return "in ruleparser 0"
        if not self.sim():
            self.invalidtask()
            return "in sim 0"
        if not self.sqlbak():
            self.invalidtask()
            return "in sqlbak 0"
        if not self.online():
            self.invalidtask()
        else:
            self.closetask()
            return "all done"

    def sqlsave(self):
        """第一步sqlsave 检查入队文件为空则抛出错误"""
        for i in self.ignoresteps:
            if i == 'sqlsave':
                message =  "TaskID: " + str(self.task_id) + " WARN 忽略sqlsave检查"
                self.notify('sqlsave', 1, message)
                return True

        if not self.files:
            message =  "TaskID: " + str(self.task_id) + " 该任务不存在sql文件,请检查或联系DBA"
            self.notify('sqlsave', 0, message)
            return False
        for f in self.files:
            if not os.path.exists(f):    
                message =  "TaskID: " + str(self.task_id) + " " + f.split('_bamXsp_')[-1] + " 不存在sql文件,请检查或联系DBA"
                self.notify('sqlsave', 0, message)
                return False
        message =  "TaskID: " + str(self.task_id) + " autosql files list: " +  '\n' + '\n'.join(self.files)
        self.notify('sqlsave', 1, message)
        return True

    def sqlparser(self):
        """第二步sqlparser 使用sqlparser检查文件语法"""
        for i in self.ignoresteps:
            if i == 'sqlparser':
                message =  "TaskID: " + str(self.task_id) + " WARN 忽略sqlparser解析"
                self.notify('sqlparser', 1, message)
                return True

        for f in self.files:
            try:
                self.p.parse(open(f).read(), filename=f)
            except SQLError,e :
                #print e.location['file']
                #e.location['file'] = e.location['file'].split('_bamXsp_')[-1]
                print "error e is:", e.__str__().encode('utf8')
                b = e.__str__().encode('utf8')
                print "type of b:", type(b)
                message =  "TaskID: " + str(self.task_id) + " " + f.split('_bamXsp_')[-1] + unicode(e.__str__().encode('utf8'),'utf8')
                self.notify('sqlparser', 0, message)
                return False
        message =  "TaskID: " + str(self.task_id) + " 语法解析完成"
        self.notify('sqlparser', 1, message)
        return True

    def ruleparser(self):
        """第三步ruleparser 过滤相应规则并且生成备份sql"""
        for i in self.ignoresteps:
            if i == 'ruleparser':
                message =  "TaskID: " + str(self.task_id) + " WARN 忽略sql rule规则检查"
                self.notify('ruleparser', 1, message)
                return True

        for f in self.files:
            try:
                sqls = self.p.parse(open(f).read(), filename=f)
                for sql in sqls:
                    ok, ruleerror, backsql = Rule(self.task_id,sql,self.classes).run()
                    if ok and backsql:
                        self.backupsql_f.write(backsql+'\n')
                    elif not ok and ruleerror:
                        self.ruleerror = True
                        self.wrongfile_f.write(str(ruleerror)+'\n')
            except SQLError,e :
                #e.location['file'] = e.location['file'].split('_bamXsp_')[-1]
                message =  "TaskID: " + str(self.task_id) + " " + f.split('_bamXsp_')[-1] +  unicode(e.__str__().encode('utf8'),'utf8')
                self.notify('ruleparser', 0, message)
                return False
        self.wrongfile_f.seek(0)    
        self.backupsql_f.seek(0)
        """need close backupsql file ????"""
        self.backupsql_f.close()    
        if self.ruleerror:
            err = self.wrongfile_f.read()
            message =  "TaskID: " + str(self.task_id) +  '\n' + err
            self.notify('ruleparser', 0, message)
            return False
        message =  "TaskID: " + str(self.task_id) + " 过滤规则完成"
        self.notify('ruleparser', 1, message)
        return True

    def sim(self):
        for i in self.ignoresteps:
            if i == 'sim':
                message =  "TaskID: " + str(self.task_id) + " WARN sim 忽略预执行"
                self.notify('sim', 1, message)
                return True

        self.getport()
        sqls = ''
        if not self.port:
            message =  "TaskID: " + str(self.task_id) + " sim 没有相应产品线"
            self.notify('sim', 0, message)
            return False
        else:
            self.simhandler = MySQLHandler(sqlconfig.simhost,self.port,sqlconfig.dbuser,sqlconfig.dbpwd,'')
            for file in self.files:
                f = open(file, 'r')
                wholesql = ''
                while 1:
                    sql = f.readline()
                    if not sql:
                        break
                    tmpsql = str(sql).strip()
                    if str(sql).strip() == '':
                        continue
                    if str(sql).strip().endswith(';'):
                        wholesql = wholesql + sql
                        try:
                            self.simhandler.execute(str(wholesql))
                            wholesql = ''
                        except MySQLdb.Error,e:
                            wholesql = ''
                            print "in sim:", e[0]
                            if e[0] in sqlconfig.ignorecodes:
                                continue
                            message = "TaskID: " + str(self.task_id) + " sim预执行失败\n" + str(e)
                            self.notify('sim', 0, message)
                            return False
                    else:
                        wholesql = wholesql + sql
            message =  "TaskID: " + str(self.task_id) + " sim 预执行成功"
            self.notify('sim', 1, message)
            return True
    
    def sqlbak(self):
        for i in self.ignoresteps:
            if i == 'sqlbak':
                message =  "TaskID: " + str(self.task_id) + " WARN sqlbak 忽略备份"
                self.notify('sqlbak', 1, message)
                return True

        if os.stat(self.backupsql).st_size == 0:
            message =  "TaskID: " + str(self.task_id) + " 本次上线无需备份"
            self.notify('sqlbak', 1, message)
            return True
        if self.classes in sqlconfig.allclasses:
            hosts = sqlconfig.allclasses[self.classes]
            for host in hosts:
                self.onlinehandler = MySQLHandler(host[0],host[1],sqlconfig.dbuser,sqlconfig.dbpwd,'')
                f = open(self.backupsql, 'r')

                wholesql = ''
                while 1:
                    sql = f.readline()
                    if not sql:
                        break
                    tmpsql = str(sql).strip()
                    if str(sql).strip() == '':
                        continue

                    if str(sql).strip().endswith(';'):
                        wholesql = wholesql + sql
                        if str(wholesql).strip().lower().startswith('use'):
                            try:
                                self.onlinehandler.execute(str(wholesql))
                            except MySQLdb.Error, e:
                                for errcode in sqlconfig.ignorecodes:
                                    if e[0] == errcode:
                                        continue
                                message = "TaskID: " + str(self.task_id) + " 执行备份失败\n" + str(e)
                                self.notify('sqlbak', 0, message)
                                return False
                            wholesql = ''
                        else:
                            try:
                                backupres =  self.onlinehandler.find(str(wholesql))
                            except MySQLdb.Error, e:
                                for errcode in sqlconfig.ignorecodes:
                                    if e[0] == errcode:
                                        continue
                                message = "TaskID: " + str(self.task_id) + " 执行备份失败\n" + str(e)
                                self.notify('sqlbak', 0, message)
                                return False
                            wholesql = ''
                            if backupres:
                                for backsql in backupres:
                                    backupline = ('\t').join([str(x) if isinstance(x, (datetime.date,int,long,datetime.datetime,float,decimal.Decimal)) else  '' if not x else x.encode('utf8') for x in backsql.values()])
                                    self.backupfile_f.write(backupline + '\n')
                    else:
                        wholesql = wholesql + sql
                break
            message =  "TaskID: " + str(self.task_id) + " sql备份成功"
            self.notify('sqlbak', 1, message)
            return True
        else:
            message =  "TaskID: " + str(self.task_id) + " 线上无或配置中没有该产品线"
            self.notify('sqlbak', 0, message)
            return False

    def delayself(self):
        taskhost = sqlconfig.gateway
        post_data = {'task_id':self.task_id,'dmlclass':self.classes}
        data = urllib.urlencode(post_data)
        print type(post_data), type(data), data
        try:
            fh = urllib2.urlopen(taskhost, data)
            res = fh.readline()
            result = eval(res)
            if 'enqueue' not in result:
                return False, "enqueue delay execute unknow error"
            elif not result['enqueue'] and 'errcode' in result:
                return False, result['errcode']
            elif result['enqueue']:
                return True, None
            else:
                return False, "enqueue error,you would not see this line!!!"
        except Exception,e:
            print e
            return False, "delayself " + str(e)

    def online(self):
        sql = "select delay from dba_stats.autosql_ddl_tasks where task_id='%s' and task_status not in (1) limit 1;" % self.task_id
        print "in online sql is:", sql
        print "in online task_id is:", self.delay, self.needdelay
        res = self.dbhandler.find(sql)
        if len(res) != 1:
            print "wouldn't happened at all!!!!"
        else:
            self.needdelay = res[0]['delay']
        if not self.delay and self.needdelay == 1:
            ok, message = self.delayself()
            if not ok:
                message =  "TaskID: " + str(self.task_id) + " online延迟调度失败 " + message
                self.notify('delay', 0, message)
                return False
            else:
                message =  "TaskID: " + str(self.task_id) + " online执行己加入队列,等待延迟调度"
                self.notify('delay', 1, message)
                return True


        if self.classes in sqlconfig.allclasses:
            hosts = sqlconfig.allclasses[self.classes]
            for host in hosts:
                self.onlinehandler = MySQLHandler(host[0],host[1],sqlconfig.dbuser,sqlconfig.dbpwd,'')
                for f in self.files:
                    f = open(f, 'r')

                    wholesql = ''
                    counts = 1
                    while 1:
                        sql = f.readline()
                        if not sql:
                            break
                        tmpsql = str(sql).strip()
                        if str(sql).strip() == '':
                            continue

                        if str(sql).strip().endswith(';'):
                            wholesql = wholesql + sql
                            counts = counts + 1
                            if counts % 100 == 0:
                                time.sleep(self.sleeptime)
                            try:
                                self.onlinehandler.execute(str(wholesql))
                                wholesql = ''
                            except MySQLdb.Error,e:
                                wholesql = ''
                                print "in sim:", e[0]
                                if e[0] in sqlconfig.ignorecodes:
                                    continue
                                message = "TaskID: " + str(self.task_id) + " 线上执行失败\n" + str(e)
                                self.notify('online', 0, message)
                                return False
                        else:
                            wholesql = wholesql + sql
            message =  "TaskID: " + str(self.task_id) + " online线上执行成功"
            self.notify('online', 1, message)
            return True
        else:
            message =  "TaskID: " + str(self.task_id) + " online执行失败,线上无此产品线"
            self.notify('online', 0, message)
            return False


    def getport(self):
        sql = "select port from %s where `class` = '%s';" % (sqlconfig.dbcfgtable, self.classes)
        port = self.dbhandler.find(sql)
        if not port:
            pass
        else:
            self.port = port[0]['port']
class RuleError(Exception):
  def __init__(self, file, message):
    self.message = message
    self.file = file

  def __str__(self):
    return "File: %s \n Error: %s" % (self.file , self.message)


if __name__ == "__main__":
    autosql = AutoSql(6230, 'ms')
    autosql.delayself()


