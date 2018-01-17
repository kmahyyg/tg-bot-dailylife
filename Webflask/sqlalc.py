#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

# import modules
from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

# flask config
app = Flask(__name__)
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

# db config
engine = create_engine('mysql://root@root:localhost:3306/sqlalc?charset=utf8mb4',convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=True,autoflush=False,bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()
metadata = Metadata(bind=engine)

# db initialize
from sqlalchemy import Column, Integer, VARCHAR


class User(Base):
    __tablename__ = 'userlist'
    id = Column(Integer,primary_key=True,nullable=False)
    username = Column(VARCHAR(255), unique=True)
    tele = Column(VARCHAR(255), unique=True)

    def __init__(self,username=None,tele=None):
        self.username = username
        self.tele = tele

    def __repr__(self):
        return [self.username,self.tele]

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

@app.route('/api/checktel',methods=['GET'])
def checkout():


@app.route('/api/updatetel',methods=['POST'])
def updatetel():


@app.route('/api/uploadtel',methods=['PUT'])
def uploadtel():

@app.route('/api/deletedel',methods=['DELETE'])
def deltel():



app.run(debug=True)