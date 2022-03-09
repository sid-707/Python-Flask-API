class InvalidNameError(Exception):
  def __init__(self, input):
    super().__init__(input)
    self.__input = input
  
  def __str__(self):
    return repr(self.__input + " is not a valid name."
                             + " It cannot have special characters and punctuation marks although spaces are allowed."
                             + " It must also be at least 1 letter.")
