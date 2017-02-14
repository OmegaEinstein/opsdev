from flask import Flask
from flask_jsonrpc import JSONRPC
import sys
reload(sys)

app = Flask(__name__)
jsonrpc = JSONRPC(app,'/api')

import login
import user
import select