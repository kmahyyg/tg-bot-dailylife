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
STORAGEFILE = open('recvmails.dat', 'w+')

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
    saveddata = json.dumps(updata)
    STORAGEFILE.write(saveddata)
    STORAGEFILE.close()
    # Tell SendGrid's Inbound Parse to stop sending POSTs
    # Everything is 200 OK :)
    return jsonify({'status': 200, 'bmsg': 'OK'})


if __name__ == '__main__':
    # Be sure to set config.debug_mode to False in production
    port = int(os.environ.get("PORT", config.port))
    if port != config.port:
        config.debug = False
    app.run(host='0.0.0.0', debug=config.debug_mode, port=port)
