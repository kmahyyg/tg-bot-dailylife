# !/usr/bin/env python3
# -*- encoding: utf-8 -*-

# API Provider: Aliyun (3rd party)
# API Desc: Check packages from Aliyun
# API Suggested Target: SFEXP only

import json
from time import ctime

import requests

from apikey import appcode

host = 'http://jisukdcx.market.alicloudapi.com'
path = '/express/query'
FILE = open('apibot.log', 'w+')


def packagereq(expno, company='auto'):
    expnO = str(expno)
    company = str(company)
    querys = 'number=' + expnO + '&type=' + company
    headers = {'User-Agent': 'TelegramBOT/v1', 'Accept': 'application/json',
               'Content-Type': "application/json; charset=UTF-8", 'Authorization': appcode}
    url = host + path + '?' + querys
    ruri = requests.get(url=url, headers=headers)
    try:
        response = ruri.json()
        status = int(response['status'])
    except ValueError as e:
        chntime = ctime()
        FILE.write(chntime)
        FILE.write(expnO)
        FILE.write(e)
    FILE.close()
    if (status == 0):
        return response  # requests.response.json returns a list
    elif (status == 201 or status == 202 or status == 203):
        return json.dumps({'code': 404, 'bmsg': 'NOT FOUND COMPANY OR ID.'})
    elif (status == 204):
        return json.dumps({'code': 204, 'bmsg': 'Cannot auto identify company. use \/exp <id> <company> instead.'})
    elif (status == 205):
        return json.dumps({'code': 205, 'bmsg': 'no info'})
    else:
        return json.dumps({'code': 400, 'bmsg': 'Invalid Request'})

# response['result']['list']
# response['status']
# testexpno 1202516705301
# len(response)