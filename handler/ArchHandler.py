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
    executor = ThreadPoolExecutor(10)
    @tornado.web.asynchronous  
    @tornado.gen.coroutine  
    def get(self):  
        result = yield self.sleep(10) #现在的sleep（）已经实现了异步，所以可以这样用，现在你知道为什么不是所有的yield xxx（）都能实现异步的原因了吧  
        self.write(result)
        self.finish()#使用了tornado.web.asynchronous装饰器时，必须显示关闭链接  
   
    @run_on_executor  
    def sleep(self, seconds):  
        time.sleep(seconds)  
        return "test async function: sleep %d s" % seconds
