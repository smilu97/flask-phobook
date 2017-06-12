# -*- coding: utf8 -*-

from flask import Blueprint, request, jsonify
from flask_login import current_user
from app.service import assert_login

import app.service.room as service
import app.service.user as userService

app = Blueprint('room', __name__)

@app.route('/room/one_to_one/<int:contactId>', methods=['GET'])
def controlGetOneToOneRoom(contactId):
	try:
		assert_login();
		contact_user = userService.get(contactId)
		if not contact_user:
			raise Exception(u'Contact user not found')

		room = service.getOneToOneRoom(current_user, contact_user)
		return jsonify({'success': 1, 'room': room.serialize})
	except Exception as e:
		print e
		return jsonify({'success': 0, 'error': str(e)})


@app.route('/room/<int:roomId>', methods=['GET'])
def controlGetRoom(roomId):
	try:
		assert_login();

		room = service.get(roomId)
		if not room:
			raise Exception(u'Room not found')

		if current_user not in room.users:
			raise Exception(u'Not authorized')

		service.userCheckRoom(current_user, room)

		return jsonify({'success': 1, 'room': room.serialize, 'messages': [i.serialize for i in room.messages]})
	except Exception as e:
		print e
		return jsonify({'success': 0, 'error': str(e)})


@app.route('/room', methods=['POST'])
def controlPostRoom():
	try:
		assert_login();

		json = request.get_json()
		name = json['name']
		userIds = json['users']
		users = []

		for userId in userIds:
			user = userService.get(userId)
			if not user:
				raise Exception(u'User not found')
			users.append(user)

		room = service.create(name, current_user, users)
		return jsonify({'success': 1, 'room': room.serialize})
	except Exception as e:
		print e
		return jsonify({'success': 0, 'error': str(e)})


@app.route('/room/<int:roomId>/invite', methods=['POST'])
def controlPostRoomInvite(roomId):
	try:
		assert_login();

		json = request.get_json();
		userIds = json['users']

		room = service.get(roomId)
		if not room:
			raise Exception(u'Room not found')

		if current_user not in room.users:
			raise Exception(u'Not authorized')

		users = []
		for userId in userIds:
			user = userService.get(userId)
			if user and (user in current_user.contacts):
				users.append(user)

		service.inviteMany(room, users)
		return jsonify({'success': 1})
	except Exception as e:
		print e
		return jsonify({'success': 0, 'error': str(e)})


@app.route('/room/<int:roomId>/exit', methods=['POST'])
def controlPostExitRoom(roomId):
	try:
		assert_login();

		room = service.get(roomId)
		if not room:
			raise Exception(u'Room not found')

		service.exitRoom(current_user, room)
		return jsonify({'success': 1})
	except Exception as e:
		print e
		return jsonify({'success': 0, 'error': str(e)})


@app.route('/room/all', methods=['GET'])
def controlGetAllRoom():
	try:
		assert_login()
		rooms = service.getAllRoomsWithCheck(current_user)
		return jsonify({'success': 1, 'rooms': rooms})
	except Exception as e:
		print e
		return jsonify({'success': 0, 'error': str(e)})