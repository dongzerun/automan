#!/bin/env python
#coding=utf-8
#ganji web db management
#version 0.1.0

import os
import tornado.ioloop
import tornado.web
import tornado.gen
import MySQLHandler
import BaseHandler
import string
import datetime

class MonRedisHandler(BaseHandler.BaseHandler):
    dbhandler = MySQLHandler.MySQLHandler()
    redisclassname = []
    redishostname = []
    idc = []
    idc = dbhandler.query_classidc()
    #idc = ['M6','yz','sd']

    def get(self):
        self.checkCookie()
        url_request = string.split(self.request.uri, "/")
        self.redisclassname = self.dbhandler.find("select class from dba_stats.redis_mon_phones")
        self.redishostname = self.dbhandler.find("select distinct host from dba_stats.redis_conf order by host")
        if len(url_request) == 4 and url_request[3] == 'hostlist':
            get_allredis_sql = "select id, class, is_master, host, port, usefor, is_mon, mon_two, mon_ten, idc, com,if((unix_timestamp(two_starttime) - unix_timestamp()) < 0, '00:00:00', (TIMEDIFF(two_starttime, now())) ) as two_starttime, if((unix_timestamp(ten_starttime) - unix_timestamp())<0,'00:00:00',(TIMEDIFF(ten_starttime, now())) )  as ten_starttime from redis_conf  order by is_mon, class, usefor, host;"
            self.redishosts = self.dbhandler.find(get_allredis_sql)
            self.render("redis.html", redisclassname=self.redisclassname, idc=self.idc, hosts=self.redishosts, user=self.curuser)
        elif len(url_request) == 4 and url_request[3] == 'findbyhost':
            get_allredis_sql = "select id, class, is_master, host, port, usefor, is_mon, mon_two, mon_ten, idc, com,if((unix_timestamp(two_starttime) - unix_timestamp()) < 0, '00:00:00', (TIMEDIFF(two_starttime, now())) ) as two_starttime, if((unix_timestamp(ten_starttime) - unix_timestamp())<0,'00:00:00',(TIMEDIFF(ten_starttime, now())) )  as ten_starttime from redis_conf  order by is_mon, host, class, usefor;"
            self.redishosts = self.dbhandler.find(get_allredis_sql)
            self.render("findredis_byhost.html", redisclassname=self.redisclassname, redishostname=self.redishostname, idc=self.idc, hosts=self.redishosts, user=self.curuser)
        elif len(url_request) == 4 and url_request[3] == 'memmon':
            get_allredis_sql = "select id, class, is_master, host, port, usefor, mon_mem, mon_two, mon_ten, idc, com,if((unix_timestamp(two_starttime) - unix_timestamp()) < 0, '00:00:00', (TIMEDIFF(two_starttime, now())) ) as two_starttime, if((unix_timestamp(ten_starttime) - unix_timestamp())<0,'00:00:00',(TIMEDIFF(ten_starttime, now())) )  as ten_starttime ,if((unix_timestamp(mem_starttime) - unix_timestamp()) < 0, '00:00:00', (TIMEDIFF(mem_starttime, now())) ) as mem_starttime,floor(mem_limit/1024/1024/1024) as mem_limit from redis_conf where is_master != 2 order by mon_mem, class, host;"
            self.redishosts = self.dbhandler.find(get_allredis_sql)
            self.render("redis_mon_mem.html", redisclassname=self.redisclassname, idc=self.idc, hosts=self.redishosts, user=self.curuser)

        elif len(url_request) == 4 and url_request[3] == 'monconf':
            get_monconf_sql = "select * from dba_stats.redis_mon_phones order by class;"
            self.redishosts = self.dbhandler.find(get_monconf_sql)
            self.render("redis_monconf.html", redisclassname=self.redisclassname, idc=self.idc, hosts=self.redishosts, user=self.curuser)


        elif len(url_request) == 5:
                if url_request[3] == 'findbyidc' and url_request[4]:
                    get_redisbyidc_sql = "select id, class, is_master, host, port, usefor, is_mon, mon_two, mon_ten, idc, com,if((unix_timestamp(two_starttime) - unix_timestamp()) < 0, '00:00:00', (TIMEDIFF(two_starttime, now())) ) as two_starttime, if((unix_timestamp(ten_starttime) - unix_timestamp())<0,'00:00:00',(TIMEDIFF(ten_starttime, now())) )  as ten_starttime from redis_conf  where idc='%s' order by is_mon, class, host;" % url_request[4]
                    self.redishosts = self.dbhandler.find(get_redisbyidc_sql)
                    self.render("redis.html", redisclassname=self.redisclassname, idc=self.idc, hosts=self.redishosts, user=self.curuser)
                elif url_request[3] == 'findbyclass' and url_request[4]:
                    get_redisbyclass_sql = "select id, class, is_master, host, port, usefor, is_mon, mon_two, mon_ten, idc, com,if((unix_timestamp(two_starttime) - unix_timestamp()) < 0, '00:00:00', (TIMEDIFF(two_starttime, now())) ) as two_starttime, if((unix_timestamp(ten_starttime) - unix_timestamp())<0,'00:00:00',(TIMEDIFF(ten_starttime, now())) )  as ten_starttime from redis_conf  where class='%s' order by is_mon, class, usefor, host;" % url_request[4]
                    self.redishosts = self.dbhandler.find(get_redisbyclass_sql)
                    self.render("redis.html", redisclassname=self.redisclassname, idc=self.idc, hosts=self.redishosts, user=self.curuser)

                elif url_request[3] == 'findbyhost' and url_request[4]:
                    get_redisbyhost_sql = "select id, class, is_master, host, port, usefor, is_mon, mon_two, mon_ten, idc, com,if((unix_timestamp(two_starttime) - unix_timestamp()) < 0, '00:00:00', (TIMEDIFF(two_starttime, now())) ) as two_starttime, if((unix_timestamp(ten_starttime) - unix_timestamp())<0,'00:00:00',(TIMEDIFF(ten_starttime, now())) )  as ten_starttime from redis_conf  where host='%s' order by is_mon, host, class;" % url_request[4]
                    self.redishosts = self.dbhandler.find(get_redisbyhost_sql)
                    self.render("findredis_byhost.html", redisclassname=self.redisclassname, redishostname=self.redishostname, idc=self.idc, hosts=self.redishosts, user=self.curuser)
                elif url_request[3] == 'memmonfindbyclass' and url_request[4]:
                    get_memredisbyclass_sql = "select id, class, is_master, host, port, usefor, mon_mem, mon_two, mon_ten, idc, com,if((unix_timestamp(two_starttime) - unix_timestamp()) < 0, '00:00:00', (TIMEDIFF(two_starttime, now())) ) as two_starttime, if((unix_timestamp(ten_starttime) - unix_timestamp())<0,'00:00:00',(TIMEDIFF(ten_starttime, now())) )  as ten_starttime ,mem_starttime,floor(mem_limit/1024/1024/1024) as mem_limit from redis_conf where is_master != 2 and class ='%s' order by mon_mem, class, usefor, host;" % url_request[4]
                    self.redishosts = self.dbhandler.find(get_memredisbyclass_sql)
                    self.render("redis_mon_mem.html", redisclassname=self.redisclassname, idc=self.idc, hosts=self.redishosts, user=self.curuser)
                    
                    
    def post(self):
        self.checkCookie()
        if self.checked:
            cb = string.split(self.request.uri, "/")[3].lower()
            if cb == "add_mon_save":
                self.add_mon_save()
            elif cb == "time_mon_save":
                self.time_mon_save()
            elif cb == "del_mon_save":
                self.del_mon_save()
            elif cb == "edit_mon_save":
                self.edit_mon_save()
            elif cb == "mem_mon_save":
                self.mem_mon_save()
            elif cb == "edit_mem_mon":
                self.edit_mem_mon()
            elif cb == "add_monconf_save":
                self.add_monconf_save()
            elif cb == "edit_mon_conf":
                self.edit_mon_conf()
            elif cb == "del_mon_conf":
                self.del_mon_conf()

    """函数作用:增加redis监控项,默认开启监控状态"""
    def add_mon_save(self):
        name = self.get_argument("inputclassname")
        role = int(self.get_argument("inputclassrole"))
        host = self.get_argument("inputclasshost")
        port = int(self.get_argument("inputclassport"))
        idc = self.get_argument("inputclassidc")
        usefor = self.get_argument("inputclassuserfor")
        comment = self.get_argument("inputclasscomment")
        sql = "insert into dba_stats.redis_conf (class, is_master, host, port, usefor, is_mon,mon_two,mon_ten,idc, com, two_starttime, ten_starttime,mon_mem,mem_limit,mem_starttime) values ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s',now(),now(),%s,%s,now())" % (name, role, host, port, usefor, 1, 1, 1, idc, comment,1,10737418240)
        self.dbhandler.execute(sql)

    '''增加新的产品线'''
    def add_monconf_save(self):
        name = self.get_argument("inputclassname")
        phones = self.get_argument("inputclassphones")
        emails = self.get_argument("inputclassemails")
        sql = "insert into dba_stats.redis_mon_phones (class, phones, emails) values('%s','%s','%s')" % (name,phones,emails)
        self.dbhandler.execute(sql)
        
    """函数作用:关闭监控, montime为时间长度,pk是对应监控项的主键,montime=0表示开启监控"""
    def time_mon_save(self):
        montime = int(self.get_argument("montime"))
        pk = int(self.get_argument("pk"))
        dt = datetime.datetime.now() + datetime.timedelta(0, montime)
        if montime > 0:
            sql = "update dba_stats.redis_conf set is_mon=0, mon_two=0, mon_ten=0, two_starttime='%s', ten_starttime='%s' where id=%s" % (dt.strftime("%Y-%m-%d %H:%M:%S"), dt.strftime("%Y-%m-%d %H:%M:%S"), pk)
        else:
            sql = "update dba_stats.redis_conf set is_mon=1, mon_two=1, mon_ten=1, two_starttime='%s', ten_starttime='%s' where id=%s" % (dt.strftime("%Y-%m-%d %H:%M:%S"), dt.strftime("%Y-%m-%d %H:%M:%S"), pk)
        self.dbhandler.execute(sql)

    ''' 关闭内存监控'''
    def mem_mon_save(self):
        montime = int(self.get_argument("montime"))
        pk = int(self.get_argument("pk"))
        dt = datetime.datetime.now() + datetime.timedelta(0, montime)
        if montime > 0:
            sql = "update dba_stats.redis_conf set mon_mem=0, mem_starttime='%s' where id=%s" % (dt.strftime("%Y-%m-%d %H:%M:%S"), pk)
        else:
            sql = "update dba_stats.redis_conf set mon_mem=1, mem_starttime='%s' where id=%s" % (dt.strftime("%Y-%m-%d %H:%M:%S"), pk)
        self.dbhandler.execute(sql)

    """函数作用:编辑并保存监控项的修改"""
    def edit_mon_save(self):
        name = self.get_argument("editclassname")
        role = int(self.get_argument("editclassrole"))
        host = self.get_argument("editclasshost")
        port = int(self.get_argument("editclassport"))
        com = self.get_argument("editclasscom")
        pk = int(self.get_argument("pk"))

        sql = "update dba_stats.redis_conf set class='%s', is_master=%s, host='%s', port=%s, com='%s' where id=%s" % (name, role, host, port, com, pk)
        self.dbhandler.execute(sql)
    ''' 编辑保存内存监控的修改'''
    def edit_mem_mon(self):
        name = self.get_argument("editclassname")
        role = int(self.get_argument("editclassrole"))
        host = self.get_argument("editclasshost")
        port = int(self.get_argument("editclassport"))
        memlimit = int(self.get_argument("editclassmemlimit"))*1024*1024*1024
        pk = int(self.get_argument("pk"))

        sql = "update dba_stats.redis_conf set class='%s', is_master=%s, host='%s', port=%s, mem_limit=%s where id=%s" % (name, role, host, port, memlimit, pk)
        self.dbhandler.execute(sql)

    ''' 编辑报警保存电话邮件'''
    def edit_mon_conf(self):
        name = self.get_argument("editclassname")
        phones = self.get_argument("editclassphones")
        emails = self.get_argument("editclassemails")
        pk = int(self.get_argument("pk"))

        sql = "update dba_stats.redis_mon_phones set class='%s', phones='%s', emails='%s' where id=%s" %(name,phones,emails,pk)
        self.dbhandler.execute(sql)


    """函数作用:删除监控项,传入参数为主键ID"""
    def del_mon_save(self):
        pk = int(self.get_argument("pk"))
        sql = "delete from dba_stats.redis_conf where id='%s'" % (pk)
        self.dbhandler.execute(sql)

    ''' 删除产品线的报警'''
    def del_mon_conf(self):
        pk = int(self.get_argument("pk"))
        sql = "delete from dba_stats.redis_mon_phones where id='%s'" % (pk)
        self.dbhandler.execute(sql)
