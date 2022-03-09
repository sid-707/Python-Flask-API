from .Contact import Contact
from sqlalchemy import Column, String
from sqlalchemy.orm import validates
from sqlalchemy.ext.hybrid import hybrid_property

from exceptions.InvalidExtensionError import InvalidExtensionError
from exceptions.InvalidDepartmentError import InvalidDepartmentError

class Professor(Contact):
    """
      Construct a Professor object that extends the Contact Column.

      :param name: Name of the professor.
      :type  name: String
      :param id: Professor's ID.
      :type  id: Integer
      :param username: Professor's username.
      :type  username: String
      :param extension: Professor's extension.
      :type  extension: String
      :param department: Professor's department
      :type  department: String

      pre:
        name: has alphabets or spaces, and it's length is greater than 0.
        id: is a number and it's length is greater than 0.
        username: can only have alphanumeric characters and it's length is greater than 0.
        extension: is a string of a 3-5 digit number that is greater that 0.
        department: has alphabets or spaces, and it's length is greater than 0.

      post:
        self._name: has alphabets or spaces, and has a length greater than 0.
        self._id: is an integer and is greater 0.
        self._username: is an alphanumeric string with a length greater than 0.
        self._extension: is a string of 3-5 digits greater than 0.
        self._department: has alphabets or spaces, and it's length is greater than 0.
    """

    __tablename__ = 'professor'

    _extension = Column(String(5), nullable=False)
    _department = Column(String(50), nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'professor',
        'concrete': True
    }

    @validates('_extension')
    def validExtension(self, key, extension=_extension):
        try:
            int(extension)
        except ValueError:
            raise InvalidExtensionError(extension)

        if not (2 < len(extension) < 6):
            raise InvalidExtensionError(extension)

        return extension

    @validates('_department')
    def validDepartment(self, key, department=_department):
        if not all(x.isalpha() or x.isspace() for x in department) or not (len(department) > 0):
            raise InvalidDepartmentError(department)
        return department

    @hybrid_property
    def extension(self):
        return self._extension

    @extension.setter
    def extension(self, extension):
        """
          Set the extension of the professor object.

          :param extension: Extension of the contact.

          pre:
            extension has alphabets or spaces, and it's length is greater than 0.

          post:
            self._extension has alphabets or spaces, and has a length greater than 0.
        """
        self._extension = extension

    @hybrid_property
    def department(self):
        return self._department

    @department.setter
    def department(self, department):
        """
          Set the department of the professor object.

          :param department: Department of the contact.

          pre:
            department has alphabets or spaces, and it's length is greater than 0.

          post:
            self._department has alphabets or spaces, and has a length greater than 0.
        """
        self._department = department

    @property
    def serialize(self):
        output = {}

        json = super(Professor, self).serialize

        for j in json.items():
            output[j[0]] = j[1]

        output['extension'] = self._extension
        output['department'] = self._department

        return output
