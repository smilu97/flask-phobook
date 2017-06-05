# -*- coding: utf8 -*-

from app.socket.base import BaseSocket
from app.db import db_session

import app.service.user as userService
import app.service.room as roomService


def register_socket(socketio):
    socketio.on_namespace(BaseSocket('/'))


def make_one_to_one_room_name(token, contactId):
	current_user = userService.findByToken(token)
	if not current_user:
		raise Exception(u'User not found')
	contact_user = userService.get(contactId)
	if not contact_user:
		raise Exception(u'Contact not found')

	firstId = current_user.id
	secondId = contact_user.id

	if firstId > secondId:
		firstId, secondId = secondId, firstId

	return current_user, contact_user, '{}:{}'.format(firstId, secondId)
