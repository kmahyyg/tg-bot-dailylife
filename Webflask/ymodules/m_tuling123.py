#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

from apikey import tulingkey

# thanks to  https://github.com/bennythink/expressbot

# Turing robot, requires TURING_KEY in config.py
__author__ = 'kmahyyg <16604643+kmahyyg@users.noreply.github.com>'

import json
import requests
import urllib3


def send_turing(info, userid, key=tulingkey):
    """
    send request to Turing robot, and get a response
    :param key: TURING_KEY
    :param info: the message from user
    :param userid: chat_id, for context parse
    :return: response from Turing Bot, in text.
    """

    data = {
        "key": key,
        "info": info,
        "userid": userid
    }

    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    url = 'https://www.tuling123.com/openapi/api'
    result = requests.post(url, json=data, verify=False).text
    return json.loads(result).get('text')


if __name__ == '__main__':
    pass
