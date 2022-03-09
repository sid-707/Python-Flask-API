# this file contains sample data

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models.Contact import Base
from models.Professor import Professor
from models.Student import Student

from constants import constants

engine = create_engine(constants.DATABASE_URL)

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

session = DBSession()

professor1 = Professor(name="Isaac Newton", username="newton", extension="123", department="Physics")
session.add(professor1)
session.commit()

professor2 = Professor(name="Albert Einstein", username="einstein", extension="234", department="Physics")
session.add(professor2)
session.commit()

professor3 = Professor(name="Alan Turing", username="turing", extension="345", department="Computer Science")
session.add(professor3)
session.commit()

student1 = Student(name="Frodo", username="frodo", major="English")
session.add(student1)
session.commit()

student2 = Student(name="Harry Potter", username="potter", major="Philosophy")
session.add(student2)
session.commit()

student3 = Student(name="Tony Stark", username="stark", major="Electrical Engineering")
session.add(student3)
session.commit()
