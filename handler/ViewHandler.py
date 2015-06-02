#!/bin/env python
#coding=utf-8
#ganji web db management
#by dongzerun 20140723
#version 0.1.0

import os
import tornado.ioloop
import tornado.web
import tornado.gen
import BaseHandler
import time
import string
import MySQLdb
import influxdb
import json
from MySQLHandler import MySQLHandler
from concurrent.futures import ThreadPoolExecutor
from functools import partial, wraps

EXECUTOR = ThreadPoolExecutor(max_workers=10)

def unblock(f):

    @tornado.web.asynchronous
    @wraps(f)
    def wrapper(*args, **kwargs):
        self = args[0]

        def callback(future):
            self.write(future.result())
            self.finish()

        EXECUTOR.submit(
            partial(f, *args, **kwargs)
        ).add_done_callback(
            lambda future: tornado.ioloop.IOLoop.instance().add_callback(
                partial(callback, future)))

    return wrapper

class ViewHandler(BaseHandler.BaseHandler):
    dbhandler = MySQLHandler()
    influx = influxdb.InfluxDBClient(host="g1-db-srv-03.dns.ganji.com",port=8086,username="root",password="ganjicac",database="mysqlslow")

    @tornado.web.asynchronous
    def get(self):

        def callback(future):
            self.write(future.result())
            self.finish()

        EXECUTOR.submit(
            partial(self.get_)
        ).add_done_callback(
            lambda future: tornado.ioloop.IOLoop.instance().add_callback(
                partial(callback, future)))

    def get_(self):
        self.checkCookie()
        url_request = string.split(self.request.uri, "/")
        print len(url_request), url_request
        sql="select id,class, class_zh, has_real, has_qa, has_sim, port from  dba_stats.class_port;"
        classes = self.dbhandler.find(sql)
        ##/view/mysql/allclasses
        if len(url_request) == 4:
            if url_request[2] == 'mysql' and url_request[3].startswith('getbyclass'):
                cname = self.get_argument('classname')
                classdata = self.getinfobyclass(cname)
                self.render("view_mysqlgetbyclass.html", user=self.curuser, classdata=classdata, cname=cname)
            elif url_request[2] == 'mysql' and url_request[3].startswith('tablesrows'):
                sql="select * from dba_stats.statics_table_rows where rows > 10000000 order by rows desc;"
                data=self.dbhandler.find(sql)
                sql="select * from dba_stats.mysql_metrics"
                metrics=self.dbhandler.find(sql)
                self.render("view_tablesrows.html",  user=self.curuser, tablerows=data, classes=classes, metrics=metrics)
            elif url_request[2] == 'mysql' and url_request[3].startswith("sqltrack"):
                self.render("view_sqltrack.html", user=self.curuser,classes=classes)
            elif url_request[2] == 'mysql':
                self.render("view.html", user=self.curuser,classes=classes)
        else:
            self.render("view.html", user=self.curuser,classes=classes)

    def getinfobyclass(self, name):
        data = []
        sql="select class,port, 'g1-off-ku-real' as host, 'g1' as idc, 4 as is_master  from dba_stats.class_port where has_real=1 and class='%s'" % name
        realinstances = self.dbhandler.find(sql)
        if len(realinstances) > 0:
            for i in realinstances:
                data.append(self.getinfobyinstance(i))

        sql="select class,host,port,idc,is_master from dba_stats.monitor_conf where class='%s' and is_master in (0,1,2,3,5) order by is_master desc" % name
        instances = self.dbhandler.find(sql)
        for i in instances:
            data.append(self.getinfobyinstance(i))
        return data

    def getinfobyinstance(self, args):
        res = args
        try:
            conn = MySQLHandler(host=args['host'], port=args['port'], user='dba_monitor', pwd='ganjicac')
        except MySQLdb.Error,e:
            res.update({'alive':0})
            res.update({'masterhost':'dead'})
            res.update({'masterlogfile':'dead'})
            res.update({'masterid': 'dead'})
            res.update({'masterlogpos':'dead'})
            res.update({'slavesql':'dead'})
            res.update({'secbeh':'dead'})
            res.update({'serverid':'dead'})
            res.update({'mysqlv':'dead'})
            res.update({'uptime': 'dead'})
            res.update({'connections':'dead'})
            return res

        sql = "show slave status"
        replinfo = conn.find(sql)
        sql = "select @@server_id as serverid"
        serverid = conn.find(sql)
        sql = "show global status like 'Threads_connected'"
        conns = conn.find(sql)
        sql = "select @@version as mysqlv"
        mysqlv = conn.find(sql)
        sql = "show global status like 'uptime'"
        uptime = conn.find(sql)
        conn.conn.close()
            
        res.update(serverid[0])
        if len(mysqlv[0]['mysqlv']) > 6:
            res.update({'mysqlv':mysqlv[0]['mysqlv'][0:6]})
        else:
            res.update({'mysqlv':mysqlv[0]['mysqlv']})
        res.update({'alive':1})
        res.update({'uptime': int(uptime[0]['Value']) / 86400})
        res.update({'connections':conns[0]['Value']})
        if len(replinfo) > 0:
            res.update({'masterhost':replinfo[0]['Master_Host']})
            res.update({'masterlogfile':replinfo[0]['Relay_Master_Log_File']})
            if 'Master_Server_Id' in replinfo[0]:
                res.update({'masterid': replinfo[0]['Master_Server_Id']})
            else:
                res.update({'masterid': ''})
            res.update({'masterlogpos':replinfo[0]['Exec_Master_Log_Pos']})
            res.update({'secbeh':replinfo[0]['Seconds_Behind_Master']})
        else:
            res.update({'masterhost':''})
            res.update({'masterlogfile':''})
            res.update({'masterid': ''})
            res.update({'masterlogpos':''})
            res.update({'slavesql':''})
            res.update({'secbeh':''})
            
        return res

    @tornado.web.asynchronous
    def post(self):

        def callback(future):
            self.write(future.result())
            self.finish()

        EXECUTOR.submit(
            partial(self.post_)
        ).add_done_callback(
            lambda future: tornado.ioloop.IOLoop.instance().add_callback(
                partial(callback, future)))


    def post_(self):
        self.checkCookie()
        url_request = string.split(self.request.uri, "/")
        print len(url_request), url_request
        if len(url_request) == 4:
            print len(url_request), url_request
            if url_request[2] == 'mysql' and url_request[3].startswith("tracker"):
                hostname = self.get_argument("hostname")
                product = self.get_argument("product")
                useindex = self.get_argument("useindex")
                dbname = self.get_argument("dbname")
                tbname = self.get_argument("tbname")
                data = self.querylists(product, useindex, tbname=tbname,dbname=dbname, host=hostname)
                #for async write
                #self.write(json.dumps(data))
                return json.dumps(data)
            elif url_request[2] == 'mysql' and url_request[3].startswith("getsqldetailbyid"):
                product = self.get_argument("product")
                tbname = self.get_argument("tbname")
                id = self.get_argument("id")
                data = self.querydetail(product, id, tbname=tbname)
                #for async write
                #self.write(json.dumps(data))
                return json.dumps(data)

            elif url_request[2] == 'mysql' and url_request[3].startswith("moretrackdata"):
                hostname = self.get_argument("hostname")
                product = self.get_argument("product")
                useindex = self.get_argument("useindex")
                dbname = self.get_argument("dbname")
                tbname = self.get_argument("tbname")
                lasttime = int(self.get_argument("lasttime"))
                d = time.gmtime(lasttime)
                strtime = time.strftime("%Y-%m-%d %H:%M:%d", d)
                print "strtime is : ", strtime
                data = self.querylists(product, useindex, tbname=tbname,lasttime=strtime,dbname=dbname, host=hostname)
                #for async write
                #self.write(json.dumps(data))
                return json.dumps(data)
                

    def querydetail(self, product, id, tbname=None):
        print "product, id, tbname:", product, id, tbname
        if tbname != "":
            sql = "select * from %s.%s where id = '%s' limit 1 " % (product, tbname, id)
        else:
            sql = "select * from %s where id = '%s' limit 1 " % (product, id)        
        #sql = "select  useindex, schema, table,sql, slowtime, rowsexamined, host, bytessent, rowsread from %s where id = '%s' limit 1 " % (product, id)        
        return self.influxquery(sql)

    def querylists(self,product, useindex, dbname=None, tbname=None, time=None, host=None, lasttime=None):
        err = {"error":""}
        if tbname != "":
            sql = "select id, useindex, schema, table,sql, slowtime, rowsexamined,time from %s.%s where table = '%s' " % (product, tbname, tbname)
        else:
            sql = "select id, useindex, schema, table,sql, slowtime, rowsexamined,time from %s " % (product)

        if dbname != "":
            if string.find(sql, 'where') != -1:
                sql = sql + " and schema= '%s' "  % (dbname)
            else:
                sql = sql + " where schema= '%s' "  % (dbname)
        if host != "":
            if string.find(sql, 'where') != -1:
                sql = sql + " and host = '%s' "  % (host)
            else:
                sql = sql + " where host = '%s' "  % (host)
        #All Yes No
        if useindex == "Yes":
            if string.find(sql, 'where') != -1:
                sql = sql + " and useindex = 'true' "
            else:
                sql = sql + " where useindex = 'true' "
        elif useindex == "No":
            if string.find(sql, 'where') != -1:
                sql = sql + " and useindex = 'false' "
            else:
                sql = sql + " where useindex = 'false' "
        if lasttime:
            if string.find(sql, 'where') != -1:
                sql = sql + " and time < '%s' " % lasttime
            else:
                sql = sql + " where time < '%s' " % lasttime
        print lasttime, sql

        sql = sql + " limit 150"
        return self.influxquery(sql)

    def influxquery(self, sql):
        serverts = int(time.time())
        err = [{"error":"influxquery error"}]
        try:
            data = self.influx.query(sql)
        except Exception, e:
            print e
            return []
        if data:
            points = data[0]["points"]
            columns = data[0]["columns"]
            output = []
            for p in points:
                tmp=dict(zip(columns, p))
                #tmp.append({"serverts":serverts})
                tmp["serverts"] = serverts
                output.append(tmp)
            #output.append({"serverts":serverts})
            return output
