#!/bin/env python
#coding=utf-8
#ganji web db management
#by dongzerun 20140723
#version 0.1.0
from __future__ import unicode_literals

import os
import sys
import tornado.ioloop
import tornado.web
import tornado.gen
import MySQLHandler
import string
import datetime
import json
import pika
import tornado.websocket
from utils import consumer

class WSHandler(tornado.websocket.WebSocketHandler):
    wsset_taskid = None
    taskid_wsset = None

    def __init__(self, application, request, **kwargs):
        tornado.websocket.WebSocketHandler.__init__(self, application, request,
                                            **kwargs)
        self.wsset_taskid = self.application.settings['wt']
        self.taskid_wsset = self.application.settings['tw']

    def check_origin(self, origin):
        return True

    def open(self):
        self.set_nodelay(True)
        print "on open myself is :", self
    def on_message(self,message):
        data = eval(message.decode('utf-8'))
        if 'type' in data:
            type = data['type']
            if type == 'register':
                self.taskid_wsset.update({data['data']:self})
                self.wsset_taskid.update({self:data['data']})

                task_id = data['data']
                welcome = "   欢迎使用automan自动化上线平台\n   分配任务ID: " + str(task_id)
                banner = {'type':'welcome', 'data':welcome}
                self.write_message(json.dumps(banner))
            elif type == 'next':
                print "receive next request"

    def on_close(self):
        if self in self.wsset_taskid:
            task_id = self.wsset_taskid[self]
            self.wsset_taskid.pop(self)
            self.taskid_wsset.pop(task_id)
