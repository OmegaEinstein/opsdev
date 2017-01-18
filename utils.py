#coding:utf-8
import os
import ConfigParser
import base64
import time
import json

work_dir = os.path.dirname(os.path.realpath(__file__))

def get_config(section=''):
    config = ConfigParser.ConfigParser()
    service_conf = os.path.join(work_dir,'conf/service.conf')
    config.read(service_conf)
    conf_items = dict(config.items('common')) if config.has_section('common') else {}
    print conf_items
    if section and config.has_section(section):
        conf_items.update(config.items(section))
    return conf_items

def get_validate(username, uid, role, fix_pwd):
    t = int(time.time())
    return base64.b64encode('%s|%s|%s|%s|%s' % (username, uid, role, fix_pwd, t)).strip()

def validate(key,fix_pwd):
    t = int(time.time())
    key = base64.b64decode(key)
    x = key.split('|')
    if len(x) != 5:
        return json.dumps({'code':1, 'errmsg':"token参数不足"})
    if t > int(x[4])+2*60*60:
        return json.dumps({'code':1, 'errmsg':"登录已经过期"})
    if fix_pwd == x[3]:
        return json.dumps({'code':0, 'username':x[0], 'uid':x[1], 'r_id':x[2]})
    else:
        return json.dumps({'code':1, 'errmsg':"密码不正确"})

