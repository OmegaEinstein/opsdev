#coding:utf-8
from flask import Flask
from  . import app, jsonrpc
import json
from auth import auth_login
from flask import request

@jsonrpc.method('user.getinfo')
@auth_login
def userselfinfo(auth_info, **kwargs):
    print "auth_info is %s" % (auth_info)
    username = auth_info['username']
    fields = ['id','username','name','email','mobile','is_lock','r_id']
    try:
        user = app.config['db'].get_one_result('user', fields, where={'username':username})
        if user.get('r_id', None):
            r_id = user['r_id'].split(',')
            rids = app.config['db'].get_results('role', ['id','name','p_id'], where={'id': r_id})
        else:
            rids = {}
        pids = []
        for x in rids:
            pids += x['p_id'].split(',')
        pids = list(set(pids)) #去重，通过用户名查到角色id，再通过角色id取到用户权限id
        user['r_id'] = [x['name'] for x in rids]

        if pids:   #将用户到权限id转为权限名
            mypids = app.config['db'].get_results('power', ['id', 'name', 'name_cn', 'url'], where={'id': pids})
            user['p_id'] = dict([(str(x['name']), dict([(k, x[k]) for k in ('name_cn','url')])) for x in mypids]) #返回格式：{'git':{'name_cn':'git','url':'http://git.com'},......}
        else:
            user['p_id'] = {}

        return json.dumps({'code':0, 'user':user})
    except:
        return json.dumps({'code':1, 'errmsg':"get userinfo failed"})

#获取用户列表
@jsonrpc.method('user.getlist')
@auth_login
def userlist(auth_info, **kwargs):
    username = auth_info['username']
    r_id = auth_info['r_id']
    users = []
    fields = ['id','username','name','email','mobile','is_lock','r_id']
    try:
        if '1' not in r_id:
            return json.dumps({'code':1,'errmsg':'只有管理员才有此权限'})
        #获取角色的id,name并存为字典，如{'1':'sa','2':'php'}
        rids = app.config['db'].get_results('role',['id','name'])
        rids = dict([(str(x['id']), x['name']) for x in rids])
        result = app.config['db'].get_results('user', fields)  #[{'id':1,'name':'mike','    r_id':'1,2,3'},{},{}]
        for user in result:  #查询user表中的r_id,与role表生成的字典对比，一致则将id替换为name,如，"sa,php"
            user['r_id'] = ','.join([rids[x] for x in user['r_id'].split(',') if x in rids])
            users.append(user)
        return json.dumps({'code':0, 'users':users, 'count':len(users)})
    except:
        return json.dumps({'code':1, 'errmsg':'获取用户列表失败'})

#通过传入的条件id，查询某条用户的信息，用于管理员修改用户信息
@jsonrpc.method('user.get')
@auth_login
def userinfo(auth_info,**kwargs):
    username = auth_info['username']
    try:
        output = ['id','username','name','email','mobile','is_lock','r_id']
        data = request.get_json()['params']
        fields = data.get('output',output) # api可以指定输出字段，如果没有指定output，就按默认output输出
        where = data.get('where', None)  # 前端传来的where条件
        if not where:
            return json.dumps({'code': 1, 'errmsg': 'must need a condition'})
        result = app.config['db'].get_one_result('user', fields, where)
        if not result:
            return json.dumps({'code': 1, 'errmsg': 'user  not  exist'})
        return json.dumps({'code': 0, 'result': result})
    except:
        return json.dumps({'code':1,'errmsg':'Get user  failed'})









