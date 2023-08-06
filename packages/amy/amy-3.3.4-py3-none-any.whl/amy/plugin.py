from .env import *
from .instance import Instance
from .message import Message
from . import actions
from threading import Thread
import json
from cryptography.fernet import Fernet
import datetime
import types
import asyncio

from kombu import Connection, Queue
from kombu.mixins import ConsumerProducerMixin


# try catcher for errors in funcs
def onError(code=400, message='Error'):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                res = func(*args, **kwargs)
                return res
            except Exception as error:
                status = statusMessage(code, message)
                print(f'Error-Python: {error}')
                print(f'Error-Status: {status}')
                return status
        return wrapper
    return decorator


def statusMessage(code=200, message='Success', payload={}):
    if payload != {}:
        payload = {'info': payload}

    return {
        'status': code,
        'message': message,
        **payload
    }


class Listner(ConsumerProducerMixin):
    def __init__(self, conn, cb, name):
        self.connection = conn
        self.cb = cb
        self.name = name

    def get_consumers(self, Consumer, channel):
        return [Consumer(
            queues=[Queue(self.name)],
            on_message=self.cb,
            accept={'application/json'},
            prefetch_count=1)]

    def sendStatus(self, properties, payload):
        self.producer.publish(
            payload,
            exchange='', routing_key=properties['reply_to'],
            correlation_id=properties['correlation_id'],
            serializer='json',
            retry=True,
        )


class Plugin:
    __instances = {}
    conn = Connection(AMY_Q_HOST)
    __crypto = Fernet(AMY_HASHKEY)

    def publishMessage(self, message: Message):
        message.setPlatform(self.name)
        print(f'PUBLISHING {message}')
        self.conn.SimpleQueue('messages_in').put(message.toDict())
        return message

    def __init__(self, name='plugin', instanceCls=Instance):
        self.name = name.lower()
        self.__instanceCls = instanceCls
        self.startListener()
        self.conn.SimpleQueue('plugins').put(
            {'name': self.name, 'status': 'online'})
        print('plugin running')

    def startListener(self):
        if not hasattr(self, '__listener'):
            self.__listner = Listner(
                self.conn, self.request_handler, self.name)
        self.__listner.should_stop = False
        self.__listner_thread = Thread(
            target=self.__listner.run)
        self.__listner_thread.start()
        print('listen on q')

    def stopListener(self):
        if hasattr(self, '__listner_thread'):
            self.__listner.should_stop = True
            self.__listner_thread.join()

    def request_handler(self, message):

        try:
            username = message.headers.get('username', None)

            if username:
                action = message.headers.get('action', None)

                if action == actions.CREATE_USER:
                    session = message.payload.get('session', None)
                    statusCode = self.create(username, session)

                elif action == actions.AUTHORIZE_USER:
                    statusCode = self.authorize(
                        username, message.payload['token'])

                elif action == actions.SEND_MESSAGE:
                    statusCode = self.sendMessage(
                        username, message.payload['message'])

                elif action == actions.STATUS_USER:
                    statusCode = self.status(username)

                elif action == actions.REMOVE_USER:
                    statusCode = self.delete(username)

                print(
                    f'action {action} on {username} returns {statusCode}')

                self.__listner.sendStatus(message.properties, statusCode)

            message.ack()

        except Exception as e:
            print(f'Error in Request Handler {e}')
            message.ack()

    @classmethod
    def __encrypt(cls, unhashstring: str):
        return cls.__crypto.encrypt(unhashstring.encode()).decode()

    @classmethod
    def __decrypt(cls, hashedstring: str):
        return cls.__crypto.decrypt(hashedstring.encode()).decode()

    @onError(500, 'failed to create User')
    def create(self, username, session):
        if username not in self.__instances:
            self.__instances[username] = self.__instanceCls()
            session = self.__decrypt(session) if session else None
            self.__instances[username].onCreate(self, username, session)
            if self.__instances[username].isAuthorized():
                self.start(username)
        return self.status(username)

    @onError(401, 'failed to autheticate User')
    def authorize(self, username, token):
        if username in self.__instances:
            session = self.__instances[username].onAuth(self, token)
            session = self.__encrypt(session) if session else None
            res = {**self.isAuth(username), "session": session}
            if(res['status'] == 202):
                self.start(username)
            return res
        return statusMessage(404, f'User {username} not found')

    @onError(500, 'failed to start User')
    def start(self, username):
        if username in self.__instances:
            self.__instances[username].onStart(self)
            return statusMessage(200, f'User {username} started')
        return statusMessage(404, f'User {username} not found')

    @onError(500, 'failed to stop User')
    def stop(self, username):
        if username in self.__instances:
            self.__instances[username].onStop()
            return statusMessage(200, f'User {username} stopped')
        return statusMessage(404, f'User {username} not found')

    @onError(500, 'failed to delete User')
    def delete(self, username):
        if username in self.__instances:
            self.stop(username)
            self.__instances[username].onDelete(self)
            del self.__instances[username]
            return statusMessage(204, f'User {username} deleted')
        return statusMessage(404, f'User {username} not found')

    @onError(500, 'failed to send Message')
    def sendMessage(self, username, message):
        if username in self.__instances:
            self.__instances[username].onSendMessage(self, message)
            return statusMessage(200, f'{username} sended a message')
        return statusMessage(404, f'User {username} not found')

    @onError(500, 'failed to send status')
    def status(self, username):

        lastsatus = statusMessage(400, f'Instance {username} not running')

        if username in self.__instances:
            arr = []

            arr.append(self.isCreated(username))
            arr.append(self.isAuth(username))
            arr.append(self.isRunning(username))

            for message in arr:
                if 199 < message['status'] < 300:
                    lastsatus = message

            return lastsatus
        return statusMessage(404, f'User {username} not found')

    @onError(400, 'failed to check Status Running')
    def isRunning(self, username):
        return statusMessage(202, f'{username} is running') if hasattr(self.__instances[username], '_Plugin__thread') else statusMessage(400, f'{username} is not running')

    @onError(401, 'failed autheticate Process')
    def isAuth(self, username):
        return statusMessage(202, f'{username} logged in') if self.__instances[username].isAuthorized() else statusMessage(401, f'{username} failed to authenticate')

    @onError(400, 'failed to read created user')
    def isCreated(self, username):
        return statusMessage(201, f'{username} created') if username in self.__instances else statusMessage(404, f'{username} not created')

    @staticmethod
    def startThread(instance, function):
        instance.__thread = Thread(target=function)
        instance.__thread.start()

    @staticmethod
    def stopThread(instance):
        if hasattr(instance, '__thread'):
            instance.__thread.join()
