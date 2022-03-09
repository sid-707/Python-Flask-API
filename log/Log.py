from modules.Singleton import Singleton
from datetime import datetime

class Log(metaclass=Singleton):
    """
      :param time: Time of the request.
      :type time: Datetime
      :param url: URL of the request
      :type url: String
      :param method: HTTP method of the request
      :type method: String

      pre:
        time: is a DateTime object.
        url: is an alphanumeric String with no spaces and is greater than 0.
        method: is a String that stores either GET or POST

      post:
        self._time: is a DateTime object.
        self._url: is a String with no spaces and is greater than 0. Stores NaN if url is invalid
        self._method: is a String that stores either GET or POST or NaN if method is invalid.
    """

    def __init__(self):
        """
          Construct the Log object.

          The constructor is empty since all values will be set/accessed using getters and setters.
          Being a Singleton class, the init method will be called only once and, therefore, subsequent
          values will have to be set/ accessed using getters and setters.

        """
        super().__init__()

    @classmethod
    def validTime(self, time):
        if not isinstance(time, datetime):
            print(time + ' is not a valid time. Storing current time.')
            return datetime.now()
        return time

    @classmethod
    def validURL(self, url):
        if not all(not x.isspace() for x in url) or not (len(url) > 0):
            print(url + ' is not a valid relative url.')
            return 'NaN'
        return url

    @classmethod
    def validMethod(self, method):
        if method not in ['GET', 'POST']:
            print(method + ' is not a valid HTTP Method. It must be either GET or POST.')
            return 'NaN'
        return method

    @property
    def time(self):
        return self._time

    @property
    def url(self):
        return self._url

    @property
    def method(self):
        return self._method

    @time.setter
    def time(self, time):
        """
          Set the time of the Log object.

          :param time: Time of the request.

          pre:
            time is a datetime object.

          post:
            self._time is a datetime object.
        """
        self._time = self.validTime(time)

    @url.setter
    def url(self, url):
        """
          Set the url of the Log object.

          :param url: URL of the request.

          pre:
            url is alphanumeric and has no spaces. It's length is greater than 0.

          post:
            self._url is alphanumeric and has no spaces. It's length is greater than 0. It can be NaN if url is not
                    valid
        """
        self._url = self.validURL(url)

    @method.setter
    def method(self, method):
        """
          Set the method of the Log object.

          :param method: Method of the request.

          pre:
            method is a String that stores either GET or POST

          post:
            self._method is a String that stores either GET or POST or NaN.
        """
        self._method = self.validMethod(method)
