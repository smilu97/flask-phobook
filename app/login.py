from flask_login import LoginManager
from app.db import db_session
from app.db.user import User
from app import app
import base64
from app.service import hash_password

login_manager = LoginManager()

login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return db_session.query(User).get(user_id)


@login_manager.request_loader
def load_user_request(request):
    try:
        auth = request.headers.get('Authorization')
        if not auth:
            return None
        if auth[:5] == 'Token':
            token = auth[6:]
            if len(token) == 64:
                user = db_session.query(User).filter(
                    User.token == token).first()
                if user:
                    return user
    except Exception as e:
        print e
