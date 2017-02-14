#coding:utf-8
from . import jsonrpc,app
from auth import auth_login
from flask import request
import json

@jsonrpc.method('role.get')
@auth_login
def role_get(auth_info, **kwargs):
    username = auth_info['username']
    try:
        output = ['id','name','name_cn','p_id','info']
        data = request.get_json()['params']
        fields = data.get('output',output)
        where = data.get('where', None)
        if not where:
            return json.dumps({'code': 1, 'errmsg': 'must need a condition'})
        result = app.config['db'].get_one_result('role', fields, where)
        if not result:
            return json.dumps({'code': 1, 'errmsg': 'result is null'})
        else:
            return json.dumps({'code': 0, 'result': result})
    except:
        return  json.dumps({'code':1,'errmsg ':'get role failed'})






