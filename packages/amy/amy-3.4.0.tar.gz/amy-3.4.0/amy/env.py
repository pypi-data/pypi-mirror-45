import os

PRODUCTION = os.environ.get('PRODUCTION', False)

AMY = os.environ.get('AMY', 'amy')
AMY_Q = os.environ.get('AMY_Q', AMY)
AMY_Q_HOST = os.environ.get('AMY_Q_HOST', '159.89.24.207')

AMY_Q_IN = os.environ.get('AMY_Q_IN', 'messages_in')

AMY_HASHKEY = os.environ.get('AMY_HASHKEY','9x6E0irEEI5BcVRPiavbbdSdJZwaHDegtIkRqH1QdzY=')
