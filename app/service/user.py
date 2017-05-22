# -*- coding: utf8 -*-

import hashlib
from app.db.user import User, user_know
from app.db import db_session
from app.service import hashPassword

def get(id):
	return db_session.query(User).get(id)

def findByPhoneNumber(phoneNumber):
	return db_session.query(User).filter(User.phoneNumber == phoneNumber).first()

def signup(data):
	user = findByPhoneNumber(data['phoneNumber'])
	if not user:
		user = User(**data)
		db_session.add(user)
	elif user.password == None:
		data['password'] = hashPassword(data['password'])
		for key in data.keys():
			setattr(user, key, data[key])
	else:
		raise Exception(u'이미 존재하는 회원입니다')
	db_session.commit()
	return user

def createContact(user, phoneNumber):
	other = findByPhoneNumber(phoneNumber)
	if not other:
		other = User(phoneNumber=phoneNumber)
		db_session.add(other)
	user.contacts.append(other)
	db_session.commit()
	return other

def removeContact(user, otherId):
	other = get(otherId)
	if not other: return False
	user.contacts.remove(other)
	if other.password == None:
		db_session.delete(other)
	db_session.commit()
	return True

def getContacts(user, page, pageSize=20, **kwargs):
	others = db_session.query(User).join(user_know, user_know.c.other_id == User.id) \
		.filter(user_know.c.user_id == user.id) \
		.offset(page*pageSize) \
		.limit(pageSize) \
		.all()
	return others




