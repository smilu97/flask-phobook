# -*- coding: utf8 -*-

from app.db.message import Message
from app.db.user import User, user_know
from app.db import db_session

from sqlalchemy import or_, and_


def get(id):
    return db_session.query(Message).get(id)


def create(user, contactId, content):
    contact = db_session.query(User).get(contactId)
    if not contact:
        raise Exception(u'메시지 전송에 실패했습니다')
    if contact not in user.contacts:
        raise Exception(u'메시지 전송에 실패했습니다')
    message = Message(user.id, contactId, content)
    db_session.add(message)
    db_session.commit()
    return message


def find_all(user, contact_id):
    contact = db_session.query(User).get(contact_id)
    if not contact:
        raise Exception(u'메시지를 읽는데에 실패했습니다')
    know = db_session.query(user_know).filter(
        user_know.c.user_id == user.id and user_know.c.other_id == contact_id).first()
    if not know:
        raise Exception(u'메시지를 읽는데에 실패했습니다')

    condition1 = and_(Message.fromId == user.id, Message.toId == contact_id)
    condition2 = and_(Message.fromId == contact_id, Message.toId == user.id)

    messages = db_session.query(Message)
    messages = messages.filter(or_(condition1, condition2))
    messages = messages.order_by(Message.time).all()

    return messages
