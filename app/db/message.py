from app.db import Base
from sqlalchemy import Column, Integer, String, Table, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship

from datetime import datetime

class Message(Base):
    __tablename__ = 'message'

    id = Column(Integer, primary_key = True)
    fromId = Column(Integer, ForeignKey('user.id'))
    toId = Column(Integer, ForeignKey('user.id'))
    content = Column(Text)
    time = Column(DateTime)

    def __init__(self, fromId, toId, content, time=None):
        self.fromId = fromId
        self.toId = toId
        self.content = content
        self.time = time or datetime.now()
    
    def __repr__(self):
        return '<Message, from: {}, to: {}, msg: {}, time: {}>'.format(self.fromId, self.toId, self.content, self.time)
    
    @property
    def serialize(self):
        return {
            'id': self.id,
            'fromId': self.fromId,
            'toId': self.toId,
            'content': self.content,
            'time': self.time
        }