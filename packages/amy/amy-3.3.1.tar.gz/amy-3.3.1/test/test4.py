from cryptography.fernet import Fernet

crypto = Fernet('9x6E0irEEI5BcVRPiavbbdSdJZwaHDegtIkRqH1QdzY='.encode())


e = crypto.encrypt('test'.encode()).decode()
e = crypto.decrypt(e.encode()).decode()
print(e)



