from app.db import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime, Table
from sqlalchemy.orm import relationship

user_in_room = Table('user_in_room', Base.metadata,
	Column('room_id', Integer, ForeignKey(
	  'room.id', ondelete='CASCADE')),
	Column('user_id', Integer, ForeignKey(
	  'user.id', ondelete='CASCADE'))	
)

from datetime import datetime


class Room(Base):
	__tablename__ = 'room'

	id = Column(Integer, primary_key = True)
	hostId = Column(Integer, ForeignKey('user.id'))
	name = Column(String(64))
	
	created_date = Column(DateTime)

	users = relationship('User', secondary=user_in_room)
	host  = relationship('User')
	messages = relationship('Message', back_populates="room")

	def __init__(self, name, hostId):
		self.name = name
		self.hostId = hostId
		self.created_date = datetime.now()

	def __repr__(self):
		return '<Room, name: {}>'.format(self.name)

	@property
	def serialize(self):
		return {
			'id': self.id,
			'hostId': self.hostId,
			'name': self.name,
			'created_date': str(self.created_date),
			'users': [i.serialize for i in self.users]
		}

class OneToOneRoom(Base):
	__tablename__ = 'one_to_one_room'

	id = Column(Integer, primary_key = True)
	roomId = Column(Integer, ForeignKey('room.id'))
	firstId = Column(Integer, ForeignKey('user.id'))
	secondId = Column(Integer, ForeignKey('user.id'))

	def __init__(self, roomId, firstId, secondId):
		self.roomId = roomId
		self.firstId = firstId
		self.secondId = secondId
