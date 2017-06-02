from app.db import Base
from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship
from app.service import hashPassword
import hashlib

user_know = Table('user_know', Base.metadata,
	Column('user_id', Integer, ForeignKey('user.id', ondelete='CASCADE')),
	Column('other_id', Integer, ForeignKey('user.id', ondelete='CASCADE'))
)

class User(Base):
	__tablename__ = 'user'
	
	id = Column(Integer, primary_key = True)
	name = Column(String(32))
	phoneNumber = Column(String(128), index=True)
	password = Column(String(256))
	role = Column(String(32))

	contacts = relationship('User', secondary=user_know,
		primaryjoin=(id == user_know.c.user_id),
		secondaryjoin=(id == user_know.c.other_id),
		backref="reverse_contacts"
	)
	
	def __init__(self, phoneNumber, name=None, password=None) :
		self.name = name
		self.phoneNumber = phoneNumber
		self.password = password and hashPassword(password)
		self.role = 'USER'

	def __repr__(self):
		return '<User {}, name: {}, phoneNumber: {}>'.format(self.id, self.name, self.phoneNumber)

	@property
	def is_authenticated(self):
		return True
	@property
	def is_active(self):
		return True
	@property
	def is_anonymous(self):
		return False
	@property
	def get_id(self):
		return unicode(self.id)

	@property
	def serialize(self):
		return {
			'id': self.id,
			'name': self.name,
			'phoneNumber': self.phoneNumber
		}