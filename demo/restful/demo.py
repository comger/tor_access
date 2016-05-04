# -*- coding:utf-8 -*-
"""
    index action demo
    author comger@gmail.com
"""
import tornado
try:
    import tor_access
except:
    import sys
    sys.path.append('..')
    import tor_access

from kpages import url
from index import aclgroup,AccessHandler


@tor_access.needcheck(url=True, group=aclgroup)
@url(r"/f")
class IndexFHandler(AccessHandler):
    def get(self):
        print aclgroup.handlers 
        self.write('hello world')


@tor_access.needcheck(url=True, group=aclgroup,ctx_param='pid')
@url(r"/fabc")
class ABCFHandler(AccessHandler):
    def get(self):
        self.write('abc')


@tor_access.needcheck(url=True)
@url(r"/fabcd")
class ABCDFHandler(AccessHandler):
    def get(self):
        self.write('abcd')

@tor_access.needcheck(url=True,category=u'新分组')
@url(r"/fabcde")
class ABCDEFHandler(AccessHandler):
    def get(self):
        self.write('abcde')
