#!/bin/sh
# wrapper start celery
cd /data/mysql/automan && nohup python handler/asynctasks/tasks.py worker --concurrency=32 --loglevel=debug 1>celery.log 2>&1 &
