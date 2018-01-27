#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

import json

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

from aliyunexp_bn import packagereq

app = Flask(__name__)
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost:3306/sqlalc?charset=utf8mb4'
db = SQLAlchemy(app)


class Package(db.Model):
    __tablename__ = 'pkglist'
    pkgid = db.Column(db.VARCHAR(32), primary_key=True, nullable=False, unique=True)
    pkgstatus = db.Column(db.Integer, nullable=False)
    pkgtrack = db.Column(db.VARCHAR(255))
    tguserid = db.Column(db.VARCHAR(32))

    def __init__(self, pkgid, pkgstatus, pkgtrack, tguserid):
        self.pkgid = pkgid
        self.pkgstatus = pkgstatus
        self.pkgtrack = pkgtrack
        self.tguserid = tguserid

    def __repr__(self):
        result = {'pkgid': self.pkgid, 'pkgstatus': self.pkgstatus, 'pkgtrack': self.pkgtrack,
                  'tguserid': self.tguserid}
        return json.dumps(result)

@app.teardown_appcontext
def shutdown_session(exception=None):
    db.session.commit()
    db.session.remove()


@app.route('/api/aliyun/checkexp', methods=['POST'])
def callpkgapi():
    expno = request.json.get('express')
    userid = request.json.get('tgid')
    company = request.json.get('company')
    respA = packagereq(expno, company)
    if (isinstance(respA, str)):
        msg = json.loads(respA)
        return respA
    companyrep = respA['result']['type']
    pkgtrack = respA['result']['list'][0]
    pkgstat = respA['result']['deliverystatus']
    package = Package(pkgid=expno, pkgstatus=pkgstat, pkgtrack=pkgtrack, tguserid=userid)
    if (pkgstat is not 3):
        if (Package.query.filter_by(pkgid=expno).first() is not None):
            package.pkgtrack = respA['result']['list'][0]
            db.session.commit()
        else:
            db.session.add(package)
            db.session.commit()
        return jsonify({'id': expno, 'stat': pkgstat, 'track': pkgtrack})
    else:
        db.session.delete(package)
        return jsonify({'code': 400, 'bmsg': 'The package is already received by user.'})


@app.route('/api/kd100/checkpkg', methods=['GET'])
def callkd100():



@app.route('/api/check2user', methods=['GET'])
def checkbyuser():
    userid = request.json.get('tgid')
    usersql = Package.query.filter_by(tguserid=userid).all()
    pkgall = []
    if (usersql is not None):
        leng = len(usersql)
        for i in range(0, leng):
            pkg = str(usersql[i])
            pkgall.append(pkg)
        return jsonify({'code': 200, 'pkg': pkgall})
    else:
        return jsonify({'code': 404, 'bmsg': 'not found'})


app.run(debug=True)
