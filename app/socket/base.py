from flask_socketio import Namespace, join_room, leave_room, emit
from flask import session
from app.db import db_session
from app.db.user import User
from app.db.message import Message

class BaseSocket(Namespace):

    def on_connect(self):
        print 'connect,'
        session['connect'] = True

    def on_disconnect(self):
        print 'disconnect'
        session.clear()

    def on_enter_chat(self, data):
        try:
            print 'enter_chat:',data
            token = data['token']
            contactId = int(data['contactId'])
            user = db_session.query(User).filter(User.token == token).first()
            if not user:
                raise Exception('enter_chat: User not found')
            other = db_session.query(User).get(contactId)
            if not other:
                raise Exception('enter_chat: Other not found')
            a, b = user.id, other.id
            if a > b:
                b, a = a, b
            room = str(a) + ':' + str(b)
            join_room(room)
        except Exception as e:
            print e


    def on_leave_chat(self, data):
        try:
            print 'leave_chat:',data
            token = data['token']
            contactId = int(data['contactId'])
            user = db_session.query(User).filter(User.token == token).first()
            if not user:
                raise Exception('enter_chat: User not found')
            other = db_session.query(User).get(contactId)
            if not other:
                raise Exception('enter_chat: Other not found')
            a, b = user.id, other.id
            if a > b:
                b, a = a, b
            room = str(a) + ':' + str(b)
            leave_room(room)
        except Exception as e:
            print e

    def on_chat(self, data):
        try:
            print 'chat:',data
            token = data['token']
            user = db_session.query(User).filter(User.token == token).first()
            if not user:
                raise Exception('chat: invalid token')
            f = user.id
            t = int(data['contactId'])
            content = str(data['content'])

            msg = Message(f, t, content)
            db_session.add(msg)
            db_session.commit()

            if f > t:
                f, t = t, f
            room = str(f) + ':' + str(t)
            emit('chat', msg.serialize, room=room)
        except Exception as e:
            print e