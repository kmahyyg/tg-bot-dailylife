#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

import json

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

from aliyun_exp import packagereq

app = Flask(__name__)
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost:3306/sqlalc?charset=utf8mb4'
db = SQLAlchemy(app)


class Package(db.Model):
    __tablename__ = 'pkglist'
    pkgid = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    pkgstatus = db.Column(db.Integer, nullable=False)
    pkgtrack = db.Column(db.VARCHAR(255))
    tguserid = db.Column(db.VARCHAR(255))


@app.teardown_appcontext
def shutdown_session(exception=None):
    db.session.remove()


@app.route('/api/checkexp', methods=['POST'])
def callpkgapi():
    expno = request.json.get('express')
    userid = request.json.get('tgid')
    company = request.json.get('company')
    respA = packagereq(expno, company)
    if (isinstance(respA, str)):
        msg = json.loads(respA)
        return respA
    companyrep = respA['result']['type']
    pkgstat = respA['result']['deliverystatus']
    package = Package(pkgid=expno, pkgstatus=pkgstat, pkgtrack=respA['result']['list'][0], tguserid=userid)
    if (pkgstat is not 3):
        if (Package.query.filter_by(pkgid=expno).first() is not None):
            package.pkgtrack = respA['result']['list'][0]
            db.session.commit()
        else:
            db.session.add(package)
            db.session.commit()
        return jsonify({'id': expno, 'stat': pkgstat, 'track': package.pkgtrack})
    else:
        db.session.delete(package)
        return jsonify({'code': 400, 'bmsg': 'The package is already received by user.'})


@app.route('/api/check2user', methods=['GET'])
def checkbyuser():
    userid = request.json.get('tgid')
    usersql = Package.query.filter_by(tguserid=userid).first()
    while (usersql is not None):
        return jsonify()


app.run(debug=True)
