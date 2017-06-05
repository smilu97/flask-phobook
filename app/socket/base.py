from flask_socketio import Namespace, join_room, leave_room, emit
from flask import session

from app.socket import *

import app.service.user as userService
import app.service.room as roomService
import app.service.message as messageService

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
            current_user = userService.findByToken(token)
            if not current_user:
                raise Exception('enter_chat: User not found')

            roomId = int(data['roomId'])
            room = roomService.get(roomId)
            if not room:
                raise Exception('enter_chat: Room not found')
            if current_user not in room.users:
                raise Exception('enter_chat: Unauthorized entering room')

            print 'joined room: {}'.format(roomId)
            join_room(roomId)

        except Exception as e:
            print e

    def on_leave_chat(self, data):
        try:
            print 'leave_chat:',data
            roomId = data['roomId']
            leave_room(roomId)
        except Exception as e:
            print e

    def on_chat(self, data):
        try:
            print 'chat:',data
            token = data['token']
            current_user = userService.findByToken(token)
            if not current_user:
                raise Exception('chat: invalid token')

            room_id = data['roomId']
            room = roomService.get(room_id)
            if not room:
                raise Exception('chat: Room not found')

            content = data['content']

            msg = messageService.create(room, current_user, content)

            emit('chat', msg.serialize, room=room.id)
        except Exception as e:
            print e