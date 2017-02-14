from . import jsonrpc ,app
from auth import auth_login
from flask import request
import json


@jsonrpc.method('selected.get')
@auth_login
def selected(auth_info,**kwargs):
    if auth_info['code'] == 1:
        return json.dumps(auth_info)
    username = auth_info['username']
    try:
        data=request.get_json()['params']
        where = data.get('where', None)
        m_table = data.get('m_table', None)
        field = data.get('field', None)
        s_table = data.get('s_table', None)
        res = app.config['db'].get_one_result(m_table, [field], where)
        res = res[field].split(',')  #  ['1','2']
        result = app.config['db'].get_results(s_table, ['id', 'name'])
        for x in result:  #eg: [{'id':1,'name':'sa'},{'id':2,'name':'php'}]
            for r_id in res:
                if r_id in str(x['id']):
                    x['selected'] = 'selected="selected"'
                else:
                    x['selected'] = ' '
        return json.dumps({'code': 0, 'result': result})
    except:
        return json.dumps({'code':'1','errmsg':'selected.get  error'})









