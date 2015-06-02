#!/bin/env python
#coding=utf-8
#by dongzerun
#celery task async for automan

import pika
import time
import json
import sys
sys.path.append("/data/mysql/automan/handler")
from asynctasks.autosql import AutoSql
from celery import Celery
from kombu import Exchange, Queue


celery = Celery('tasks', broker='amqp://localhost')
celery.conf.CELERY_RESULT_BACKEND = 'amqp://localhost'
celery.conf.update(
        CELERY_DEFAULT_QUEUE = 'default',
        CELERY_IGNORE_RESULT = True,
        CELERY_QUEUES = (
            Queue('default', Exchange('default'), routing_key='default'),
            Queue('for_task_sleep', Exchange('for_task_sleep'), routing_key='for_task_sleep'),
            Queue('for_task_wait', Exchange('for_task_wait'), routing_key='for_task_wait'),
            Queue('for_submittask', Exchange('for_submittask'), routing_key='for_submittask'),
            Queue('for_delaytask', Exchange('for_delaytask'), routing_key='for_delaytask'),
        ),
        CELERY_ROUTES = {
            'sleep': {'queue': 'for_task_sleep', 'routing_key': 'for_task_sleep'},
            'wait': {'queue': 'for_task_wait', 'routing_key': 'for_task_wait'},
            'delaytask': {'queue': 'for_delaytask', 'routing_key': 'for_delaytask'},
        },
        CELERY_IMPORTS=('handler.asynctasks.tasks',)
)

@celery.task
def sleep(seconds):
    time.sleep(float(seconds))
    return seconds

@celery.task
def wait(seconds):
    time.sleep(float(seconds))
    return seconds

@celery.task
def savefile(filename, data):
    if filename:
        filepath = '/tmp/' + filename
        with open(filepath, 'wb') as up:
            up.write(data)
            up.seek(0)
            up.close()
        return filepath
    else:
        print "file name empty"
        return None

@celery.task
def delaytask(task_id,classes,delay=False,ignoresteps=[]):
    time.sleep(1)
    print "in delaytask: ", task_id, classes, delay, ignoresteps
    AutoSql(task_id, classes, delay,ignoresteps).run()
 
@celery.task
def submittask(task_id,classes,delay=False,ignoresteps=[]):
    time.sleep(1)
    print "in submittask: ", task_id, classes, delay, ignoresteps
    AutoSql(task_id, classes, delay,ignoresteps).run()
 
@celery.task
def auto_simple():
    time.sleep(4)

@celery.task
def auto_complex():
    time.sleep(10)

if __name__ == "__main__":
    celery.start()
