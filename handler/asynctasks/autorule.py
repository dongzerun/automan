#!/bin/env python
#encoding=utf-8
#by dongzerun 
#test autosql rule and generate backup sql

#from __future__ import unicode_literals 
import sys
import os
sys.path.append("/data/mysql/automan/handler")
import time
import datetime
import urllib
import urllib2
import re
from  utils.redistool import RowsGet
from MySQLHandler import MySQLHandler
from  sqlconfig import pknames,pkpattern,allclasses,dangerclasses

class RuleError(Exception):
    def __init__(self, file, message):
        self.message = message
        self.file = file
        self.output = None
    def __str__(self):
        return "File: %s \n Error: %s" % (self.file, self.message)


class Rule(object):
    name="autorule"
    has_auto_pk = False
    cols = 0
    indexes = 0
    textcols = 0
    pkname = ''
    classes = 'log'
    dbhandler = None
    instances = None
    ckrows = RowsGet(host='yz-log-ku-01',port=8888)

    def __init__(self, task_id, sql, classes=None):
        self._sql = sql
        self.task_id = task_id
        if  classes:
            self.classes = classes
        self.dbhandler = MySQLHandler()
        self.pkequal = True

    def checkrule(self):
        print self._sql[0], self._sql
        if self._sql[0] == 'select':
            return RuleError(self._sql[-1]['location'], 'SELECT sql forbidden') 
        if self._sql[0] == 'add_index':
            self.delayself()
            return None
        if self._sql[0] == 'remove_index':
            self.delayself()
            return None
        if self._sql[0] == 'change_engine':
            self.delayself()
            return None
        if self._sql[0] == 'remove_column':
            self.delayself()
            return None
        if self._sql[0] == 'change_column':
            self.delayself()
            return self.chcol_rule()
        if self._sql[0] == 'add_column':
            self.delayself()
            return self.addcol_rule()
        if self._sql[0] == 'delete':
            return self.delete_rule()
        if self._sql[0] == 'update':
            return self.update_rule()
        if self._sql[0] == 'create_database':
            return self.createdb_rule()
        if self._sql[0] == 'use':
            return None
        if self._sql[0] == 'create_table':
            return self.createtb_rule()
        if self._sql[0] == 'insert':
            return self.insert_rule()
        if self._sql[0] == 'replace':
            return self.replace_rule()

        return RuleError(self._sql[-1]['location'], 'Unsupported sql type, please contact DBA')

    def delaydelta(self):
        rows = self.ckrows.getrows(self.classes + '.' + self._sql[1])
        print self.classes + '.' + self._sql[1] , "get rows: ", rows
        
        #return second
        curr_unix = time.mktime(time.strptime(datetime.datetime.now().strftime('%Y-%m-%d'), '%Y-%m-%d'))
        if   rows < 10000:
            deltatime = 0
        elif rows < 20000:
            deltatime = 1
        elif rows < 50000:
            deltatime = 1.5
        elif rows < 70000:
            deltatime = 2
        elif rows < 100000:
            deltatime = 3.5
        elif rows < 200000:
            deltatime = 5
        elif rows < 300000:
            deltatime = 7
        elif rows < 500000:
            deltatime = 8
        elif rows < 1000000:
            deltatime = 11
        elif rows < 1500000:
            deltatime = 14
        elif rows < 2000000:
            deltatime = 15
        elif rows < 2500000:
            deltatime = 16
        elif rows < 3000000:
            deltatime = 17
        else:
            deltatime = 18
        
        return int(curr_unix) + 57600 + deltatime * 1800

    def delayself(self):
        print self.classes
        sql = "select * from  dba_stats.autosql_ddl_tasks  where task_id='%s' limit 1;" % (self.task_id)
        try:
            res = self.dbhandler.find(sql)
        except MySQLdb.Error,e:
            return False, str(e)

        forcetime = self.delaydelta()

        if len(res) < 1:
            current_time = datetime.datetime.now()
            sys_time = (current_time + datetime.timedelta(days=1)).strftime('%Y-%m-%d')
            forcetime =  int(time.mktime(time.strptime(sys_time, '%Y-%m-%d')))
        else:
            expect_time =  int(res[0]['expect_time'])
            current_time = datetime.datetime.now()
            if self.classes in dangerclasses:
                forcetime = forcetime + 380
                #sys_time = (current_time + datetime.timedelta(days=1)).strftime('%Y-%m-%d')
                #sys_timestamp =  int(time.mktime(time.strptime(sys_time, '%Y-%m-%d')))
            #else:
            #    sys_time = (current_time).strftime('%Y-%m-%d ')
            #    sys_timestamp =  int(time.mktime(time.strptime(sys_time + '21:00', '%Y-%m-%d %H:%M')))
            if forcetime < expect_time:
                forcetime = expect_time

        sql = "update dba_stats.autosql_ddl_tasks set delay = 1,expect_time = '%s' where task_id='%s';" % (forcetime, self.task_id)
        print sql
        try:
            self.dbhandler.execute(sql)
            return True, None
        except MySQLdb.Error,e:
            return False, str(e)

    def genbaksql(self):
        """DML反转备份, 并且use必须记录"""
        """replace需要反查数据库,根据主键或唯一索引生成备份sql"""
        if self._sql[0] == 'replace':
            return self.replace_backup()
        if self._sql[0] == 'delete':
            return self.delete_backup()
        if self._sql[0] == 'update':
            return self.update_backup()
        if self._sql[0] == 'use':
            return self.use_backup()
        return None

    def run(self):
        ckrule = self.checkrule()

        if isinstance(ckrule, RuleError):
            success = False
            result = (success, ckrule, None)
            return result
        else:
            success = True
            baksql = self.genbaksql()
            result = (success, ckrule, baksql)
            return result

    def insert_rule(self):
        insertval = self._sql[3]
        if len(insertval) > 100:
            return RuleError(self._sql[-1]['location'], 'multiple insert values must less than 100')
        if isinstance(insertval[0], str):
            if insertval[0] == 'select':
                return RuleError(self._sql[-1]['location'], 'insert from select forbidden')
        return None

    def replace_rule(self):
        return self.insert_rule()

    def replace_backup(self):
        """根据replace的表名反查primary 或是 unique key 来做备份"""
        columns = self._sql[2]
        values = self._sql[3]
        name = self._sql[1][1]
        colindex = None
        bakvalues = []
        bakcolumn = None
        pknames = self.get_structs(name)
        for pkname in pknames:
            for i in range(len(columns)):
                if columns[i] == pkname:
                    bakcolumn = pkname
                    colindex = i;
                    break
        for value in values:
             bakvalues.append(value[colindex])
        bakvalues = ["'" + str(x).decode('utf8') + "'" for x in bakvalues]
        return "select * from %s where %s in (%s);" % (name, bakcolumn, ','.join(bakvalues))
        
    def get_structs(self, name):
        """去数据库中反查表结构,如果tbname是纯表名需要反查information_schema.tables表
           如果是db.table,则直接查询即可,最后返回主键和唯一索引,如果均无,反回None"""

        if len(name.split('.')) == 1:
            tbname = name
            sql = "select  column_name from columns where table_name='%s' and column_key in ('PRI', 'UIN');" % tbname
        elif len(name.split('.')) == 2:
            dbname, tbname = name.split('.')
            sql = "select  column_name from columns where table_name='%s' and table_schema = '%s' and column_key in ('PRI', 'UIN');" % (tbname, dbname)
        else:
            raise


        if self.classes in allclasses:
            self.instances = allclasses[self.classes]
            if self.classes not in ('qe', 'qeedm') and len(self.instances) != 1:
                raise
        else:
            raise

        

        for i in self.instances:
            self.dbhandler = MySQLHandler(host=i[0], port=i[1], user='dba_monitor',pwd='ganjicac',dbname='information_schema')
            pknames = self.dbhandler.find(sql)
            if len(pknames) > 0:
                return [x['column_name'] for x in pknames] 

    def chcol_rule(self):
        opt = self._sql[-1]
        if 'COMMENT' not in opt:
            return RuleError(self._sql[-1]['location'], 'every column must contain COMMENT')
        if self.classes == 'qe':
            return None
        if 'default' not in opt:
            return RuleError(self._sql[-1]['location'], 'every column must write  not NULL  and has DEFAULT value')
        elif not isinstance(opt['default'], (int, str, float, datetime.datetime)):
            return RuleError(self._sql[-1]['location'], 'every column must write  not NULL  and has DEFAULT value')

        if 'null' not in opt:
            return RuleError(self._sql[-1]['location'], 'every column must write  not NULL  and has DEFAULT value')
        elif  opt['null']:
            return RuleError(self._sql[-1]['location'], 'every column must write  not NULL  and has DEFAULT value')

        return None

    def addcol_rule(self):
        opt = self._sql[-1]
        if 'COMMENT' not in opt:
            return RuleError(self._sql[-1]['location'], 'every column must contain COMMENT')
        if self.classes == 'qe':
            return None
    
        if 'default' not in opt:
            return RuleError(self._sql[-1]['location'], 'every column must write  not NULL  and has DEFAULT value')

        if 'null' not in opt:
            return RuleError(self._sql[-1]['location'], 'every column must write  not NULL  and has DEFAULT value')
        elif  opt['null']:
            return RuleError(self._sql[-1]['location'], 'every column must write  not NULL  and has DEFAULT value')

        return None
            

    def createtb_rule(self):
        if 'if_not_exists' not in self._sql[3]: 
            return RuleError(self._sql[3]['location'], 'please write if not exists')
        if 'options' not in self._sql[3]:
            return RuleError(self._sql[3]['location'], 'please write table options')

        opt = dict(self._sql[3]['options'])
        if 'engine' in opt:
            if opt['engine'] not in ('InnoDB', 'innodb', 'queue', 'Queue', 'QUEUE', 'INNODB'):
                return RuleError(self._sql[3]['location'], 'MyiSAM forbidden default engine must innodb or queue')
            if 'charset' in opt:
                if opt['charset'] != 'utf8' and opt['charset'] != 'utf8mb4':
                    return RuleError(self._sql[3]['location'], 'charset must utf8 or utf8mb4')
            if 'comment' not in opt:
                return RuleError(self._sql[3]['location'], 'please write table comment')

        if self.classes == 'qe':
            return None

        for column in  self._sql[2]:
            if column[0] == 'column':
                if column[2] in ('binary', 'longbinary', 'tinybinary','mediumbinary'):
                    return RuleError(self._sql[3]['location'], 'table column can not contain binary type')
                if column[2] in ('text', 'longtext', 'mediumtext'):
                    self.textcols = self.textcols + 1
                if 'COMMENT' not in column[-1]:
                    return RuleError(self._sql[3]['location'], 'every column must contain COMMENT')
                if 'auto_increment' in column[3]:
                    self.has_auto_pk = True
                elif column[2] not in ('text', 'longtext', 'mediumtext') and 'auto_increment' not in column[3]:
                    if 'default' not in column[3] or 'null' not in column[3]:
                        return RuleError(self._sql[3]['location'], 'every column must write  not NULL  and has DEFAULT value')
                self.cols = self.cols + 1
            if column[0] in ('primary_key', 'index', 'unique'):
                    self.indexes = self.indexes + 1

        """必须显示指定自增主键"""
        if not self.has_auto_pk:
            return RuleError(self._sql[3]['location'], 'table must have a auto increment primary key')
        """索引数目不能过少,比例 至少大于5"""
        if self.indexes > 0:
            if self.cols / (self.indexes + 1) >= 20:
                return RuleError(self._sql[3]['location'], 'indexes of this table too few, please rewrite sql')
        """text字段影响性能, 比例至少小于10"""
        if self.textcols > 0:
            if self.cols / self.textcols <= 4:
                return RuleError(self._sql[3]['location'], 'cause performance text columns should not too much, please rewrite sql')
        return None

    def createdb_rule(self):
        if self._sql[0] == 'create_database':
            return RuleError(self._sql[2]['location'], 'create new database, please contact DBA')
        return None

    def mustequal(self, op, s1, s2):
        if not isinstance(s1, tuple) and not isinstance(s2, tuple):
            if s1 == self.pkname:
                print "sql print: ", s1, op, s2
                if op != "=":
                    print op
                    self.pkequal = False
        elif  isinstance(s1, tuple) and isinstance(s2, tuple):
            return '{} {} {}'.format(self.mustequal(*s1), op , self.mustequal(*s2))
        elif isinstance(s1, tuple):
            return '{} {} {}'.format( self.mustequal(*s1) , op , s2)
        else:
            return '{} {} {}'.format( s1, op , self.mustequal(*s2))


    def update_rule(self):
        """where条件不许为空"""
        if 'where' not in self._sql[3]:
            return RuleError(self._sql[3]['location'], 'update sql must have where clause')

        """where 条件不允许为真"""
        if not isinstance(self._sql[3]['where'], tuple):
            return RuleError(self._sql[3]['location'], 'where clause must not null or true forever')

        """如果有or 条件, true条件,或非常用主键,唯一索引等不允许通过"""
        try:
            res = gensql(*self._sql[3]['where'])
            if not isinstance(res, RuleError):
                match = pkpattern.search(res)
                if match:
                    self.pkname = match.group()
                    print "pkpattern find pk name: ", self.pkname
                else:
                    return RuleError(self._sql[3]['location'], 'where clause must contain primary or unique key')
                self.mustequal(*self._sql[3]['where'])
                if not self.pkequal:
                    return RuleError(self._sql[3]['location'], 'where clause pkname operation must be = , range operation forbidden!')
        except  Exception, e:
            print e
            return RuleError(self._sql[3]['location'], e)
        if isinstance(res, RuleError):
            res.file = self._sql[3]['location']
            return res
        return None


    def update_backup(self):
        res = gensql(*self._sql[-1]['where'])
        if isinstance(self._sql[1], str):
            return "select * from %s where %s;" % (self._sql[1], res)
        elif isinstance(self._sql[1], (list, tuple)):
            return "select * from %s where %s;" % (self._sql[1][0], res)

    def delete_backup(self):
        return self.update_backup()

    def use_backup(self):
        return "use `%s`;" % self._sql[1] 

    def delete_rule(self):
        """where 条件不允许为空"""
        if 'where' not  in self._sql[2]:
            return RuleError(self._sql[2]['location'], 'delete sql must have where clause')

        """where 条件不允许为真"""
        if not isinstance(self._sql[2]['where'], tuple):
            return RuleError(self._sql[2]['location'], 'where clause must not null or true forever')

        """如果有or 条件, true条件,或非常用主键,唯一索引等不允许通过"""
        try:
            res = gensql(*self._sql[2]['where'])
            if not isinstance(res, RuleError):
                match = pkpattern.search(res)
                if match:
                    self.pkname = match.group()
                    if not self.pkname:
                        return RuleError(self._sql[2]['location'], 'where clause must contain primary or unique key')
                    self.mustequal(*self._sql[2]['where'])
                    if not self.pkequal:
                        return RuleError(self._sql[2]['location'], 'where clause pkname operation must be = , range operation forbidden!')
                else:
                    return RuleError(self._sql[2]['location'], 'where clause must contain primary or unique key')
        except  Exception, e:
            return RuleError(self._sql[2]['location'], e)
        if isinstance(res, RuleError):
            res.file = self._sql[2]['location']
            return res
        return None



