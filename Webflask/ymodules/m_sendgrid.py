#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

import magic
import sendgrid

from apikey import sgridkey


# helpers.mail helps us build a personalization object to send a customized mail
# according to SendGrid tutorial,  Whole requests should not exceed 20M
# it strongly suggests that 7M is the biggest size of attachments.

# def detectsize(filedir):
#     orisize = os.path.getsize(filedir)
#     realsize = orisize / 1024 / 1024
#     return realsize
#
# Already proceeded in frontend

# cuz libmagic doesn't exist in Windows Platform
# if you need it to be running on Win
# use python-magic with python-magic-win64 instead
# https://github.com/axnsan12/python-magic-win64
# from winmagic import magic
# Here I just need it to be running on Linux. #

def getmime(file):
    mime = magic.Magic(mime=True)
    mimetp = mime.from_file(file)
    return mimetp


def sendmail(mailjson):
    sg = sendgrid.SendGridAPIClient(apikey=sgridkey)
