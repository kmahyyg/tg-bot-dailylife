"""Receiver module for processing SendGrid Inbound Parse messages.

See README.txt for usage instructions."""
import json

try:
    from config import Config
except:
    # Python 3+, Travis
    from sendgrid.helpers.inbound.config import Config

try:
    from parse import Parse
except:
    # Python 3+, Travis
    from sendgrid.helpers.inbound.parse import Parse

from flask import Flask, request, render_template, jsonify
import os

app = Flask(__name__)
config = Config()
YYGFile = open('/tmp/recvmails_yyg.dat', 'w+')
ECSFile = open('/tmp/recvmails_ecs.dat', 'w+')
SpamFile = open('/tmp/recvmails_idk.dat', 'w+')

@app.route('/', methods=['GET'])
@app.route('/recvsg', methods=['GET'])
def index():
    """Show index page to confirm that server is running."""
    return render_template('index.html')


@app.route(config.endpoint, methods=['POST'])
def inbound_parse():
    """Process POST from Inbound Parse and save received data."""
    parse = Parse(config, request)
    # Sample proccessing action
    updata = parse.key_values()
    if ("kmahyyg" in updata['to']):
        yygdata = json.dumps(updata)
        YYGFile.write(yygdata)
        YYGFile.close()
    elif ("ecswvern" in updata['to']):
        ecsdata = json.dumps(updata)
        ECSFile.write(ecsdata)
        ECSFile.close()
    else:
        spamdata = json.dumps(updata)
        SpamFile.write(spamdata)
        SpamFile.close()
    # Tell SendGrid's Inbound Parse to stop sending POSTs
    # Everything is 200 OK :)
    # Now send the corresponding file to each chat id
    return jsonify({'status': 200, 'bmsg': 'OK'})


if __name__ == '__main__':
    # Be sure to set config.debug_mode to False in production
    port = int(os.environ.get("PORT", config.port))
    if port != config.port:
        config.debug = False
    app.run(host='0.0.0.0', debug=config.debug_mode, port=port)
