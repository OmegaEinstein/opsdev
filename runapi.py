#coding:utf-8
from api import app
import utils
import db

#导入配置文件参数，以字典形式返回
config = utils.get_config('api')

#将自定义配置文件参数加入到app.config全局大字典里
app.config.update(config)

#将数据库实例加到全局大字典
app.config['db'] = db.Cursor(config)