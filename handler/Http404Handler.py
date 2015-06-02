#!/bin/env python
#coding=utf-8
#ganji web db management
#by dongzerun 20140723
#version 0.1.0

import os
import tornado.ioloop
import tornado.web

class Http404Handler(tornado.web.ErrorHandler):
    def initialize(self):
        tornado.web.ErrorHandler.initialize(self, 404)
    def prepare(self):
        self.render("404.html")
