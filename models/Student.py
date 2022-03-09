from .Contact import Contact
from sqlalchemy.orm import validates
from sqlalchemy import Column, String
from sqlalchemy.ext.hybrid import hybrid_property

from exceptions.InvalidMajorError import InvalidMajorError

class Student(Contact):
    """
      Construct a Student object that inherits from the Contact class.

      :param name: Name of the student.
      :type  name: String
      :param id: Student's ID.
      :type  id: Integer
      :param username: Student's username.
      :type  username: String
      :param major: Student's major.
      :type  major: String

      pre:
        name: has alphabets or spaces, and it's length is greater than 0.
        id: is a number and it's length is greater than 0.
        username: can only have alphanumeric characters and it's length is greater than 0.
        major: has alphabets or spaces, and it's length is greater than 0.

      post:
        self._name: has alphabets or spaces, and has a length greater than 0.
        self._id: is an integer and is greater 0.
        self._username: is an alphanumeric string with a length greater than 0.
        self._major: has alphabets or spaces, and it's length is greater than 0.
    """
    __tablename__ = 'student'

    _major = Column(String(50))

    __mapper_args__ = {
        'polymorphic_identity': 'student',
        'concrete': True
    }

    @validates('_major')
    def validMajor(self, key, major = _major):
        if not all(x.isalpha() or x.isspace() for x in major) or not (len(major) > 0):
            raise InvalidMajorError(major)
        return major

    @hybrid_property
    def major(self):
        return self._major

    @major.setter
    def major(self, major):
        """
          Set the major of the student object.

          :param major: Student's major.

          pre:
            major has alphabets or spaces, and it's length is greater than 0.

          post:
            self._major has alphabets or spaces, and has a length greater than 0.
        """
        self._major = major

    @property
    def serialize(self):
        output = {}

        json = super(Student, self).serialize

        for j in json.items():
            output[j[0]] = j[1]

        output['major'] = self._major

        return output
