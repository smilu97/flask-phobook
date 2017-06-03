from flask_socketio import Namespace, emit
from flask import session

class BaseSocket(Namespace):
	def on_connect(self):
		print 'connect,'
		session['connect'] = True

	def on_disconnect(self):
		print 'disconnect'
		session.clear()
