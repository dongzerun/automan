#!/bin/sh
ps aux | grep -i automan | grep -iv grep | awk '{print $2}' | xargs  kill -9
