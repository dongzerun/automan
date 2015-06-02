#!/bin/env python
#coding=utf-8

import functools
import redis
import time

class RowsGet(object):

    def __init__(self, **kwargs):
        self.conn = redis.Redis(**kwargs)
        self._setversion()

    def _setversion(self):
        """rows_version:统计集息每天4点生成,当前unix时间戳"""
        v = self.conn.get('rows_version')
        if v:
            self.version = int(v)
        else:
            self.version = 0

    def __getattr__(self, cmd):
        if cmd not in self.__dict__:
            self.__dict__[cmd] = functools.partial(self.conn.execute_command, cmd)
        return self.__dict__[cmd]

    def getrows(self, tbname):
        """每次重置时间版本"""
        self._setversion()
        c_ut = int(time.time())
        #大于一天,那么此统计信息不准
        if c_ut - self.version > 86400:
            print c_ut, self.version
            return 1000000
        rows = self.get(tbname)
        if isinstance(rows, str):
            return int(rows)
        else:
            return 1000009
        

if __name__ == "__main__":
    conn = RowsGet(host='yz-log-ku-01', port=8888)
    print "current statics version: ", conn.version
    pricedb = conn.hgetall('price')[::2]
    for db in pricedb:
        pricetb = conn.hgetall('price.' + db)[::2]
        for table in pricetb:
            print 'price.' + db + '.' + table + ' : ', conn.getrows('price.' + db + '.' + table)

    print conn.getrows('ms.wanted_shop_resume')
