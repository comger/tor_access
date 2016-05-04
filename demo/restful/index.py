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


from tornado import gen
from kpages import url, ContextHandler, LogicContext, get_context, service_async

aclgroup = tor_access.ACLGroupNode('userdemo',u'系统管理')

class AccessHandler(tornado.web.RequestHandler):
    def prepare(self):
        mrn = tor_access.MasterRoleNeed()
        ctx_vals = dict(pid=['A','B'],mid=('MA','Mb'))
        rn = tor_access.RoleNeed('abcrole',intro=u'普通角色',
            nodes=set(['restful.index.IndexHandler','userdemo']),
            ctx_vals=ctx_vals)
        self.check_access(rn)


@tor_access.needcheck(url=True, group=aclgroup)
@url(r"/")
class IndexHandler(AccessHandler):
    def get(self):
        print tor_access.ACL 
        self.write('hello world')


@tor_access.needcheck(url=True, group=aclgroup, ctx_param='pid,mid')
@url(r"/abc")
class ABCHandler(AccessHandler):
    def get(self):
        self.write('abc')


@tor_access.needcheck(url=True)
@url(r"/abcd")
class ABCDHandler(AccessHandler):
    def get(self):
        self.write('abcd')

@tor_access.needcheck(url=True,category=u'新分组')
@url(r"/abcde")
class ABCDEHandler(AccessHandler):
    def get(self):
        self.write('abcde')
