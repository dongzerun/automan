#!/bin/env python
#coding=utf-8
#ganji web db management
#by dongzerun 20140723
#version 0.1.0

import os
import tornado.ioloop
import tornado.web
import urllib
import urllib2
import string
import json
from  asynctasks.sqlconfig import _admin

class BaseHandler(tornado.web.RequestHandler):
    _sso_getIdentity    = "http://sso.corp.ganji.com/Account/GetIdentity"
    _sso_login  = "http://sso.corp.ganji.com/Account/LogOn"
    _sso_logout = "http://sso.corp.ganji.com/Account/LogOff"
    #_self_host = "http://10.1.6.157"
    _self_host = "http://automan.corp.ganji.com"
    _subid  = 37
    _ssokey = "E5F85CCC-A422-405D-8D44-6EB8F03EF4F3"
    _pdata  = ""
    _token  = ""
#    _admin  = ("lujiajun", "lirui2", "ligangxing", "luojian", "caifeng", "lvwei", "wanglei", "wangjun", "yangyu","jipengcheng","dongzerun","cuihua","mangweiqi","chenyifan","liujun2","shanzebing","zhaoshenju")
    _purl   = ("autosql", "cdc")
    curuser = {}
    checked = False
    def checkCookie(self):
        """验证逻辑: 通过SSO认证, 确定为技术部员工,写cookie"""
        """admin权限能查看所有, 其它一律只能看静态数据和sql上线""" 
        #self.checked = True
        #self.curuser['fullname']='super'
        #self.curuser['enname'] = 'super'
        #return True
        returnUrl = self._self_host + self.request.uri
        print returnUrl
        """先设置checked = False 防止异步时未认证提交post"""
        self.checked = False

        if self.get_cookie('GDNETSSOC'):
            self._token = urllib.quote(self.get_cookie('GDNETSSOC').replace('userm=', '').replace(' ', '+'))
            self._pdata = "key=%s&userId=%s" % (self._ssokey, self._token)
            ok, data = self.checkIdentity(self._sso_getIdentity, self._pdata)
            print ok, data
            if not ok:
                self.checked = False
                print "False begain to login"
                self.login(returnUrl)
            else:
                print data
                if data['IsAuthenticated']:
                    self.curuser['email'] = data['Email']
                    self.curuser['fullname'] = data['FullName']
                    self.curuser['enname'] = data['Email'].replace('@ganji.com','')
                    """如果是admin, 或是sql上线,或是请求根地址,都允许通过"""
                    if self.curuser['enname'] in _admin or  self.request.uri.startswith('/autosql') or self.request.uri == "/" or self.request.uri.startswith('/offpriv') or self.request.uri.startswith('/pribid') or self.request.uri.startswith('/view'):
                        self.checked = True
                    else:
                        self.checked = False
                        self.redirect(self._self_host + "/pribid")
                else:
                    self.checked = False
                    self.login(returnUrl)
        else:
            self.checked = False
            self.login(returnUrl)
    def checkIdentity(self, url, data):
        try:
            req = urllib2.Request(url, data)
            res = urllib2.urlopen(req)
            result = res.read()
            return True, json.loads(result)
        except Exception, e:
            print e
            return False, None

    def login(self, returnUrl=None):
        if returnUrl:
            self.redirect('%s?id=%d&returnUrl=%s' % (self._sso_login, self._subid, returnUrl))
        else:
            self.redirect('%s?id=%d' % (self._sso_login, self._subid))

    def logout(self, returnUrl=None): 
        if returnUrl:
            self.redirect('%s?id=%d&returnUrl=%s' % (_sso_logout, self._subid, returnUrl))
        else:
            self.redirect('%s?id=%d' % (_sso_logout, self._subid))
