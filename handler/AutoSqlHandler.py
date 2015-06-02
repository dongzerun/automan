#!/bin/env python
#coding=utf-8
#ganji web db management
#by dongzerun 20140723
#version 0.1.0

import time
import os
import sys
import tornado.ioloop
import tornado.web
import tornado.gen
import MySQLHandler
import BaseHandler
import string
import datetime
import json
import tcelery
import urllib
import urllib2
from  asynctasks.tasks import savefile
from  asynctasks.tasks import submittask
from  asynctasks.sqlconfig import cities
from utils.taskid import get_taskid


class AutoSqlHandler(BaseHandler.BaseHandler):
    dbhandler = MySQLHandler.MySQLHandler()
    myclasses = []
    fileurl   = "/data/mysql/sqldata/" 

    def get(self):
        self.checkCookie()
        #task_id = get_taskid()
        #self.set_cookie('task_id', str(task_id))
        self.myclasses = self.dbhandler.query_classbyuser(self.curuser['enname'])
        if not self.myclasses:
            self.myclasses = []

        url_request = string.split(self.request.uri, "/")
        if len(url_request) == 3:
            if url_request[2] == 'autodml':
                task_id = get_taskid()
                getalltasks_sql = "select task_id, classname, left(description,30) as description, task_status, feedback, sqlsave, sqlparser, ruleparser, sim, sqlbak, online, applicant, if((expect_time - unix_timestamp()) < 0, '00:00:00', (TIMEDIFF(from_unixtime(expect_time), now())) )  as expecttime,done_time from autosql_ddl_tasks where done_time > DATE_SUB(CURDATE(),INTERVAL 7 DAY) and task_status in (0,1,4,7) order by done_time desc, task_status desc;"
                alltasks = self.dbhandler.find(getalltasks_sql)
                ifall = 1
                self.render("autosql_autodml.html", user=self.curuser, class_avl=self.myclasses, task_id=task_id, alltasks = alltasks, ifall=ifall)
            elif url_request[2] == 'autodmlgetbyuser': 
                task_id = get_taskid()
                getalltasks_sql = "select task_id, classname, left(description,30) as description, task_status, feedback, sqlsave, sqlparser, ruleparser, sim, sqlbak, online, applicant, if((expect_time - unix_timestamp()) < 0, '00:00:00', (TIMEDIFF(from_unixtime(expect_time), now())) )  as expecttime,done_time from autosql_ddl_tasks where task_status in (0,1,4,7) and applicant = '%s' order by done_time desc, task_status desc;" % self.curuser['enname']
                alltasks = self.dbhandler.find(getalltasks_sql)
                ifall = 0
                self.render("autosql_autodml.html", user=self.curuser, class_avl=self.myclasses, task_id=task_id, alltasks = alltasks,ifall=ifall)
            elif url_request[2].startswith('gencitysql'):
                self.render("autosql_gencitysql.html", user=self.curuser)
            else:
                self.render("autosql.html", user=self.curuser, class_avl=self.myclasses)
        else:
            self.render("autosql.html", user=self.curuser, class_avl=self.myclasses)

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def post(self):
        self.checkCookie()
        url_request = string.split(self.request.uri, '/')
        print url_request
        if len(url_request) == 4:
            if url_request[3] == 'uploadfile':
                task_id = self.get_argument('task_id');
                self.savefile(task_id)
            elif url_request[3] == 'dmlsubmit':
                dmlclass = self.get_argument('dmlclass').split('-')[0]
                dmltime = self.get_argument('dmltime')
                dmlcom = self.get_argument('dmlcom')
                dmlcityyes = int(self.get_argument('dmlcityyes'))
                dmlcityno = int(self.get_argument('dmlcityno'))
                ignoreyes = int(self.get_argument('ignoreyes'))
                ignoreno = int(self.get_argument('ignoreno'))
                dmlupfiles = self.get_argument('dmlupfile')
                dmlsql = self.get_argument('dmlsql').encode('utf-8')
                task_id = self.get_argument('task_id')
                username = self.get_argument('username')
                print "ignore yes: no", ignoreyes, ignoreno
                print type(dmlcom)
                print type(dmlsql)
                print self.curuser['enname']
                print "expect time is:", dmltime, type(dmltime)
                print "expect time is:", str(dmltime), type(str(dmltime))

                today = datetime.datetime.now().strftime("%Y-%m-%d ")
                expect_time = int(time.mktime(time.strptime(today + str(dmltime),'%Y-%m-%d %H:%M')))

                current_time = int(time.time())
                print expect_time,  current_time, expect_time - current_time

                if expect_time - current_time > 60:
                    delay = True
                    sql = "replace into autosql_ddl_tasks (task_id,classname,applicant,description,task_status,expect_time, delay) values ('%s','%s','%s','%s','%s','%s','%s');" % (task_id, dmlclass, self.curuser['enname'], dmlcom, 0, expect_time,1)
                else:
                    delay = False
                    sql = "replace into autosql_ddl_tasks (task_id,classname,applicant,description,task_status,expect_time, delay) values ('%s','%s','%s','%s','%s','%s', '%s');" % (task_id, dmlclass, self.curuser['enname'], dmlcom, 0, current_time,0)
                self.dbhandler.execute(sql)


                if dmlsql != 'NULL':
                    print "dmlsql is:", dmlsql, type(dmlsql)
                    self.writefile(task_id , dmlsql, task_id)
                print "dmlclass is :", dmlclass
                print "ignore yes: no", ignoreyes, ignoreno
                if ignoreyes == 1 and ignoreno == 0:
                        result = yield tornado.gen.Task(submittask.apply_async, args=[task_id,dmlclass,False,['sim']])
                else:
                        result = yield tornado.gen.Task(submittask.apply_async, args=[task_id,dmlclass,False])
                print "result is:", result    
                self.finish()
            elif url_request[3] == 'deltask':
                print url_request
                delid = int(self.get_argument('task_id'))
                deluser = self.get_argument('deluser')
                self.deltask(delid, deluser)
            elif url_request[3] == 'taskdesc':
                print url_request
                task_id = int(self.get_argument('task_id'))
                sql = "select distinct file_url from dba_stats.autosql_tasks_files where task_id='%s'" % task_id
                suffix = "_bamXsp_" + str(task_id) + "_bamXsp_" + str(task_id)
                taskdesc = ""
                print "suffix is:", suffix
                res = self.dbhandler.find(sql)
                for col in res:
                    print col
                    if not col['file_url'].endswith(suffix):
                        taskdesc = col['file_url'] + '\n' + taskdesc
                    else:
                        if os.path.exists(col['file_url']):
                            with open(col['file_url'], 'r') as f:
                                lines = f.readlines()
                                for line in lines:
                                    taskdesc = taskdesc + line
                self.write(taskdesc)
            elif url_request[3] == 'taskrejected':
                print url_request
                task_id = int(self.get_argument('task_id'))
                sql = "select file_url from dba_stats.autosql_tasks_files where task_id='%s' limit 1" % task_id
                res = self.dbhandler.find(sql)
                if len(res) == 1:
                    if 'file_url' in res[0]:
                        file_url = res[0]['file_url']
                        basedir = ('/').join(file_url.split('/')[0:-1])
                        applicant = file_url.split('/')[-1].split('_')[0]
                        wrong_file = basedir + applicant + '_bamXsp_' + str(task_id) + '_bamXsp_wrong.txt'
                        if os.path.exists(wrong_file):
                            taskrejected = ''
                            with open(wrong_file, 'r') as f:
                                lines = f.readlines()
                                for line in lines:
                                    taskrejected = taskrejected + line
                            if taskrejected == '':
                                taskrejected = "nothing found"
                            self.write(taskrejected)
                    else:
                        self.write("nothing found")
                else:
                    self.write("nothing found")
        elif len(url_request) == 3:
            if url_request[2] == 'gensql':
                oldsql = self.get_argument('oldsql')
                oldsqls = oldsql.split(';')
                newsqls = []
                for sql in oldsqls[0:-1]:
                    for city in cities:
                        newsql = sql.strip().replace('_CITIES_', city)
                        newsqls.append(newsql)
                newsqls.append('')
                self.write((';\r\n').join(newsqls))
            elif url_request[2] == 'gensqlunion':
                oldsql = self.get_argument('oldsql')
                oldsqls = oldsql.split(';')
                newsqls = []
                for sql in oldsqls[0:-1]:
                    tmpsqls = []
                    for city in cities:
                        newsql = sql.strip().replace('_CITIES_', city)
                        tmpsqls.append(newsql)
                    newsqls.append((' union all ').join(tmpsqls))
                newsqls.append('')
                self.write((';\r\n').join(newsqls))

    def deltask(self, delid, deluser):
        print "starting delete delay task:", delid, deluser,self.curuser['enname']
        if self.curuser['enname'] not in self._admin and self.curuser['enname'] != deluser:
            print "deluser is,", deluser, self._admin
            return False
        sql = "delete from dba_stats.autosql_tasks_files where task_id='%s'" % delid
        print sql
        self.dbhandler.execute(sql)
        sql = "delete from dba_stats.autosql_ddl_tasks where task_id='%s'" % delid
        print sql
        self.dbhandler.execute(sql)



    def savefile(self, task_id):
        file_metas = self.request.files['file']
        for meta in file_metas:
            filename = meta['filename']
            result = self.writefile(filename, meta['body'], task_id)
            print result
            if result:
                self.write({'status':'ok'})
                self.finish()
            else: 
                self.write({'status':'false'})
                self.finish()

    def writefile(self, filename, data, task_id=None):
        #curtime = datetime.datetime.now().strftime(u"%Y%m%d%H%M")
        if 'enname' in self.curuser:
            f = self.curuser['enname'].encode('utf-8') + '_bamXsp_' + task_id + '_bamXsp_' + filename
        else:
            f = task_id + '_bamXsp_' + filename
        destdir = self.fileurl + '/' + datetime.datetime.now().strftime(u"%Y%m%d") + '/'
        if not os.path.exists(destdir):
            os.mkdir(destdir)
        if filename:
            filepath = destdir + '/' + f
            with open(filepath, 'wb') as up:
                up.write(data)
                up.seek(0)
                up.close()
            self.dbhandler.taskfile_todb(task_id, filepath)
            return filepath
        else:
            return None 

 #   @tornado.web.asynchronous
 #   @tornado.gen.coroutine
 #   def post(self):
 #       self.checkCookie()
 #       file_metas = self.request.files['file']
 #       for meta in file_metas:
 #           filename = meta['filename']
 #           curtime = datetime.datetime.now().strftime(u"%Y%m%d_%H%M")
 #           if 'enname' in self.curuser:
 #               filename = self.curuser['enname'] + '_' + curtime + '_' + filename
 #           else:
 #               filename = curtime + '_' + filename
 #           print filename
 #           result = yield tornado.gen.Task(savefile.apply_async, args=[filename, meta['body']])
 #           print result.result
 #           if result.result:
 #               self.write({'status':'ok'})
 #           else: 
 #               self.write({'status':'false'})
 #
