tor_access
==========

Tornado access lib for user role 


## How to collect access node in tornado
```
import tor_access

@tor_access.needcheck(url=True)
class IndexHandler(tornado.web.RequestHandler):
	def get(self):
		pass



aclgroup = tor_access.ACLGroupNode('userdemo',u'系统管理')

@tor_access.needcheck(url=True, group=aclgroup)
class UserHandler(tornado.web.RequestHandler):
	def get(self):
		pass



@tor_access.needcheck(url=True, category='categroyname')
class UserInfoHandler(tornado.web.RequestHandler):
	def get(self):
		pass


OR: aclgroup.fetch_handlers(UserHandler,UserInfoHandler) to add access node 
```


## How to get  access node
```
import tor_access

acl = tor_access.ACL 

```

## How to user Role and check access in Handler
```
import tor_access


@tor_access.needcheck(url=True)
class IndexHandler(tornado.web.RequestHandler):
	def prepare(self):
		mrn = tor_access.MasterRoleNeed() # 超管角色；有所有的权限节点
		rn = tor_access.RoleNeed('abcrole',intro=u'普通角色',nodes=set(['restful.index.IndexHandler','userdemo']))
		self.check_access(rn)


```



