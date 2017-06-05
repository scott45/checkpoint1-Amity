__author__ = 'scotty'

import os

import unittest
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


# to test that the database can be created and removed
# to test that the db is removed before being created.
# first creates a sample db file and later removes it using the os.path.exits file
class TestDbPersistence(unittest.TestCase):
    def test_database_exists_and_removed(self):
        db_name = "test_amitydb_exists.db"
        if os.path.exists(db_name):
            os.remove(db_name)
        from sqlalchemy import create_engine
        engine = create_engine('sqlite:///' + db_name)
        from sqlalchemy.orm import sessionmaker
        session = sessionmaker()
        session.configure(bind=engine)
        Base.metadata.create_all(engine)
        if os.path.exists(db_name):
            os.remove(db_name)
        self.assertFalse(os.path.exists(db_name))
