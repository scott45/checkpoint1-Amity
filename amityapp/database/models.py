__author__ = 'scotty'


from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


# people table
class People(Base):
    __tablename__ = 'people'
    id = Column(Integer, primary_key=True)
    person_qualifier = Column(String(50))
    person_name = Column(String(80))
    person_label = Column(String(25))
    wants_accommodation = Column(String(5))
    office_allocated = Column(String(50))
    living_space_allocated = Column(String(50))

    def __repr__(self):
        return "<Person(person_name='%s')>" % self.person_name


# rooms table
class Rooms(Base):
    __tablename__ = 'rooms'
    id = Column(Integer, primary_key=True)
    room_name = Column(String(25), nullable=False)
    room_type = Column(String(25), nullable=False)
    room_capacity = Column(Integer)

    def __repr__(self):
        return "<Room(room_name='%s')>" % self.room_name


# Establishes a database connection
class DatabaseManager(object):
    def __init__(self, db_name=None):
        self.db_name = db_name
        if self.db_name:
            self.db_name = db_name + '.sqlite'
        else:
            self.db_name = 'amity_db.sqlite'
        self.engine = create_engine('sqlite:///' + self.db_name)
        self.session = sessionmaker()
        self.session.configure(bind=self.engine)
        Base.metadata.create_all(self.engine)
