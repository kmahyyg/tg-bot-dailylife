#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

# API Provider: Aliyun (3rd party)
# API Desc: Check packages from Aliyun
# API Suggested Target: SFEXP only

import json
from time import ctime

import requests

from apikey import appcode

host = 'https://wuliu.market.alicloudapi.com'
path = '/kdi'
FILE = open('alipkgbot.log', 'w+')


def packagereq(expno, company='auto'):
    expnO = str(expno)
    company = str(company)
    querys = 'no=' + expnO + '&type=' + company
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
    elif (status == 204 or status == 207):
        return json.dumps({'code': 204, 'bmsg': 'Cannot auto identify company. use \/exp <id> <company> instead.'})
    elif (status == 205):
        return json.dumps({'code': 205, 'bmsg': 'no info'})
    else:
        return json.dumps({'code': 400, 'bmsg': 'Invalid Request'})

# finalrep = response['result']['list'][0]
# response['result']['deliverystatus']  1-OnTheWay 2-Delivering 3-Received 4-Failed
# {'status': '0', 'msg': 'ok', 'result': {'number': '1202516705301', 'type': 'yunda', 'list': [{'time': '2017-01-16 14:55:00', 'status': '广东深圳公司宝安后瑞分部快件已被 已签收 签收'}, {'time': '2017-01-16 14:49:05', 'status': '广东深圳公司宝安后瑞分部进行派件扫描；派送业务员：苏东缘；联系电话：15323423918'}, {'time': '2017-01-16 07:40:46', 'status': '广东深圳公司宝安区分拨分部进行快件扫描，将发往：广东深圳公司宝安后瑞分部'}, {'time': '2017-01-15 23:53:28', 'status': '广东深圳公司进行快件扫描，将发往：广东深圳公司宝安区分拨分部'}, {'time': '2017-01-15 23:40:20', 'status': '广东深圳公司在分拨中心进行卸车扫描'}, {'time': '2017-01-14 22:37:46', 'status': '浙江杭州分拨中心进行装车扫描，即将发往：广东深圳公司'}, {'time': '2017-01-14 22:36:08', 'status': '浙江杭州分拨中心在分拨中心进行称重扫描'}, {'time': '2017-01-14 20:43:59', 'status': '浙江主城区公司杭州下城区凤起路服务部进行揽件扫描'}, {'time': '2017-01-14 20:42:29', 'status': '浙江主城区公司杭州下城区凤起路服务部进行下级地点扫描，将发往：广东深圳公司'}, {'time': '2017-01-14 18:50:03', 'status': '浙江主城区公司杭州下城区凤起路服务部进行揽件扫描'}], 'deliverystatus': '3', 'issign': '1'}}
# response['result']['list']
# response['status']
# testexpno 1202516705301
# len(response)
