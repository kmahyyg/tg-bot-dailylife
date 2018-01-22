#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

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
        return jsonify({'code': 400, 'info': 'Illegal Input!'})
    dbconn = g.db
    dbcur = dbconn.cursor()
    dbcurexec = dbcur.execute('SELECT * FROM USER')
    userinfo = dbcurexec.fetchone()
    while userinfo != None:
        if userinfo[1] == username:
            return jsonify({'code': 200, 'id': userinfo[0], 'name': userinfo[1], 'result': userinfo[2]})
        else:
            userinfo = dbcurexec.fetchone()
    return jsonify({'code': 404, 'info': 'Not found'})


@app.route('/api/deletetel', methods=['DELETE'])
def delete_data():
    username = request.args.get('name')
    if username == None:
        return jsonify({'code': 400, 'info': 'Illegal Input!'})
    dbconn = g.db
    dbcur = dbconn.cursor()
    dropsentence = str("DELETE FROM USER WHERE USER.NAME = " + "\'" + username + "\'")
    dbcur.execute(dropsentence)
    dbconn.commit()
    return jsonify({'code': 200, 'deleted': username})


@app.route('/api/updatetel', methods=['POST'])
def update_data():
    username = request.args.get('name')
    phone = str(int(request.args.get('tel')))
    if (username == None or phone == None):
        return jsonify({'code': 400, 'info': 'Illegal Input!'})
    dbconn = g.db
    dbcur = dbconn.cursor()
    updatesentence = "UPDATE USER SET tel = " + phone + " WHERE USER.name = \'" + username + "\'"
    dbcur.execute(updatesentence)
    dbconn.commit()
    return jsonify({'code': 202, 'updated': username, 'updatetel': phone})


@app.route('/api/uploadtel', methods=['PUT'])
def upload_data():
    username = request.args.get('name')
    phone = str(int(request.args.get('tel')))
    if (username == None or phone == None):
        return jsonify({'code': 400, 'info': 'Illegal Input!'})
    dbconn = g.db
    dbcur = dbconn.cursor()
    lastid = int(((dbcur.execute('SELECT ID FROM USER ORDER BY ID DESC LIMIT 1')).fetchone())[0])
    id = str(lastid + 1)
    uploadsentence = "INSERT INTO USER (id,name,tel) VALUES " + "(" + id + "," + "\'" + username + "\'" + "," + phone + ")"
    dbcur.execute(uploadsentence)
    dbconn.commit()
    return jsonify({'code': 202, 'uploaded': username, 'uploadedtel': phone})


app.run(debug=True)
