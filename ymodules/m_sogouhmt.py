#!/usr/bin/env python3
# -*- encoding:utf-8 -*-

import requests
import json
import re

def loads_jsonp(_jsonp):
    try:
        return json.loads(re.match(".*?({.*}).*", _jsonp, re.S).group(1))  # Py2.7 should add param: ensure_ascii=False
    except:
        raise ValueError('Invalid Input')

def usr_subdata(querytel):
    baseurl= 'https://www.sogou.com/reventondc/inner/vrapi?number='
    baseurl_params = '&type=json&callback=show&isSogoDomain=1'
    req_url = baseurl + querytel + baseurl_params
    r = requests.get(req_url)
    return loads_jsonp(r.text)['NumInfo'][8:-2]


def ofc_belonging(querytel):
    if isinstance(querytel,str):
        if querytel[0] == '0':
            return ''
    baseurl = 'https://www.sogou.com/websearch/phoneAddress.jsp?phoneNumber='
    baseurl_params = '&cb=handlenumber&isSogoDomain=1'
    req_url = baseurl + querytel + baseurl_params
    r = requests.get(req_url)
    return r.text[14:-3]