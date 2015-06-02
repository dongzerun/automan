#!/bin/env python
#coding=utf-8
#by dongzerun
#db handler for mysql

import MySQLdb
import torndb

class MySQLHandler(object):
    def __init__(self, host=None, port=None, user=None, pwd=None, dbname=''):
        if not host and not port and not user and not pwd:
            self.host = "yz-log-ku-m00"
            self.port = 3306
            self.user = "dba_monitor"
            self.pwd = "ganjicac"
            self.dbname = "dba_stats"
        elif host and port and user and pwd:
            self.host = host
            self.port = port
            self.user = user
            self.pwd = pwd
            self.dbname = dbname
        else:
            raise
        self.conn = torndb.Connection(self.host + ':' + str(self.port), self.dbname, user=self.user, password=self.pwd ,time_zone="+8:00")
        self.conn.max_idle_time = 600
        self.conn.execute("set session sql_mode='ANSI'")
        """set max_idle_time < mysql max_idle_time"""

    def select_db(self, dbname):
        self.conn._db.select_db(dbname)

    def find(self, sql):
        #res =  self.conn.query(sql)
        res =  self.conn.query(sql.replace('%','%%'))
        return res

    def query(self):
        sql = "select realserver, id, class, is_master, host, port, usefor, day_lag, night_lag, is_mon, mon_one, mon_ten, idc, com,if((unix_timestamp(one_starttime) - unix_timestamp()) < 0, '00:00:00', (TIMEDIFF(one_starttime, now())) ) as one_starttime, if((unix_timestamp(ten_starttime) - unix_timestamp())<0,'00:00:00',(TIMEDIFF(ten_starttime, now())) )  as ten_starttime from monitor_conf  order by is_mon, class, host;"
        res = self.conn.query(sql)
        return res
    
    def query_classname(self):
        res = self.conn.query("select distinct class from dba_stats.monitor_class")
        return res
    def redis_classname(self):
        res = self.conn.query("select class from dba_stats.redis_mon_phones")
        return res

    def query_byidc(self, idc):
        sql = "select realserver,id, class, is_master, host, port, usefor, day_lag, night_lag, is_mon, mon_one, mon_ten, idc, com,if((unix_timestamp(one_starttime) - unix_timestamp()) < 0, '00:00:00', (TIMEDIFF(one_starttime, now())) ) as one_starttime, if((unix_timestamp(ten_starttime) - unix_timestamp())<0,'00:00:00',(TIMEDIFF(ten_starttime, now())) )  as ten_starttime from monitor_conf  where idc='%s' order by is_mon, class, host" % idc
        res = self.conn.query(sql)
        return res
    
    def query_classidc(self):
        sql = "select distinct idc from dba_stats.monitor_conf order by idc"
        res = self.conn.query(sql)
        return res

    def query_byclass(self, class_name):
        sql = "select realserver,id, class, is_master, host, port, usefor, day_lag, night_lag, is_mon, mon_one, mon_ten, idc, com,if((unix_timestamp(one_starttime) - unix_timestamp()) < 0, '00:00:00', (TIMEDIFF(one_starttime, now())) ) as one_starttime, if((unix_timestamp(ten_starttime) - unix_timestamp())<0,'00:00:00',(TIMEDIFF(ten_starttime, now())) )  as ten_starttime from monitor_conf  where class='%s' order by is_mon, host" % class_name
        res = self.conn.query(sql)
        return res

    def query_classbyuser(self, username):
        """autosql 按用户查找所拥有的产品线列表"""
        if not username:
            return None
        sql = "select distinct name,hostname,class as class_en,port,class_zh,env_type from dba_stats.users where name='%s'" % username
        res = self.conn.query(sql)
        return res

    def taskfile_todb(self, task_id, file_url):
        sql = "replace into dba_stats.autosql_tasks_files (task_id, file_url) values ('%s','%s');" % (task_id, file_url)
        self.conn.execute(sql)
    def execute(self, sql):
        self.conn.execute(sql.replace('%','%%'))
