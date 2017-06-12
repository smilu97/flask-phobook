# -*- coding: utf8 -*-

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

    def on_user_join(self, data):
        token = data['token']
        current_user = userService.findByToken(token)
        if current_user:
            userService.connect(current_user)
            join_room('user:{}'.format(current_user.id))
            online_friends = userService.findOnlineContact(current_user)
            for user in online_friends:
                emit('friend_in', current_user.id, room='user:{}'.format(user.id))


    def on_user_out(self, data):
        token = data['token']
        current_user = userService.findByToken(token)
        if current_user:
            userService.disconnect(current_user)
            leave_room('user:{}'.format(current_user.id))
            online_friends = userService.findOnlineContact(current_user)
            for user in online_friends:
                emit('friend_out', current_user.id, room='user:{}'.format(user.id))

    def on_chat(self, data):
        try:
            token = data['token']
            current_user = userService.findByToken(token)
            if not current_user:
                raise Exception('chat: invalid token')

            room_id = data['roomId']
            room = roomService.get(room_id)
            if not room:
                raise Exception('chat: Room not found')

            content = data['content']

            print 'chat: {} said {}'.format(current_user.name, content)

            msg = messageService.create(room, current_user, content).serialize

            users = roomService.findConnectingUsersInRoom(room)
            for user in users:
                emit('chat', msg, room='user:{}'.format(user.id))
        except Exception as e:
            print e