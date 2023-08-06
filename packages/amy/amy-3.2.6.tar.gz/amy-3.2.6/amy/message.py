import datetime
import types

class Message:
    '''
    Message class
    @return: Message builder
    '''

    def __init__(self, platform = 'plugin', content = '', sender = '', channel = '', datetime = datetime.datetime.now(), user = '', out = False):
        self.platform = platform
        self.content = content
        self.sender = sender
        self.channel = channel
        self.datetime = datetime
        self.user = user
        self.out = out

    def setPlatform(self, val):
        self.platform = str(val).lower()
        return self

    def setContent(self, val):
        self.content = str(val)
        return self

    def setSender(self, val):
        self.sender = str(val)
        return self

    def setChannel(self, val):
        self.channel = str(val)
        return self

    def setDatetime(self, val):
        #datetime.datetime.fromtimestamp(message_object.timestamp)
        self.datetime = val
        return self

    def setUser(self, val):
        self.user = str(val)
        return self

    def setOut(self, val):
        self.out = bool(val)
        return self

    def toDict(self):
        return self.__dict__