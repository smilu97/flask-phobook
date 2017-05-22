from flask_login import LoginManager
from app.db import db_session
from app.db.user import User
from app import app
import base64, hashlib
from app.service import hashPassword

login_manager = LoginManager()

login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
	return db_session.query(User).get(user_id)

@login_manager.request_loader
def load_user_request(request):
	try:
		auth = request.headers.get('Authorization')
		if not auth: return None
		if auth[0:5] == 'Basic':
			auth = base64.b64decode(auth[6:])
			div = auth.find(':')
			if div == -1: raise Exception('invalid basic auth')
			username = auth[:div]
			password = hashPassword(auth[div+1:])
			user = db_session.query(User).filter(User.phoneNumber == username).filter(User.password == password).first()
			if not user:
				return None
			return user
	except Exception as e:
		print e