
try:
    from BytesIO import BytesIO
except ImportError:
    from io import BytesIO
from pyecore.resources import URI


class BytesURI(URI):

    def __init__(self, uri, text=None):
        super(BytesURI, self).__init__(uri)
        if text is not None:
            self.__stream = BytesIO(text)

    def getvalue(self):
        return self.__stream.getvalue()

    def create_instream(self):
        self.__stream = open(self.plain, 'rb')
        return self.__stream

    def create_outstream(self):
        self.__stream = BytesIO()
        return self.__stream
