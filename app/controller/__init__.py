
def routes(app):
    from .base import app as base
    from .user import app as user
    from .message import app as message
    from .room import app as room
    from .file import app as file

    app.register_blueprint(base)
    app.register_blueprint(user)
    app.register_blueprint(message)
    app.register_blueprint(room)
    app.register_blueprint(file)
