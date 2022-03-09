# this file is used to set up the database

from sqlalchemy import create_engine
from models.Contact import Base, Contact
from models.Professor import Professor
from models.Student import Student

from constants import constants

engine = create_engine(constants.DATABASE_URL)

Base.metadata.create_all(engine)
