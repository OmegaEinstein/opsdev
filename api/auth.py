#coding:utf-8
from flask import request
import utils
from . import app
import json

def auth_login(func):
    def wrapper(*arg, **kwargs):
        try:
            authorization = request.headers.get('authorization',None)
            res = utils.validate(authorization, app.config['passport_key'])
            res = json.loads(res)
            if int(res['code']) == 1:
                return json.dumps({'code':1, 'errmsg': '%s' % (res['errmsg'])})
        except:
            return json.dumps({'code':1, 'errmsg': '验证异常'})
        return func(res, *arg, **kwargs)
    wrapper.__name__ = '%s_wrapper' % func.__name__
    return wrapper