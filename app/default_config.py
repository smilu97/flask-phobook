# -*- coding: utf8 -*-
import os

DEBUG = True
TESTING = False

PROPAGATE_EXCEPTIONS = None
SECRET_KEY = 'HanyangUnivSmilu'
SESSION_COOKIE_NAME = 'phobookSession'
SESSION_COOKIE_SECURE = True

APPLICATION_ROOT = os.path.realpath('.')
MAX_CONTENT_LENGTH = 1024 * 1024 * 10
JSONIFY_PRETTYPRINT_REGULAR = True

DATABASE_USERNAME = '<username of mysql database>'
DATABASE_PASSWORD = '<password of mysql database>'
DATABASE_URL = '<url of database>'
DATABASE_SCHEME_NAME = '<scheme to use>'

DATABASE_CONNECT_URL = 'mysql+pymysql://{}:{}@{}/{}'.format(\
        DATABASE_USERNAME, DATABASE_PASSWORD, \
        DATABASE_URL, DATABASE_SCHEME_NAME \
    )
DATABASE_SQL_ECHO = False
