#!/usr/bin/env python3
#-*- encoding: utf-8 -*-

# 3rd party API : KD100
# http://www.kuaidi100.com/autonumber/autoComNum?resultv2=1&text= <EXP CODE>  [POST]
# http://www.kuaidi100.com/query?type= <COMPANY CODE> &postid= <EXP CODE>  [GET]

# POST : resp['auto'][0]['comCode']
# raise IndexError (None Array)

# GET: pkgresp['data'][0]['context']
# check if pkgresp['status'] == 200, else is error

# kd100_company.json http://www.kuaidi100.com/js/share/company.js
