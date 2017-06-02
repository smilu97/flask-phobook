#-*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from flask import Flask
import config

app = Flask('phobook')
app.config.from_object('config')

# Handling OPTION Method request for cross site
from flask_cors import CORS, cross_origin
CORS(app)

from app.db import init_db, db_session
init_db()

from app.login import *

@app.teardown_appcontext
def shutdown_session(exception):
	db_session.remove()

from app.controller import routes
routes(app)