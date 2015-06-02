#!/bin/env python
#coding=utf-8
#ganji web db management
#by dongzerun 20140723
#version 0.1.0

import os
import tornado.ioloop
import tornado.web
import tornado.gen
import MySQLHandler
import BaseHandler
import string
import datetime


class BackupHandler(BaseHandler.BaseHandler):
    dbhandler = MySQLHandler.MySQLHandler()

    def get(self):
        self.checkCookie()
        url_request = string.split(self.request.uri, "/")
        print url_request
        print "this is default !!!!"
        sql = "select c.*,b.last_bak_date from dba_stats.class_port c left join (select db_name, max(date) last_bak_date from dba_stats.backup_info group by db_name)b on c.class=b.db_name order by c.has_bak;"
        backups = self.dbhandler.find(sql)
        self.render("backup.html", user=self.curuser, backups=backups)

    def post(self):
        self.checkCookie()
        url_request = string.split(self.request.uri, "/")
        if self.checked:
            print self.request.uri
            if len(url_request) == 3:
                if url_request[2] == 'delbackupclass':
                    self.backup_conf_del()
                elif url_request[2] == 'subbackupclass':
                    self.backup_conf_save()

    def backup_conf_del(self):
        print "in backup_conf_del"
        classname = self.get_argument('classname')
        sql = "delete from dba_stats.class_port where class='%s'" % classname
        self.dbhandler.execute(sql)

    def backup_conf_save(self):
        print "in backup_conf_save"
        classname = self.get_argument('classname')
        hasbak = self.get_argument('hasbak')
        bakhost = self.get_argument('bakhost')
        bakdir = self.get_argument('bakdir')
        bakdays = self.get_argument('bakdays')
        bakport = self.get_argument('bakport')
        print classname, hasbak, bakhost, bakdir, bakdays
        sql = "update dba_stats.class_port set has_bak='%s', bak_host='%s', bakdir='%s', retain_days='%s', port='%s'  where class='%s'" % (hasbak, bakhost, bakdir, bakdays, bakport, classname)
        self.dbhandler.execute(sql)
