#!/bin/env python
#coding=utf-8

import MySQLdb
import time
import datetime

def get_taskid():
    user = "dbwebm"
    pwd = "RW01f1nTbqXJR5MsU8"
    host = "yz-log-ku-m00.dns.ganji.com"
    dbname = "dba_stats"
    port = 3306
    try:
        conn = MySQLdb.connect(host=host,user=user,passwd=pwd,port=port,db=dbname)
        cursor = conn.cursor() 
        SQL = "replace into automan_taskid(time,name) values(unix_timestamp(),'automan')"
        cursor.execute(SQL)
        task_id = conn.insert_id()
        conn.commit()
        return task_id
    except MySQLdb.Error,e:
        now = time.mktime(datetime.datetime.now().timetuple())
        return int(now)

