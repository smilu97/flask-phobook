# -*- coding: utf8 -*-

from app.db.message import Message
from app.db.user import User
from app.db import db_session

def get(id):
    return db_session.query(Message).get(id)

def create(user, contactId, content):
    contact = db_session.query(User).get(contactId)
    if not contact: raise Exception(u'메시지 전송에 실패했습니다')
    if contact not in user.contacts: raise Exception(u'메시지 전송에 실패했습니다')
    message = Message(user.id, contactId, content)
    db_session.add(message)
    db_session.commit()
    return message

def findAll(user, contactId):
    contact = db_session.query(User).get(contactId)
    if not contact: raise Exception(u'메시지 전송에 실패했습니다')
    if contact not in user.contacts: raise Exception(u'메시지 전송에 실패했습니다')
    messages = db_session.query(Message).filter(Message.fromId == user.id).filter(Message.toId == contactId)
    messages = messages.order_by(Message.time).all()
    return messages