#!/usr/bin/env python3.6
# -*- encoding: utf-8 -*-

from secrets import token_urlsafe as urltoken

from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from passlib.apps import custom_app_context as pwd_context

app = Flask(__name__)
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost:3306/sqlalc?charset=utf8mb4'
db = SQLAlchemy(app)


@app.teardown_appcontext
def shutdown_session(exception=None):
    db.session.remove()


class User(db.Model):
    __tablename__ = 'userlist'
    id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True, index=True)
    tgid = db.Column(db.BIGINT, nullable=True, unique=True)
    username = db.Column(db.VARCHAR(255), unique=True)
    tele = db.Column(db.VARCHAR(255), unique=True, nullable=True)
    passhash = db.Column(db.VARCHAR(255), unique=True)

    def hash_pass(self, password):
        self.passhash = pwd_context.encrypt(password)

    def verify_pass(self, password):
        return pwd_context.verify(password, self.passhash)

    def gen_token(self):
        self.passhash = urltoken(12)


class Package(db.Model):
    __tablename__ = 'pkglist'
    pkgid = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    pkgstatus = db.Column(db.Integer, nullable=False)
    pkgtrack = db.Column(db.VARCHAR(255))
    tguserid = db.Column(db.VARCHAR(255))


@app.route('/api/appreg', methods=['POST'])
def new_app():
    appname = request.json.get('name')
    telep = request.json.get('phone')
    if (appname == None):
        abort(400, 'application\'s name is not submitted.')
    if ((User.query.filter_by(username=appname).first()) is not None):
        abort(400, 'APP already existed.')
    app = User(username=appname, tele=telep)
    app.gen_token()
    db.session.add(app)
    db.session.commit()
    return jsonify({'code': 201, 'appname': app.username, 'token': app.passhash, 'recovery': app.tele, 'id': app.id})


@app.route('/api/userreg', methods=['POST'])
def new_user():
    username = request.json.get('username')
    password = request.json.get('password')
    telep = request.json.get('tele')
    if (username == None or password == None or telep == None):
        abort(400, 'Invalid Request. The content in your request is not usable.')
    if ((User.query.filter_by(username=username).first()) is not None):
        abort(400, 'User already Existed.')
    user = User(username=username, tele=telep)
    user.hash_pass(password)
    db.session.add(user)
    db.session.commit()
    return jsonify(
        {'code': 201, 'username': user.username, 'password': password, 'RecCredential': user.tele, 'id': user.id})


@app.route('/api/resetkey', methods=['POST'])
def reset_key():
    username = request.json.get('username')
    resetkey = request.json.get('newpassw')
    telep = request.json.get('tel')
    if (username == None or telep == None or resetkey == None):
        abort(400, 'Invalid Request. The content in your request is not usable.')
    if ((User.query.filter_by(username=username).first()).tele == telep):
        user = User(username=username)
        resetuser = User.query.filter_by(username=username).first()
        resetuser.passhash = user.hash_pass(resetkey)
        # setattr(user, 'no_of_logins', user.no_of_logins+1)
        db.session.commit()
        return jsonify({'code': 203, 'reset': resetkey, 'name': user.username})
    else:
        abort(400, 'User already Existed.')


@app.route('/api/bindtel', methods=['POST'])
def bindtel():
    username = request.json.get('name')
    password = request.json.get('password')
    telep = request.json.get('tele')
    if (username == None or password == None):
        abort(400, 'Invalid Request.')
    if ((User.query.filter_by(username=username).first()).tele is not None): \
            abort(403, 'Forbidden. Telephone already binded.')
    user = User(username=username)
    if (user.hash_pass(password) == True):
        binduser = User.query.filter_by(username=username).first()
        binduser.tele = telep
        db.session.commit()
        return jsonify({'code': 202, 'msg': 'done'})

# app.run(debug=True)
