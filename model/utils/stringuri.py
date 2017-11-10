from StringIO import StringIO
from pyecore.resources import URI

class StringURI(URI):

    def __init__(self, uri, text=None):
        super(StringURI, self).__init__(uri)
        if text is not None:
            self.__stream = io.StringIO(text)

    def getvalue(self):
        return self.__stream.getvalue()

    def create_instream(self):
        self.__stream = open(self.plain, 'rb')
        return self.__stream

    def create_outstream(self):
        self.__stream = StringIO()
        return self.__stream