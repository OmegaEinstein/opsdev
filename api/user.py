#coding:utf-8
from flask import Flask
from  . import app, jsonrpc
import json
from auth import auth_login


@jsonrpc.method('user.getinfo')
@auth_login
def userselfinfo(auth_info, **kwargs):
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




