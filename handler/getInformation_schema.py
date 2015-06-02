#!/usr/local/bin/python
#encoding=utf-8
#get information_schema 
#tables rows,auto_increment id etc.....

import time
import redis
from MySQLHandler import MySQLHandler
from asynctasks.sqlconfig import dbuser, dbpwd


redis = redis.Redis(host='yz-log-ku-01.dns.ganji.com', port=8888,socket_timeout=3) 
logdb = MySQLHandler()

def init():
    """truncate table statics_table_rows"""
    sql = "truncate table dba_stats.statics_table_rows"
    logdb.execute(sql)

def getclasses():
    sql = "select class, host, port from  dba_stats.monitor_conf where is_master=3 and class not in ('rp','arch','fang','rpbg')   group by class;"
    classes = logdb.find(sql)
    for i in classes:
        data = getbyinstance(i)

def getbyinstance(args):
    conn = MySQLHandler(host=args['host'], port=args['port'], user=dbuser, pwd=dbpwd)
    sql = "show databases"
    dbs = conn.find(sql)
    print args['class']
    for db in dbs:
        if db['Database'] in ('information_schema','test','mysql','performance_schema','percona'):
            continue
        print db['Database']
        redis.hset(args['class'], db['Database'], '')
        sql = "show table status"
        conn.select_db(db['Database'])
        tbs = conn.find(sql)
        for tb in tbs:
            redis.hset(args['class'] + '.' + db['Database'],  tb['Name'], '')
            k = args['class'] + '.' + db['Database'] + '.' +  tb['Name']
            v =  tb['Rows']
            redis.set(k,v)
            redis.set(tb['Name'], args['class'] + '.' + db['Database'] )
            redis.set(db['Database'], args['class'])
            k = args['class'] + '.' +  tb['Name']
            redis.set(k,v)
            redis.set('rows_version', int(time.time()))

            findpksql = "select * from information_schema.COLUMNS where table_schema='%s' and  EXTRA='auto_increment' and COLUMN_KEY='PRI' and table_name='%s'" % (db['Database'], tb['Name'])
            findpkdata = conn.find(findpksql)
            if len(findpkdata) == 0:
                pkname=''
                pktype=''
                pkid=0
            else:
                pkname=findpkdata[0]['COLUMN_NAME']
                pktype=findpkdata[0]['COLUMN_TYPE']
                findpkidsql = "select * from information_schema.tables where  table_schema='%s' and table_name='%s'"  % (db['Database'], tb['Name'])
                findpkiddata = conn.find(findpkidsql)
                if len(findpkiddata) > 0:
                    pkid=findpkiddata[0]['AUTO_INCREMENT']
                else:
                    pkid=0

            sql = "insert into dba_stats.statics_table_rows (classname,dbname,tbname,rows, pkname, pktype, pkid) values ('%s','%s','%s','%s','%s','%s','%s')" % (args['class'], db['Database'], tb['Name'], tb['Rows'], pkname, pktype, pkid)
            logdb.execute(sql)

def getinfo():
    getclasses()

def main():
    init()
    getinfo()

if __name__ == "__main__":
    main()
