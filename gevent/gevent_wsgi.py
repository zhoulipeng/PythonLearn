from gevent import monkey
from gevent.pywsgi import *

monkey.patch_all()


def app(env, start_response):
    start_response('200 OK', [('Content-Type', 'text/html')])
    return ['<html><head><title>AB Test</title></head><body><h1>Hello</h1></body></html>']


print('Start gevent 9999...')
WSGIServer(('localhost', 9999), app).serve_forever()
"""
$ ab -n 10000 -c 1000 -k http://localhost:9999/
...
Concurrency Level:      1000
Time taken for tests:   4.514 seconds
Complete requests:      10000
Failed requests:        0
Write errors:           0
Total transferred:      1900000 bytes
HTML transferred:       750000 bytes
Requests per second:    2215.36 [#/sec] (mean)
Time per request:       451.393 [ms] (mean)
Time per request:       0.451 [ms] (mean, across all concurrent requests)
Transfer rate:          411.05 [Kbytes/sec] received
Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        0  105 350.3      9    3029
Processing:    71  165  81.3    145    1747
Waiting:       67  161  81.2    142    1744
Total:         88  270 383.4    152    3395

Percentage of the requests served within a certain time (ms)
  50%    152
  66%    165
  75%    176
  80%    205
  90%    353
  95%   1158
  98%   1407
  99%   1880
 100%   3395 (longest request)
 """
