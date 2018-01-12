#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

import json
import sqlite3

from flask import Flask, jsonify, request, g

app = Flask(__name__)
DATABASE = 'test.db'


def connect_db():
    return sqlite3.connect(DATABASE)


# g.db = get_connection()  for CLI usage
def get_connection():
    db = getattr(g, '_db', None)
    if db is None:
        db = g._db = connect_db()
    return db


@app.before_request
def before_request():
    g.db = connect_db()


@app.teardown_request
def teardown_request(exception):
    if hasattr(g, 'db'):
        g.db.close()


@app.route('/api/checktel', methods=['GET'])
def checkout_data():
    username = request.args.get('name')
    if username == None:
        return jsonify({'code': '400', 'info': 'Illegal Input!'})
    dbconn = g.db
    dbcur = dbconn.cursor()
    dbcurexec = dbcur.execute('SELECT * FROM USER')
    userinfo = dbcurexec.fetchone()
    while userinfo != None:
        if userinfo[1] == username:
            return jsonify({'code': 200, 'result': userinfo[2]})
        else:
            userinfo = dbcurexec.fetchone()
    return jsonify({'code': '404', 'info': 'Not found'})


@app.route('/api/checktel', methods=['DELETE'])
def delete_data():
    record = json.loads(request.data)
    if record == None:
        return jsonify({'code': '400', 'info': 'Illegal Input!'})
    dbconn = g.db
    dbcur = dbconn.cursor()


@app.route('/api/checktel', methods=['POST'])
def update_data():
    username = request.args.get('name')
    if username == None:
        return jsonify({'code': '400', 'info': 'Illegal Input!'})
    dbconn = g.db
    dbcur = dbconn.cursor()


@app.route('/api/checktel', methods=['PUT'])
def upload_data():
    username = request.args.get('name')
    if username == None:
        return jsonify({'code': '400', 'info': 'Illegal Input!'})
    dbconn = g.db
    dbcur = dbconn.cursor()


app.run(debug=True)
