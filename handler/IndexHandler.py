#!/bin/env python
#coding=utf-8
#ganji web db management
#by dongzerun 20140723
#version 0.1.0

import os
import tornado.ioloop
import tornado.web
import BaseHandler

class IndexHandler(BaseHandler.BaseHandler):
    def get(self):
        self.checkCookie()
        self.render("index.html", user=self.curuser)
