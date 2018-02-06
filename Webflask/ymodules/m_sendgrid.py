#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

import base64
import json
import magic
import os
import sendgrid
from sendgrid.helpers.mail import *

from apikey import sgridkey


# helpers.mail helps us build a personalization object to send a customized mail
# according to SendGrid tutorial,  Whole requests should not exceed 20M
# it strongly suggests that 7M is the biggest size of attachments.

def detectsize(filedir):
    orisize = os.path.getsize(filedir)
    realsize = orisize / 1024 / 1024
    return realsize


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
    dictsg = json.loads(mailjson)
    from_mail = Email(dictsg['from'])
    to_mail = Email(dictsg['tomail'])
    subject = dictsg['subject']
    if dictsg['mimetxt'] == 'text/plain':
        content = Content("text/plain", dictsg['textcont'])
    elif dictsg['mimetxt'] == 'text/html':
        content = Content("text/html", dictsg['textcont'])
    else:
        return json.dumps({'status': 400, 'bmsg': 'Invalid Request.'})
    if dictsg['hasfile'] == True:
        filedir = dictsg['filedir']
        filename = dictsg['filenm']
        mailconstruct = Mail(from_mail, subject, to_mail, content)
        with open(filedir, "rb") as f1:
            datamime = getmime(f1)
            dataattc = f1.read()
            f1.close()
        encoded = base64.b64encode(dataattc)
        attach = Attachment()
        attach.set_content(encoded)
        attach.set_type(datamime)
        attach.set_filename(filename)
        attach.set_disposition("attachment")
        attach.set_content_id(255)
        mailconstruct.add_attachment(attach)
    response = sg.client.mail.send.post(request_body=mail.post())
    rep = {}
    rep['code'] = response.status_code
    rep['bmsg'] = response.body
    rep['head'] = response.headers
    return rep
