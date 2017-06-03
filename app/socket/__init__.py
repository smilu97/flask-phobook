from app.socket.base import BaseSocket

def register_socket(socketio):
	socketio.on_namespace(BaseSocket('/'))