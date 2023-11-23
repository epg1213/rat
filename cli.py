#!/usr/bin/python3
import socket
import rsa
from cryptography.fernet import Fernet

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect(("127.0.0.1", 62832))

public_key=rsa.PublicKey.load_pkcs1(s.recv(2048))
print(public_key)
# gen & send symetric key via socket
