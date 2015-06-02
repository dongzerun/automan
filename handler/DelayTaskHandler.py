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
import celery
from  asynctasks.tasks import savefile
from  asynctasks.tasks import submittask
from  asynctasks.tasks import delaytask
from utils.taskid import get_taskid

#tcelery.setup_nonblocking_producer()

"""只提供http异步服务"""
class DelayTaskHandler(BaseHandler.BaseHandler):
    dbhandler = MySQLHandler.MySQLHandler()


    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def post(self):
        url_request = string.split(self.request.uri, '/')
        print url_request
        task_id = int(self.get_argument('task_id'))
        dmlclass = self.get_argument('dmlclass')
        sql = "select  if((expect_time - unix_timestamp()) < 0, 0, (expect_time - unix_timestamp()))  as expecttime from dba_stats.autosql_ddl_tasks where task_status not in (1) and task_id='%s' limit 1;" % task_id
        print sql
        try:
            res = self.dbhandler.find(sql)
        except MySQLdb.Error,e:
            self.write("{'enqueue':False,'errcode':'mysql error during enqueue'}")
            self.finish()
        if not res:
            self.write("{'enqueue':False,'errcode':'this task do not need delay execute'}")
            self.finish() 
        else:
            print "res is:"
            delaytime = 0 if not res[0]['expecttime'] else res[0]['expecttime']
            ignoresteps = ['sqlsave','sqlparser','ruleparser','sim','sqlbak']
            args = [task_id, dmlclass, False,ignoresteps]
            result = delaytask.apply_async(args=args,countdown=delaytime)
            print result,type(result)
            sql = "update dba_stats.autosql_ddl_tasks set celeryid = '%s' where task_id = '%s';" % (result, task_id)
            print sql
            try:
                self.dbhandler.execute(sql)
            except MySQLdb.Error,e:
                self.write("{'enqueue':False,'errcode':'celery id updated failed!!! please contact DBA'}")
                self.finish()
            print "after yield"
            if isinstance(result, celery.result.AsyncResult):
                self.write("{'enqueue':True, 'errcode':''}")
            else:
                self.write("{'enqueue':False,'errcode':'enqueue failed!!! please contact DBA'}")
            self.finish()
