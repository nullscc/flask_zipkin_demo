import requests
import time

def default_handler(encoded_span):
    #body = str.encode('\x0c\x00\x00\x00\x01') + encoded_span
    print('post to  zipkin in default_handler', int(time.time()))
    return requests.post(
        #self.app.config.get('ZIPKIN_DSN'),
        "http://127.0.0.1:9411/api/v1/spans",
        data=encoded_span,
        headers={'Content-Type': 'application/x-thrift'},
    )
