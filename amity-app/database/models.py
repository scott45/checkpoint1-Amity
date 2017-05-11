__author__ = 'scotty'

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class People(Base):
    __tablename__ = 'people'
    id = Column(Integer, primary_key=True)
    person_qualifier = Column(String(50), unique=True)
    person_name = Column(String(80))
    person_label = Column(String(25))
    wants_accommodation = Column(String(5))
    office_allocated = Column(String(50))
    living_space_allocated = Column(String(50))

    def __repr__(self):
        return "<Person(person_name='%s')>" % self.person_name


class Rooms(Base):
    __tablename__ = 'rooms'
    id = Column(Integer, primary_key=True)
    room_name = Column(String(25), nullable=False)
    room_type = Column(String(25), nullable=False)
    room_capacity = Column(Integer)

    def __repr__(self):
        return "<Room(room_name='%s')>" % self.room_name

    
