from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import validates
from sqlalchemy.ext.declarative import AbstractConcreteBase, declarative_base
from sqlalchemy.ext.hybrid import hybrid_property

from exceptions.InvalidNameError import InvalidNameError
from exceptions.InvalidUsernameError import InvalidUsernameError

Base = declarative_base()


class Contact(AbstractConcreteBase, Base):
    """
      Construct an abstract Column Base that other Columns can inherit from.

      :param name: Name of the contact.
      :type  name: String
      :param id: ID of the contact. Serves as the primary_key.
      :type  id: Integer
      :param username: Username of the contact.
      :type  username: String

      pre:
        name: has alphabets or spaces, and it's length is greater than 0.
        id: is an integer and it's length is greater than 0.
        username: can only have alphanumeric characters and it's length is greater than 0.

      post:
        self.name: has alphabets or spaces, and has a length greater than 0.
        self.id: is an integer and is greater 0.
        self.username: is an alphanumeric string with a length greater than 0.
    """

    # class variable
    _domainName = "example.com"

    # attributes
    _id = Column(Integer, primary_key=True)
    _name = Column(String(50), nullable=False)
    _username = Column(String(50), nullable=False, unique=True)


    @validates('_name')
    def validName(self, key, name=_name):
        if not (all(x.isalpha() or x.isspace() for x in name) and (len(name) > 0)):
            raise InvalidNameError(name)
        return name

    @validates('_username')
    def validUsername(self, key, username=_username):
        if not username.isalnum() or not (len(username) > 0):
            raise InvalidUsernameError(username)
        return username

    @hybrid_property
    def id(self):
        return self._id

    @hybrid_property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        """
          Set the name of the contact object.

          :param name: Name of the contact.

          pre:
            name has alphabets or spaces, and it's length is greater than 0.

          post:
            self._name has alphabets or spaces, and has a length greater than 0.
        """

        self._name = name

    @hybrid_property
    def username(self):
        return self._username

    @username.setter
    def username(self, username):
        """
          Set the username of the contact object.

          :param username: Username of the contact.

          pre:
            username can only have alphanumeric characters and it's length is greater than 0.

          post:
            self._username is an alphanumeric string with a length greater than 0.
        """
        self._username = username

    @property
    def serialize(self):
        return {
            'id': self._id,
            'name': self._name,
            'username': self._username
        }
