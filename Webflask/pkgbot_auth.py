#!/usr/bin/env python3
#-*- encoding: utf-8 -*-

class Package(db.Model):
    __tablename__ = 'pkglist'
    pkgid = db.Column(db.Integer,primary_key=True,nullable=False,unique=True)
    pkgstatus = db.Column(db.Integer,nullable=False)
    pkgtrack = db.Column(db.VARCHAR(255))
    tguserid = db.Column(db.VARCHAR(255))

from flask import Flask,request,json,abort,jsonify
from flask_sqlalchemy import SQLAlchemy
from aliyun_exp import packagereq

app=Flask(__name__)
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI']= 'mysql://root:root@localhost:3306/sqlalc?charset=utf8mb4'
db = SQLAlchemy(app)

@app.teardown_appcontext
def shutdown_session(exception=None):
    db.session.remove()


@app.route('/api/checkexp',methods = ['POST'])
def callbgapi():
    expno = request.json.get('express')
    userid = request.json.get('tgid')
    company = request.json.get('company')
    respA = packagereq(expno)


app.run(debug=True)