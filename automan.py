#!/usr/local/bin/python
#coding=utf-8
#ganji web db management
#by dongzerun 20140723
#version 0.1.0

import os
from handler.MonRedisHandler import MonRedisHandler
from handler.IndexHandler import IndexHandler
from handler.MonMySQLHandler import MonMySQLHandler
from handler.AutoSqlHandler import AutoSqlHandler
from handler.Http404Handler import Http404Handler
from handler.PriBidHandler import PriBidHandler
from handler.ArchHandler import ArchHandler
from handler.WSHandler import WSHandler
from handler.BackupHandler import BackupHandler
from handler.DelayTaskHandler import DelayTaskHandler
from handler.OffPrivHandler import OffPrivHandler
from handler.ViewHandler import ViewHandler
from handler.utils import consumer
import tornado.ioloop
import tornado.web
import tornado.options
import tcelery
from tornado.options import define, options


if __name__ == "__main__":
    define("port", default=8080, help="run on the given port", type=int)
    define("debug", default=1, help="debug mode", type=int)
    tornado.options.parse_command_line()

    wsset_taskid = {}    
    taskid_wsset = {}
    example = consumer.ExampleConsumer('amqp://guest:guest@localhost:5672/%2F')
    example._wt = wsset_taskid
    example._tw = taskid_wsset

    settings = {
        "static_path" : os.path.join(os.path.dirname(__file__), "static"),
        "template_path" : os.path.join(os.path.dirname(__file__), "view"),
        "gzip" : True,
        "debug" : True,
        "wt" : wsset_taskid,
        "tw" : taskid_wsset,
    }

    handlers = [
        (r'/', IndexHandler),
        (r'/monitor', MonMySQLHandler),
        (r'/monitor/mysql/.*', MonMySQLHandler),
        (r'/monitor/redis/.*', MonRedisHandler),
        (r'/autosql', AutoSqlHandler),
        (r'/autosql/.*', AutoSqlHandler),
        (r'/websocket', WSHandler),
        (r'/delaytask*', DelayTaskHandler),
        (r'/delaytask/.*', DelayTaskHandler),
        (r'/pribid', PriBidHandler),
        (r'/backup', BackupHandler),
        (r'/backup/.*', BackupHandler),
        (r'/offpriv', OffPrivHandler),
        (r'/offpriv/.*', OffPrivHandler),
        (r'/arch', ArchHandler),
        (r'/view/.*', ViewHandler),
        (r'/view', ViewHandler),
        (r'/.*', Http404Handler),
    ]

    app = tornado.web.Application(handlers, **settings)
    tcelery.setup_nonblocking_producer()
    app.listen(options.port)
    ioloop = tornado.ioloop.IOLoop.instance()
    example._connection = example.connect()
    """使rabbitmq的异步consumer能和tornado共用一个ioloop
        正确写法应该是获取current(), anyway 当前代码都对
        example._connection.ioloop = ioloop.current()
    """
    example._connection.ioloop = ioloop

    """为了跟踪性能,记录blocking大于 100ms的堆栈信息"""
    ioloop.current().set_blocking_log_threshold(0.1)

    ioloop.start()
