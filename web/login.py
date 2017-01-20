#coding:utf-8
from flask import Flask,request,session,render_template
from . import app
import requests
import json
import utils

headers = {'content-type': 'application/json'}

@app.route("/login",methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('passwd')
        url = "http://%s/api/login?username=%s&passwd=%s" % ('apihost', username, password)
        r = requests.get(url, headers=headers) #请求api验证用户，并获取token
        result = json.loads(r.content)
        if result['code'] == 0:
            token = result['authorization']
            res = utils.validate(token,'passport_key')
            res = json.loads(res)
            session['author'] = token
            session['username'] = username
            return json.dumps({'code':0})
        else:
            return json.dumps({'code':1, 'errmsg':result['errmsg']})
    return render_template('login.html')