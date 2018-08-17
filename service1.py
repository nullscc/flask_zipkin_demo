#!/usr/bin/env python
#-*- coding:utf8 -*-
# Power by null 2018-08-17 16:09:41
import requests
from flask import Flask, request
from py_zipkin.zipkin import zipkin_span,create_http_headers_for_new_span, ZipkinAttrs
import time
from handler import default_handler as http_transport

app = Flask(__name__)

@zipkin_span(service_name='service1', span_name='service1_do_stuff')
def do_stuff():
    time.sleep(5)
    return 'OK'

@app.route('/service1/')
def index():
    print('recieve request in service1', int(time.time()))
    with zipkin_span(
        service_name='service1',
        zipkin_attrs=ZipkinAttrs(
            trace_id=request.headers['X-B3-TraceID'],
            span_id=request.headers['X-B3-SpanID'],
            parent_span_id=request.headers['X-B3-ParentSpanID'],
            flags=request.headers['X-B3-Flags'],
            is_sampled=request.headers['X-B3-Sampled'],
        ),
        span_name='index_service1',
        transport_handler=http_transport,
        port=6000,
        sample_rate=100, #0.05, # Value between 0.0 and 100.0
    ):
        do_stuff()
    print('end request in service1', int(time.time()))
    return 'OK', 200

if __name__=='__main__':
    app.run(host="0.0.0.0",port=6000,debug=True)

