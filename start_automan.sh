#!/bin/sh
#wrapper start automan.py
cd /data/mysql/automan && nohup python automan.py 1>automan.log 2>&1 &
