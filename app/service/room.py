# -*- coding: utf8 -*- 

from app.db import db_session
from app.db.room import Room, user_in_room, OneToOneRoom

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
	if first.id > second.id:
		first, second = second, first

	otor = db_session.query(OneToOneRoom).filter(OneToOneRoom.firstId == first.id)\
			.filter(OneToOneRoom.secondId == second.id).first();
	if not otor:
		room = create(None, first)
		registerAsOneToOne(room, first, second)
		return room
	else:
		return get(otor.roomId)
		