#coding:utf-8
from flask import request, render_template
from . import app
import hashlib,json,time
import utils

#用户登录验证
@app.route('/api/login',methods=['GET'])
def login():
    try:
        username = request.args.get('username',None)
        passwd = request.args.get('passwd',None)
        passwd = hashlib.md5(passwd).hexdigest()
        if not (username and passwd):
            return json.dumps({'code':1, 'errmsg':"need username or password"})
        result = app.config['db'].get_one_result('user',['id','username', 'password', 'r_id', 'is_lock'], {'username':username})
        if not result:
            return json.dumps({'code':1, 'errmsg':'username is not exist'})
        if result['is_lock'] == 1:
            return json.dumps({'code':1, 'errmsg':'user is lock'})
        if passwd == result['password']:
            data = {'last_login': time.strftime('%Y-%m-%d %H:%M:%S')}
            app.config['db'].execute_update_sql('user', data, {'username':username})
            token = utils.get_validate(username, result['uid'], result['r_id'])
            return json.dumps({'code':0, 'authorization': token})
        else:
            return json.dumps({'code':1, 'errmsg':"passwd is wrong"})
    except:
        return json.dumps({'code':1,'errmsg':"login fail"})