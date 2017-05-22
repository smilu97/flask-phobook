
def routes(app):
	from app.controller.base import app as base
	from app.controller.user import app as user

	app.register_blueprint(base)
	app.register_blueprint(user)