def gensql(op, s1=None, s2=None):
    if op == 'in':
        if isinstance(s1, str) and isinstance(s2, (tuple,list)):
            tmplist = ["'" + str(x) + "'" for x in s2]
            strlist = (',').join(tmplist)
            return ' '  + s1 + ' in ' + '(' + strlist  + ')' + ' '
    if op == 'or':
        return RuleError('','where clause can not contain OR, please split it into two sqls')
    if op == 'not':
        tmp =  "not " + s1[0]
        s1[0] = tmp
    if not isinstance(s1, (tuple,list)) and not isinstance(s2, (tuple,list)):
        return "{} {} '{}'".format(str(s1) , op , str(s2))
    elif  isinstance(s1, (tuple,list)) and isinstance(s2, (tuple,list)):
        return "{} {} {}".format( gensql(*s1) , op , gensql(*s2))
    elif isinstance(s1, (tuple,list)):
        return "{} {} {}".format( gensql(*s1) , op , s2)
    elif not s1 and s2:
        return "{} {} ".format(s1 , op , gensql(*s2))
    elif s1 and not s2:
        return "{} ".format(s1)
    else:
        return "{} {} {}".format(s1 , op , gensql(*s2))


def searchpkclause(op, s1=None, s2=None, pkname = None):
    """根据主键或唯一索引反写delete, update的备份sql"""
    if not isinstance(s1, (tuple,list)) and not isinstance(s2, (tuple,list)):
        if str(s1) == pkname:
            return "{} {} '{}'".format(str(s1) , op , str(s2))
        else:
            return ''
    elif  isinstance(s1, (tuple,list)) and isinstance(s2, (tuple,list)):
        return "{} {} {}".format( searchpkclause(s1[0], s1[1],s1[2], pkname) , '' , searchpkclause(s2[0],s2[1],s2[2],pkname))
    elif isinstance(s1, (tuple,list)):
        return "{} {} {}".format( searchpkclause(s1[0],s1[1],s1[2],pkname) , '' , s2)
    elif not s1 and s2:
        return "{} {} ".format(s1 , '' , searchpkclause(s2[0],s2[1],s2[2],pkname))
    elif s1 and not s2:
        return "{} ".format(s1)
    else:
        return "{} {} {}".format(s1 , '' , searchpkclause(s2[0],s2[1],s2[2],pkname))


if __name__ == "__main__":
    sql=('update', ['xiaoqu.xiaoqu_xiaoqu'], [('district_id', 0), ('address', 'testaddr')], {'where': ('=', 'id', '147503'), 'location': 'update.sql:1'})
    print Rule(1246,sql,'mana').run()
