#!/usr/bin/env python
#-*- coding:utf8 -*-
# Power by null 2018-08-17 16:07:29
import requests
from flask import Flask
from py_zipkin.zipkin import zipkin_span,create_http_headers_for_new_span
import time
from handler import default_handler as http_transport

app = Flask(__name__)

@zipkin_span(service_name='webapp', span_name='do_stuff')
def do_stuff():
    time.sleep(5)
    headers = create_http_headers_for_new_span()
    requests.get('http://localhost:6000/service1/', headers=headers)
    return 'OK'

@app.route('/')
def index():
    print('recieve request in demo', int(time.time()))
    with zipkin_span(
        service_name='webapp',
        span_name='index',
        transport_handler=http_transport,
        port=5000,
        sample_rate=100, #0.05, # Value between 0.0 and 100.0
    ):
        do_stuff()
        time.sleep(10)
    print('end request in demo', int(time.time()))
    return 'OK', 200

if __name__=='__main__':
    app.run(host="0.0.0.0",port=5005,debug=True)

