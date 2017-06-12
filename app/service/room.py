# -*- coding: utf8 -*- 

from app.db import db_session, engine
from app.db.room import Room, user_in_room, OneToOneRoom
from app.db.message import Message
from app.db.user import User

from sqlalchemy import update

from datetime import datetime

def get(id):
	return db_session.query(Room).get(id)

def findByName(name):
	return db_session.query(Room).filter(Room.name == name).first()

def create(name, host, users=None):
	room = Room(name, host.id)
	room.users.append(host)
	if users:
		for user in users:
			room.users.append(user)
	db_session.add(room)
	db_session.commit()

	return room

def invite(room, user):
	room.users.append(user)
	for ot in room.oto:
		room.oto.remove(ot)
		db_session.delete(ot)
	db_session.commit()

def inviteMany(room, users):
	for user in users:
		room.users.append(user)
	for ot in room.oto:
		room.oto.remove(ot)
		db_session.delete(ot)
	db_session.commit()

def registerAsOneToOne(room, first, second):
	if first.id > second.id:
		first, second = second, first

	otor = OneToOneRoom(room.id, first.id, second.id)
	room.users.append(first)
	room.users.append(second)
	db_session.add(otor)
	db_session.commit()

	return otor

def getOneToOneRoom(first, second):
	current_user = first

	if first.id > second.id:
		first, second = second, first

	otor = db_session.query(OneToOneRoom).filter(OneToOneRoom.firstId == first.id)\
			.filter(OneToOneRoom.secondId == second.id).first();
	if not otor:
		room = create(None, first)
		registerAsOneToOne(room, first, second)
	else:
		room = get(otor.roomId)
		if current_user not in room.users:
			room.users.append(current_user)
			db_session.commit()
	return room

def findLastMessage(room):
	return db_session.query(Message).filter(Message.roomId == room.id)\
			.order_by(Message.time.desc()).first()

def getAllRoomsWithCheck(user):
	res = []
	for room in user.rooms:
		last_message = findLastMessage(room)
		last_check = db_session.query(user_in_room.c.last_check)\
			.filter(user_in_room.c.room_id == room.id)\
			.filter(user_in_room.c.user_id == user.id).first()[0]
		room_dict = room.serialize
		room_dict['lastMessage'] = last_message and last_message.serialize
		room_dict['lastCheck'] = str(last_check)
		
		res.append(room_dict)
	return res

def userCheckRoom(user, room):
	conn = engine.connect()
	stmt = update(user_in_room).where((user_in_room.c.room_id == room.id) & (user_in_room.c.user_id == user.id))\
		.values(last_check=datetime.now())
	print stmt
	conn.execute(stmt)

def findConnectingUsersInRoom(room):
	result = db_session.query(user_in_room, User).filter(user_in_room.c.room_id == room.id)\
		.join(User, User.id == user_in_room.c.user_id)\
		.filter(User.connecting == 1).all()
	return [i.User for i in result]

def exitRoom(user, room):
	room.users.remove(user)
	if len(room.users) == 0:
		db_session.delete(room)
	db_session.commit()