#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

from apikey import sentryid
from raven import Client

client = Client(sentryid)


def sendlog_sent():
    client.capture_exceptions()


def sendlog_my(msg):
    client.captureMessage(msg)
