#!/bin/env python
#coding=utf-8

import urllib
import datetime
import logging
import os
import sys
import string


"""发短信"""
def send_sms(msg, phones, sms_gateway='http://sms.dns.ganji.com:20000/WebGate/ShortMsg.aspx'):
    '''
        send short message to phones, no return value(empty string anyway)
    '''
    res = True
    unique_id = 'Tan'
    query_dict = {'opt': 'send',
                  'uniqueId': unique_id,
                  'serviceId': 'bf33195b-2a42-a847-b8d8-351a233a2c87',
                  'phones': phones,
                  'content': msg}
                  #'content': msg.encode('utf8')}
    try:
        query = urllib.urlencode(query_dict)
        url = '%s?%s' % (sms_gateway, query)
        fh = urllib.urlopen(url)
        status = fh.read()
        if status.strip() != '1':
            # print "send_sms failed:", status
            print "send_sms failed: returned status != 1"
    except Exception as ex:
        print 'send sms failed:', ex
        res = False
    return res

"""发邮件"""
def send_mail_http(receiver, body, title=None,
                   sid='dba-alert', email_gateway='http://192.168.127.111:8080/emailservice/postdata'
                   ):
    res = True
    if title is None:
        title = 'warning from dba python'
        title = title +  datetime.datetime.now().strftime(u"%m-%d %H:%M")
    if not body:
        print('empty body, no email sent')
        return False
    post_data = {'data':
                 "{'Sid': '%s', 'Mail': '%s', 'Type': '1', 'Subject': '%s'}"
                 % (sid, receiver, title),
                 'mailbody': '%s' % body}
                 #% (sid, receiver, title.encode('utf-8')),
                 #'mailbody': '%s' % body.encode('utf-8')}
    try:
        fh = urllib.urlopen(email_gateway, data=urllib.urlencode(post_data))
        result = fh.readlines()
        if result != ['result=1']:
            print(u'send failed:%s' % result)
            res = False
        else:
            print(u'send ok:%s' % result)
    except Exception as ex:
        print (u'send fail:', ex)
        res = False
    return res

