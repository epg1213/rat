#!/usr/bin/python3
import socket
import rsa
from cryptography.fernet import Fernet

class SecureSocket:
  def __init__(self, sock=None, host="127.0.0.1", port=62832):
    if sock is None:
      self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    else:
      self.sock = sock
    try:
      self.sock.connect((host, port))
    except:
      exit("Server unreachable.")

    connection_key=rsa.PublicKey.load_pkcs1(self.sock.recv(2048))
    key = Fernet.generate_key()
    print(key)
    encrypted_key=rsa.encrypt(key, connection_key)
    self.sock.send(encrypted_key)
    self.key = Fernet(key)

  def send(self, message):
    print(message)

sock=SecureSocket()
sock.send('Hello, World !')
