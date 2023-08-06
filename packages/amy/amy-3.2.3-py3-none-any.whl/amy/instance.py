from threading import Thread

def passFunc(self, *args, **kwargs): pass

def initSuper(self, cls, *args, **kwargs): cls.__init__(self, *args, **kwargs)

def passDefault(cls, name, func=passFunc):
    if not hasattr(cls, name):
        setattr(cls, name, func)

# def startThead(instance, function):
#     instance.__thread = Thread(target=function)
#     instance.__thread.start()


# def stopThread(self, instance):
#     if hasattr(instance, '__thread'):
#         instance.__thread.join()


def instance(cls):

    setattr(cls, '__init__', passFunc)

    passDefault(cls, 'onCreate')
    passDefault(cls, 'onLoad')
    passDefault(cls, 'onAuth')
    passDefault(cls, 'isAuthorized')
    passDefault(cls, 'onStart')
    passDefault(cls, 'onStop')
    passDefault(cls, 'sendMessage')
    passDefault(cls, 'onDelete')

    return cls


@instance
class Instance:
    pass
