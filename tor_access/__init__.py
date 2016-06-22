# -*- coding:utf-8 -*-
"""
    author comger@gmail.com
    适合于Tornado 的角色权限模块

    主要功能清单
    1. 权限的自动分组收集
    2. 角色
        a. 支持默认超管角色
        b. 支持代码级的角色管理
        c. 支持数据存储级的角色管理
"""
import os
import traceback
import tornado
from tornado.web import RequestHandler
from tornado.httpclient import HTTPError
from inspect import getmembers

CATEGORY = "默认分组"
ACL = dict()

#节点过滤方法
member_filter = lambda h: isinstance(h, type) and issubclass(h, RequestHandler)

def get_obj_name(obj):
    lst = [obj]
    for item in lst:
        for itemx,itemy in locals().items():
            if item == itemy and itemx != 'item':
                return itemx

class ACLNode(object):
    """
        权限节点
    """
    def __init__(self, handler):
        self.name = '{0}.{1}'.format(handler.__module__, handler.__name__)
        self.intro = handler.__doc__ or self.name
        self.handler = handler


class ACLGroupNode(ACLNode):
    def __init__(self, intro=None, category=None):
        (filename,line_number,function_name,text)=traceback.extract_stack()[-2]
        self.name = '{0}.{1}'.format(filename,text[:text.find('=')].strip())
        self.name = self.name.replace(os.getcwd(),'')
        self.name = self.name.replace('/','.')
        self.name = self.name[1:].replace('.py','')
        self.intro = intro or name
        self.category = category
        self.handlers = []

    def append(self, handler):
        self.handlers.append(handler)

    
    def fetch_module(self, module):
        ACL[CATEGORY][self.name] = self
        for k, v in getmembers(module, member_filter):
            self.append(v)
            v.__checkname__ = self.name
            v.check_access = check_access
            v.__needcheck__ = {'url':True}
    
    def fetch_handlers(self,*handlers):
        ACL[CATEGORY][self.name] = self
        for v in handlers:
            if not member_filter(v): continue

            self.append(v)
            v.__checkname__ = self.name
            v.check_access = check_access
            v.__needcheck__ = {'url':True}
            

class RoleNeed(object):
    """
        角色类型
    """
    def __init__(self, name, intro=None, nodes=set(), ctx_vals={}):
        self.name = name
        self.intro = intro or name

        self.nodes = nodes
        self.ctx_vals = ctx_vals
    
    def require(self, **kwargs):
        def actual(handler):
            assert(issubclass(handler, tornado.web.RequestHandler))
            handler.__needcheck__ = kwargs
            category = kwargs.get('category',CATEGORY)
            if not ACL.get(category,None):ACL[category] = {}


            groupnode = kwargs.get('group', None)

            if groupnode:
                """ 分组权限 """
                ACL[category][groupnode.name] = groupnode
                groupnode.append(handler)
                handler.__checkname__ = groupnode.name
            else:
                aclnode = ACLNode(handler)
                ACL[category][aclnode.name] = aclnode
                handler.__checkname__ = aclnode.name
            

            handler.check_access  = check_access
            return handler
    
        return actual

        

class MasterRoleNeed(RoleNeed):
    def __init__(self):
        self.name = 'master'
        self.intro = u'超级管理员'
        

def check_access(handler, roleneed):
    
    if isinstance(roleneed,MasterRoleNeed):
        return
    
    if not roleneed:
	raise HTTPError(403)

    checkname = handler.__checkname__
    if handler.__needcheck__.get('url',None):
        if not checkname in roleneed.nodes:
            raise HTTPError(403)

    ctx_params = handler.__needcheck__.get('ctx_param',None)
    if ctx_params:
        for ctx_param in ctx_params.split(','):
            ctx_val = handler.get_argument(ctx_param, handler.path_kwargs.get(ctx_param,None))
            if not ctx_val in roleneed.ctx_vals.get(ctx_param,()):
                raise HTTPError(403)


def needcheck(**kwargs):
    """
        权限收集的装饰器
        参数说明：
        url : 当url=True 时, 该Handler 需要进行Url 访问限制；
              只有用户权限里有这个Handler标记时，才有权限访问

        ctx_param: 当需要进行内容参数权限控制,多个内容由','分割
                   如： ctx_param = 'project_id,sensor_type',xx?project_id=A&sensor_type=STR;
                   则访问此Handler 时需要判断用户权限表里project_id 存在A 记录, sensor_type 存在STR记录


        group : 将多个Handler 组成一个权限节点来控制

    """
    def actual(handler):
        assert(issubclass(handler, tornado.web.RequestHandler))
        handler.__needcheck__ = kwargs
        groupnode = kwargs.get('group', None)

        if groupnode:
            """ 分组权限 """
            category = groupnode.category or kwargs.get('category',CATEGORY)
            if not ACL.get(category,None):ACL[category] = {}
            ACL[category][groupnode.name] = groupnode
            groupnode.append(handler)
            handler.__checkname__ = groupnode.name
        else:
            category = kwargs.get('category',CATEGORY)
            if not ACL.get(category,None):ACL[category] = {}
            aclnode = ACLNode(handler)
            ACL[category][aclnode.name] = aclnode
            handler.__checkname__ = aclnode.name
        

        handler.check_access  = check_access
        return handler

    return actual



