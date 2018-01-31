#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

# Next we are going to use webhook to parse inbound mail
# we need flask to deal with this

from flask import Flask, request
import simplejson

app = Flask(__name__)


@app.route('/recvsg', methods=['POST'])
def inboundmail():
    # Consume the entire email
    envelope = simplejson.loads(request.form.get('envelope'))

    # Get some header information
    to_address = envelope['to'][0]
    from_address = envelope['from']

    # Now, onto the body
    text = request.form.get('text')
    html = request.form.get('html')
    subject = request.form.get('subject')

    # Process the attachements, if any
    num_attachments = int(request.form.get('attachments', 0))
    attachments = []
    if num_attachments > 0:
        for num in range(1, (num_attachments + 1)):
            attachment = request.files.get(('attachment % d' % num))
            attachments.append(attachment.read())


app.run(debug=True)
