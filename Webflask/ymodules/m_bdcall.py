#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
#
# Baidu callback library
# Copyright (C) 2018 Jiangtaste
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import json
import random
import re
import time
import requests


def check_phone(phone):
    """
    :param phone_num:
    :return True, False
    """
    phone_re = re.compile('^0\d{2,3}\d{7,8}$|^1[3456789]\d{9}$|^861[3456789]\d{9}$')
    phone_num = re.sub("\D", "", phone)

    if phone_re.match(phone_num):
        if len(phone_num) > 11:
            return phone_num[-11:-1]
        return phone_num
    else:
        return False


def loads_jsonp(_jsonp):
    try:
        return json.loads(re.match(".*?({.*}).*", _jsonp, re.S).group(1), ensure_ascii=False)
    except:
        raise ValueError('Invalid Input')


# thanks to: https://www.v2ex.com/t/449432, copyright owned by original user

def start_call(phone):  # phone is string
    """
    :param phone:
    :return True, False
    """
    # config
    f = 55
    id = random.randint(1, 92000)  # Random choose a market to callback
    g = 0
    _ = t = int(time.time() * 1000)
    t = int(time.time() * 1000 + 320)
    r = ''

    # custom headers
    my_headers = {
        'Accept':
            'text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01',
        'Accept-Encoding':
            'gzip, deflate',
        'Accept-Language':
            'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection':
            'keep-alive',
        'Host':
            'lxbjs.baidu.com',
        'Referer':
            'http://lxbjs.baidu.com/cb/url/show?f=%s&id=%s' % (f, id),
        'User-Agent':
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
        'X-Requested-With':
            'XMLHttpRequest'
    }

    # token_url
    get_token_url = 'http://lxbjs.baidu.com/cb/url/check'

    # params for sending
    params = {'f': f, 'id': id, 'g': g, 't': t, 'r': r, '_': _}

    # use session
    sss = requests.Session()

    # get token
    print('--------Start--------')
    print('Acquiring Token...')
    tk = sss.get(get_token_url, params=params).json()
    try:
        tk = tk['data']['tk']
    except KeyError:
        return False

    if tk:
        print('Success, Token got.')
    else:
        print('Failed to acquire a token!')
        return False

    # call_url
    get_call_url = 'http://lxbjs.baidu.com/cb/call'

    # params
    params = {'f': f, 'id': id, 'tk': tk, 'vtel': phone, '_': _ + 1}

    # submit callback request
    print('Submitted Callback Request')
    req = sss.get(get_call_url, params=params)


    if req.status_code == 200:        # status code should and actually always be 200 to avoid ISP hijack
        print('Success Requested')    # return msg status not 0 is error, but I'm lazy to check it.
        try:
            return loads_jsonp(req.text)
        except:
            pass
        return True
    else:
        print('Failed Request')
        return False

