#!/bin/env python
#coding=utf-8
#ganji web db management
#by dongzerun 20140723
#version 0.1.0

import os
import tornado.ioloop
from tornado.web import asynchronous
from tornado.gen import coroutine
import tornado.web
import tornado.gen
import BaseHandler
import time
from concurrent.futures import ThreadPoolExecutor  
from tornado.concurrent import run_on_executor


class ArchHandler(BaseHandler.BaseHandler):
        dbhandler = MySQLHandler.MySQLHandler()

    def get(self):
        self.checkCookie()
        url_request = string.split(self.request.uri, "/")
        print url_request
        print "this is default !!!!"
        #sql = "select c.*,b.last_bak_date from dba_stats.class_port c left join (select db_name, max(date) last_bak_date from dba_stats.backup_info group by db_name)b on c.class=b.db_name order by c.has_bak;"
        sql = "select c.*,b.last_bak_date from dba_stats.class_port c left join (select db_name, max(date) last_bak_date from dba_stats.backup_info group by db_name)b on c.class=b.db_name order by c.has_bak;"
        backups = self.dbhandler.find(sql)
        self.render("arch_bylarry.html", user=self.curuser, backups=backups)
