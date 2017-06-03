# -*- coding: utf8 -*-

import hashlib
from app.db.user import User, user_know
from app.db import db_session
from app.service import hash_password


def get(id):
    return db_session.query(User).get(id)


def findByPhoneNumber(phoneNumber):
    return db_session.query(User).filter(User.phoneNumber == phoneNumber).first()


def login(phoneNumber, password):
    user = findByPhoneNumber(phoneNumber)
    if not user:
        raise Exception(u'로그인에 실패했습니다')
    p_hash = hash_password(password)
    if user.password != p_hash:
        raise Exception(u'로그인에 실패했습니다')
    return user


def signup(data):
    user = findByPhoneNumber(data['phoneNumber'])
    phoneNumber = data['phoneNumber']
    if len(phoneNumber) != 10 and len(phoneNumber) != 11:
        raise Exception(u'전화번호는 10자리 혹은 11자리여야 합니다')
    name = data['name']
    if len(name) < 2:
        raise Exception(u'이름이 너무 짧습니다')
    password = data['password']
    if len(password) < 2:
        raise Exception(u'비밀번호가 너무 짧습니다')
    if not user:
        user = User(**data)
        db_session.add(user)
    elif user.password is None:
        data['password'] = hash_password(data['password'])
        for key in data.keys():
            setattr(user, key, data[key])
    else:
        raise Exception(u'이미 존재하는 회원입니다')
    db_session.commit()
    return user


def createContact(user, name, phoneNumber):
    other = findByPhoneNumber(phoneNumber)
    if not other:
        other = User(name=name, phoneNumber=phoneNumber)
        db_session.add(other)
    user.contacts.append(other)
    db_session.commit()
    return other


def removeContact(user, otherId):
    other = get(otherId)
    if not other:
        return False
    user.contacts.remove(other)
    db_session.commit()
    return True


def getContacts(user, page, pageSize=20, **kwargs):
    others = db_session.query(User).join(user_know, user_know.c.other_id == User.id) \
        .filter(user_know.c.user_id == user.id) \
        .offset(page*pageSize) \
        .limit(pageSize) \
        .all()
    return others
