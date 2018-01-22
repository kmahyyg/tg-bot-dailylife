#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

import json

from flask import Flask, jsonify, request

# curl -H 'Content-Type: application/json' -X POST/DELETE/PUT/GET -d '{"name":"yyg2","tel":"111211"}'
# http://127.0.0.1:5000


app = Flask(__name__)


@app.route('/', methods=['GET'])
def query_records():
    name = request.args.get('name')
    print(name)
    with open('data.txt', 'r') as f:
        data = f.read()
        records = json.loads(data)
        for record in records:
            if record['name'] == name:
                return jsonify(record)
        return jsonify({'code': 404, 'data': 'not found'})


@app.route('/', methods=['PUT'])
def create_record():
    record = json.loads(request.data)
    with open('data.txt', 'r') as f:
        data = f.read()

    if not data:
        records = [record]
    else:
        records = json.loads(data)
        records.append(record)

    with open("data.txt", 'w') as f:
        f.write(json.dumps(records, indent=2))
    return jsonify({'code': 200, 'uploaded': record})


@app.route('/', methods=['POST'])
def update_record():
    record = json.loads(request.data)
    new_records = []
    with open('data.txt', 'r') as f:
        data = f.read()
        records = json.loads(data)

    for r in records:
        if r['name'] == record['name']:
            r['tel'] = record['tel']
        new_records.append(r)

    with open('data.txt', 'w') as f:
        f.write(json.dumps(new_records, indent=2))
    return jsonify({'code': 202, 'updated': record})


@app.route('/', methods=['DELETE'])
def delete_record():
    record = json.loads(request.data)
    new_records = []
    with open('data.txt', 'r') as f:
        data = f.read()
        records = json.loads(data)
        for r in records:
            if r['name'] == record['name']:
                continue
            new_records.append(r)

    with open('data.txt', 'w') as f:
        f.write(json.dumps(new_records, indent=2))

    return jsonify({'code': 200, 'deleted': records[0]})


app.run(debug=True)
