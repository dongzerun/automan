#!/usr/local/bin/python
#coding=utf-8
import time
import socket
import sys
import urllib
import urllib2
import datetime
import json


def send_mail_http(receiver,body, title=None,sid='dba-alert', email_gateway='http://edmpost.dns.ganji.com:8080/emailservice/postdata'):
    res = True
    if title is None:
        title = 'warning from dba python'
        title = title 
        print title, type(title)
    if not body:
        print('empty body, no email sent')
        return False
    print type(title)

    post_data = "data={\"Mail\":\"%s\",\"Sid\":\"%s\",\"Type\":\"1\",\"Subject\":\"%s\"}&mailbody=\"%s\"" % (receiver, sid, str(title).decode('utf8'), str(body).decode('utf8'))
    try:
        req = urllib2.Request(email_gateway, post_data.encode('utf8'))
        res = urllib2.urlopen(req)
        result = res.read()
        if result != 'result=1':
            print(u'send failed:%s' % result)
            res = False
        else:
            print(u'send ok:%s' % result)
        return True
    except Exception as ex:
        print (u'send fail:', ex)
        res = False
    return res    

def sendmailbyuser(name):
    content = """您线下库权限申核通过,请查看 <a href="http://automan.corp.ganji.com/offpriv/getoffbyuser"><U><strong>我的线下库</strong></U></a>"""
    user= name + "@ganji.com"
    send_mail_http(user, content, 'automan线下库权限申请通过')

def sendmailtoleader(name):
    content = """您有新的线下库权限审核,请查看 <a href="http://automan.corp.ganji.com/offpriv"><U><strong>automan</strong></U></a>"""
    user= name + "@ganji.com"
    send_mail_http(user, content, 'automan线下库权限申请')

if __name__ == "__main__":
    sendmailtoleader('dongzerun')
    sendmailbyuser('dongzerun')
