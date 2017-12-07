#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

from flask import Flask, jsonify

app = Flask(__name__)


@app.route('/')
def jsoned():
    return jsonify({'name': 'shit', 'tel': '11111'})


if __name__ == '__main__':
    app.run()
