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


class MonMySQLHandler(BaseHandler.BaseHandler):
    dbhandler = MySQLHandler.MySQLHandler()
    mysqlclassname = []
    idc = []
    idc = dbhandler.query_classidc()

    def get(self):
        self.checkCookie()
        url_request = string.split(self.request.uri, "/")
        self.mysqlclassname = self.dbhandler.query_classname()
        if len(url_request) == 5:
            if url_request[3] == 'findbyclass' and url_request[4]:
                self.mysqlhosts = self.dbhandler.query_byclass(url_request[4])
                self.render("monitor.html", mysqlclassname=self.mysqlclassname, idc=self.idc, hosts=self.mysqlhosts, user=self.curuser)
            elif url_request[3] == 'findbyidc' and url_request[4]:
                if url_request[4] == 'all':
                    self.mysqlhosts = self.dbhandler.query()
                    self.render("monitor.html", mysqlclassname=self.mysqlclassname, idc=self.idc, hosts=self.mysqlhosts, user=self.curuser)
                else:
                    self.mysqlhosts = self.dbhandler.query_byidc(url_request[4])
                    self.render("monitor.html", mysqlclassname=self.mysqlclassname, idc=self.idc, hosts=self.mysqlhosts,user=self.curuser)
            else:
                self.mysqlhosts = self.dbhandler.query()
                self.render("monitor.html", mysqlclassname=self.mysqlclassname, idc=self.idc, hosts=self.mysqlhosts,user=self.curuser)
        elif len(url_request) == 4 and url_request[3] == 'monconf':
            print url_request, len(url_request)
            print "this is function monconf!!!!"
            sql = "select * from dba_stats.monitor_class;"
            classes = self.dbhandler.find(sql)
            self.render("mysql_monconf.html", classes=classes, user=self.curuser)
        elif len(url_request) == 4 and url_request[3] == 'editclass':
            print url_request, len(url_request)
            print "this is function editclass!!!!"
            sql = "select * from dba_stats.class_port;"
            classes = self.dbhandler.find(sql)
            self.render("mysql_class.html", classes=classes, user=self.curuser)
        else:
            print "this is default !!!!"
            self.mysqlhosts = self.dbhandler.query()
            self.render("monitor.html", mysqlclassname=self.mysqlclassname, idc=self.idc, hosts=self.mysqlhosts,user=self.curuser)

    def post(self):
        self.checkCookie()
        if self.checked:
            cb = string.split(self.request.uri, "/")[3].lower()
            print "post url:", cb
            if cb == "add_mon_save":
                self.add_mon_save()
            elif cb == "time_mon_save":
                self.time_mon_save()
            elif cb == "del_mon_save":
                self.del_mon_save()
            elif cb == "edit_mon_save":
                self.edit_mon_save()
            elif cb == "delclassconf":
                self.class_conf_del()
            elif cb == "subclassconf":
                self.class_conf_update()
            elif cb == "saveclassconf":
                self.class_conf_save()
            elif cb == "savenewclass":
                self.class_new_save()
            elif cb == "savedelclass":
                self.class_del_save()
            elif cb == "savesubclass":
                self.class_update_save()

    def class_del_save(self):
        classname = self.get_argument("classname")
        print "classname:", classname
        if classname:
            sql = "delete from dba_stats.class_port where class = '%s'" % (classname)
            print sql
            self.dbhandler.execute(sql)

    def class_update_save(self):
        classname = self.get_argument("classname")
        namecn = self.get_argument("namecn")
        port = self.get_argument("port")
        hasreal = self.get_argument("hasreal")
        hasqa = self.get_argument("hasqa")
        hassim = self.get_argument("hassim")
        hasbak = self.get_argument("hasbak")
        bakhost = self.get_argument("bakhost")
        bakdir = self.get_argument("bakdir")
        bakdays = self.get_argument("bakdays")
        sql = ("update dba_stats.class_port set  port='%s',class_zh='%s',"
               "has_real='%s',has_qa='%s', has_sim='%s',has_bak='%s',bak_host='%s', "
               "bakdir='%s', retain_days='%s' where class='%s'"
               ) % (port, namecn, hasreal, hasqa, hassim, hasbak,bakhost,bakdir,bakdays,classname)
        print sql
        if classname:
            self.dbhandler.execute(sql)

    def class_new_save(self):
        classname = self.get_argument("classname")
        namecn = self.get_argument("namecn")
        port = self.get_argument("port")
        hasreal = self.get_argument("hasreal")
        hasqa = self.get_argument("hasqa")
        hassim = self.get_argument("hassim")
        hasbak = self.get_argument("hasbak")
        bakhost = self.get_argument("bakhost")
        bakdir = self.get_argument("bakdir")
        bakdays = self.get_argument("bakdays")
        sql = ("insert into dba_stats.class_port set class='%s', port='%s', "
               "class_zh='%s',has_real='%s',has_qa='%s', has_sim='%s',has_bak='%s'"
               ",bak_host='%s', bakdir='%s', retain_days='%s'"
               ) % (classname, port, namecn, hasreal, hasqa, hassim, hasbak,bakhost,bakdir,bakdays)
        print sql
        self.dbhandler.execute(sql)

    def class_conf_save(self):
        classname = self.get_argument("classname")
        dayphones = self.get_argument("dayphones")
        nightphones = self.get_argument("nightphones")
        thread_threshold = self.get_argument("thread_threshold")
        print "classname is :", classname
        if classname:
            sql = "insert ignore into  dba_stats.monitor_class set day_phones='%s', night_phones='%s', class='%s', thread_threshold='%s';" % (dayphones, nightphones, classname,thread_threshold)
            print sql
            self.dbhandler.execute(sql)

    def class_conf_update(self):
        classname = self.get_argument("classname")
        dayphones = self.get_argument("dayphones")
        nightphones = self.get_argument("nightphones")
        thread_threshold = self.get_argument("thread_threshold")
        print "classname is :", classname
        if classname:
            sql = "update dba_stats.monitor_class set day_phones='%s', night_phones='%s', thread_threshold='%s' where class='%s';" % (dayphones, nightphones, thread_threshold,classname)
            print sql
            self.dbhandler.execute(sql)

    def class_conf_del(self):
        classname = self.get_argument("classname")
        print "classname is :", classname
        if  classname:
            sql = "delete from   dba_stats.monitor_class where class='%s';" % classname
            print sql
            self.dbhandler.execute(sql)

    """函数作用:增加mysql监控项,默认开启监控状态"""
    def add_mon_save(self):
        name = self.get_argument("inputclassname")
        role = int(self.get_argument("inputclassrole"))
        host = self.get_argument("inputclasshost")
        realserver = self.get_argument("inputrealserver")
        port = int(self.get_argument("inputclassport"))
        daylag = int(self.get_argument("inputclassdaylag"))
        nightlag = int(self.get_argument("inputclassnightlag"))
        idc = self.get_argument("inputclassidc")
        usefor = self.get_argument("inputclassuserfor")
        comment = self.get_argument("inputclasscomment")

        sql = "insert into dba_stats.monitor_conf (class, is_master, host, port, usefor, day_lag, night_lag, is_mon,mon_one,mon_ten,idc, is_avail, com, one_starttime, ten_starttime, realserver) values ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s',now(),now(),'%s')" % (name, role, host, port, usefor, daylag, nightlag, 1, 1, 1, idc, 1, comment,realserver)
        print "in add_mon_save sql: ", sql
        self.dbhandler.execute(sql)


    """函数作用:关闭监控, montime为时间长度,pk是对应监控项的主键,montime=0表示开启监控"""
    def time_mon_save(self):
        montime = int(self.get_argument("montime"))
        pk = int(self.get_argument("pk"))
        dt = datetime.datetime.now() + datetime.timedelta(0, montime)
        if montime > 0:
            sql = "update dba_stats.monitor_conf set is_mon=0, mon_one=0, mon_ten=0, one_starttime='%s', ten_starttime='%s' where id=%s" % (dt.strftime("%Y-%m-%d %H:%M:%S"), dt.strftime("%Y-%m-%d %H:%M:%S"), pk)
        else: 
            sql = "update dba_stats.monitor_conf set is_mon=1, mon_one=1, mon_ten=1, one_starttime='%s', ten_starttime='%s' where id=%s" % (dt.strftime("%Y-%m-%d %H:%M:%S"), dt.strftime("%Y-%m-%d %H:%M:%S"), pk)
        self.dbhandler.execute(sql)

    """函数作用:删除监控项,传入参数为主键ID"""
    def del_mon_save(self):
        pk = int(self.get_argument("pk"))
        sql = "delete from dba_stats.monitor_conf where id='%s'" % (pk)
        self.dbhandler.execute(sql)

    """函数作用:编辑并保存监控项的修改"""
    def edit_mon_save(self):
        name = self.get_argument("editclassname")
        role = int(self.get_argument("editclassrole"))
        host = self.get_argument("editclasshost")
        realserver = self.get_argument("editrealserver")
        port = int(self.get_argument("editclassport"))
        daylag = int(self.get_argument("editclassdaylag"))
        nightlag = int(self.get_argument("editclassnightlag"))
        com = self.get_argument("editclasscom")
        pk = int(self.get_argument("pk"))

        sql = "update dba_stats.monitor_conf set class='%s', is_master=%s, host='%s', port=%s, day_lag=%s, night_lag=%s, com='%s', realserver='%s' where id=%s" % (name, role, host, port, daylag, nightlag,com, realserver,pk)
        self.dbhandler.execute(sql)
