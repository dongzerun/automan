#!/bin/env python
#coding=utf-8
#ganji web db management
#by dongzerun 20140723
#version 0.1.0
#目前线下库授权没有做成异步,对性能影响较大
#可以考滤将所有耗时操作移植到celery中
#最后做异步调度更好一些


import os
import tornado.ioloop
import tornado.web
import BaseHandler
import string
import MySQLdb
import utils.SendMsg
from MySQLHandler import MySQLHandler
from asynctasks.sqlconfig import leaders,envhost,dbuser,dbpwd
from asynctasks.sqlconfig import dbas, envtype, envbynum

class OffPrivHandler(BaseHandler.BaseHandler):
    dbhandler = MySQLHandler()

    def get(self):
        self.checkCookie()
        url_request = string.split(self.request.uri, "/")

        if len(url_request) == 3:
            if url_request[2].startswith('getoffbyuser'):
                sql = "select * from dba_stats.users where name='%s'" % self.curuser['enname']
                myoffs = self.dbhandler.find(sql)
                self.render("myoffs.html",user=self.curuser,myoffs=myoffs)
            elif url_request[2].startswith('getappbyuser'):
                allapp = 0
                allleader = 1
                sql = "select id,class,class_zh,has_real,has_qa,has_sim from class_port order by class;"
                classes = self.dbhandler.find(sql)
                sql = "select * from dba_stats.offpriv where applicant ='%s' order by create_at desc;" %  self.curuser['enname']
                print sql
                appls = self.dbhandler.find(sql)
                self.render("offpriv.html", user=self.curuser, classes=classes,leaders=leaders,appls=appls, allapp=allapp, allleader=allleader)

            elif url_request[2].startswith('getleaderbyuser'):
                allapp = 1
                allleader = 0
                sql = "select id,class,class_zh,has_real,has_qa,has_sim from class_port order by class;"
                classes = self.dbhandler.find(sql)
                sql = "select * from dba_stats.offpriv where leader ='%s' order by create_at desc;" %  self.curuser['enname']
                print sql
                appls = self.dbhandler.find(sql)
                self.render("offpriv.html", user=self.curuser, classes=classes,leaders=leaders,appls=appls, allapp=allapp, allleader=allleader)
        else:
            allapp = 1
            allleader = 1
            sql = "select id,class,class_zh,has_real,has_qa,has_sim from class_port order by class;"
            classes = self.dbhandler.find(sql)
            sql = "select * from dba_stats.offpriv  order by create_at desc;"
            print sql
            appls = self.dbhandler.find(sql)
            self.render("offpriv.html", user=self.curuser, classes=classes,leaders=leaders,appls=appls, allapp=allapp, allleader=allleader)

    def post(self):
        self.checkCookie()
        url_request = string.split(self.request.uri, "/")
        if len(url_request) == 3:
            if url_request[2] == 'offrequest':
                self.off_request_sub()
            if url_request[2] == 'offmysqlapp':
                self.off_mysql_app();

    def off_mysql_app(self):
        offid = int(self.get_argument('offid'))
        status = int(self.get_argument('offstatus'))
        fb = self.get_argument('fb')
        print "offid status fb:", offid, status, fb
        if offid and status:
            if status > 4 and self.curuser['enname'] in dbas:
                print "start grant off prive:", offid
                ok, res =  self.grant_off_priv(offid)
                print "grant_off_priv:", ok , res
                if ok:
                    sql = "update dba_stats.offpriv set status='%s', feedback='%s' where id='%s'" % (status,fb,offid)
                    print sql
                    self.dbhandler.execute(sql)
                else:
                    print "type of res is :", type(res)
                    self.write(res[1])
                    self.finish()
            elif status <=4 and self.curuser['enname'] in leaders:
                sql = "select * from dba_stats.offpriv where id='%s' limit 1"  % offid
                offinfo = self.dbhandler.find(sql)
                print offinfo
                if offinfo:
                    if offinfo[0]['leader'] == self.curuser['enname']:
                        sql = "update dba_stats.offpriv set status='%s', feedback='%s' where id='%s'" % (status,fb,offid)
                        print sql
                        self.dbhandler.execute(sql)
                        utils.SendMsg.sendmailtoleader('dba.mon')

    def off_request_sub(self):
        leader = self.get_argument('leader')
        qa = self.get_argument('qa')
        real = self.get_argument('real')
        sim = self.get_argument('sim')
        com = self.get_argument('comment')
        applicant  = self.curuser['enname']
        print self.curuser
        sql = ("insert into dba_stats.offpriv set applicant='%s', leader='%s',allqa='%s',allsim='%s',"
               "allreal='%s',comment='%s'") % (applicant,leader,qa,sim,real,com)
        if leader in leaders  and applicant and (qa or real or sim):
            self.dbhandler.execute(sql)
            print "send mail to ", leader 
            utils.SendMsg.sendmailtoleader(leader)

    def grant_off_priv(self, offid):
        sql = "select * from dba_stats.offpriv where id='%s' and status= 4 limit 1"  % offid
        print sql, "to be executed"
        offinfo = self.dbhandler.find(sql)
        print offinfo

        sql = "select class, port from class_port;"
        classbyport = self.dbhandler.find(sql)

        if not offinfo:
            return False
        sql = "select * from users where name = '%s'" % offinfo[0]['applicant']
        print "all off by user sql:", sql
        offsbyuser = self.dbhandler.find(sql)

        try:
            if offinfo[0]['allqa']:
                self.grantbyenv(offinfo[0]['applicant'], envtype['qa'], offinfo[0]['allqa'], offsbyuser,classbyport)
            if offinfo[0]['allsim']:
                self.grantbyenv(offinfo[0]['applicant'], envtype['sim'], offinfo[0]['allsim'], offsbyuser,classbyport)
            if offinfo[0]['allreal']:
                self.grantbyenv(offinfo[0]['applicant'], envtype['real'], offinfo[0]['allreal'], offsbyuser,classbyport)
            utils.SendMsg.sendmailbyuser(offinfo[0]['applicant'])
            return True,None
        except Exception, e:
            print e
            return False, e
            #return False, str(e)

    def grantbyenv(self, name, type, appclasses, myclasses,classbyport):
        offpwd = None
        newclasses = appclasses.split(',')
        for newclass in newclasses:
            if not newclass:
                continue
            classname = newclass.split('(')[0]
            for off in myclasses:
                offpwd = off['passwd']
                if off['env_type'] == type and off['class'] == classname:
                    break
            if not offpwd:
                offpwd = ''.join(map(lambda xx:(hex(ord(xx))[2:]),os.urandom(4)))
            print offpwd
            if classname == "bin":
                host = envhost['bin']
            else:
                host = envhost[envbynum[type]]
            for i in classbyport:
                if i['class'] == classname:
                    port = i['port']
                    break

            dbh = MySQLHandler(host,port,dbuser,dbpwd)
            print host,port,dbuser,dbpwd
            if envbynum[type] == 'real':
                sql192 = "grant select on *.* to '%s'@'192.168.%%.%%' identified by '%s'" % (name, offpwd)
                sql10 = "grant select on *.* to '%s'@'10.%%.%%.%%' identified by '%s'" % (name, offpwd)
            else:
                sql192 = "grant SELECT, INSERT, UPDATE, DELETE on *.* to '%s'@'192.168.%%.%%' identified by '%s'" % (name, offpwd)
                sql10 = "grant SELECT, INSERT, UPDATE, DELETE on *.* to '%s'@'10.%%.%%.%%' identified by '%s'" % (name, offpwd)

            print sql192,sql10
            try:
                print sql192
                dbh.execute(sql192)
                print sql10
                dbh.execute(sql10)
            except MySQLdb.Error, e:
                print e
                #raise MySQLdb.Error(newclass+'\n'+host+':'+str(port)+'\n'+str(e[0]) + ' ' +e[1])
                raise MySQLdb.Error(e[0], newclass+' ' +host+':'+str(port)+' '+ ' ' +e[1])
            sql = "insert into dba_stats.users set name='%s',class='%s',passwd='%s',hostname='%s',port='%s',env_type='%s'" % (name, classname, offpwd,host,port,type)
            self.dbhandler.execute(sql)


