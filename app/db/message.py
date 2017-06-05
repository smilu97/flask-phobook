from app.db import Base
from sqlalchemy import Column, Integer, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship

from datetime import datetime


class Message(Base):
    __tablename__ = 'message'

    id = Column(Integer, primary_key=True)
    roomId = Column(Integer, ForeignKey('room.id', ondelete='CASCADE'))
    userId = Column(Integer, ForeignKey('user.id'))
    content = Column(Text)
    time = Column(DateTime)

    room = relationship('Room', back_populates="messages")

    def __init__(self, roomId, userId, content, time=None):
        self.roomId = roomId
        self.userId = userId
        self.content = content
        self.time = time or datetime.now()

    def __repr__(self):
        return '<Message, room: {}, user: {}, content: {}, time: {}>'.format(self.roomId, self.userId, self.content, self.time)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'roomId': self.roomId,
            'userId': self.userId,
            'content': self.content,
            'time': str(self.time),
        }
