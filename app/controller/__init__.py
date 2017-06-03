
def routes(app):
	from .base import app as base
	from .user import app as user
	from .message import app as message

	app.register_blueprint(base)
	app.register_blueprint(user)
	app.register_blueprint(message)