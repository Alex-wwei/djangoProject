#coding=utf-8
from django.test import TestCase

# Create your tests here.
import redis

# r = redis.StrictRedis(host='localhost', port=6379)
#
# # r.set('wang', 'wei')
# r.setex('w', 10, 'wei')
#
# print(r.get('wang'), type(r.get('wang').decode()), type(r.get('w')), r.get('w'))


s = '1'

l = [5,3,6,2,7]
p = l.pop()

print(s.split(';'), p , l)

from datetime import datetime
now = datetime.now()
s = now.strftime('%Y%m%d%H%M%S')
print(now, s, type(s))

import os, subprocess
print(os.path.basename(__file__),  os.path.abspath(__file__), os.getcwd())
print(os.path.dirname(__file__), os.path.getsize(__file__), os.stat(__file__).st_size,os.stat(__file__))
print(os.listdir(os.getcwd()),os.popen('ls ..').read(), os.system('ls ..'))
print()
print(subprocess.getoutput('ls tests.py'))