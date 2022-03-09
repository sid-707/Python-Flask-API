class InvalidDepartmentError(Exception):
    def __init__(self, input):
        super().__init__(input)
        self.__input = input

    def __str__(self):
        return repr(self.__input + " is not a valid department.")
