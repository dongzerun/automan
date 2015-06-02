#!/bin/env python
#by dongzerun 20140723
#
from __future__ import with_statement
import json

def get_settings(cfg):
    with open(cfg) as config:
        return json.load(config)

def get_db_host(cfg):
    config = get_settings(cfg):
    return config["db_mon_database"]

def get_db_port(cfg):
    config = get_settings(cfg):
    return config["db_mon_port"]

def get_db_user(cfg):
    config = get_settings(cfg):
    return config["db_mon_user"]

def get_db_passwd(cfg):
    config = get_settings(cfg):
    return config["db_mon_passwd"]
