#!/usr/bin/python3
import socket
import rsa
from cryptography.fernet import Fernet
MSGLEN=2048

class SecureSocket:

  def __init__(self, host="127.0.0.1", port=62832):
    self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
      self.sock.connect((host, port))
    except:
      exit("Server unreachable.")
    connection_key=rsa.PublicKey.load_pkcs1(self.sock.recv(2048))
    key = Fernet.generate_key()
    encrypted_key=rsa.encrypt(key, connection_key)
    self.sock.send(encrypted_key)
    self.key = Fernet(key)

  def send(self, message):
    msg=self.key.encrypt(str(message).encode('utf-8'))
    self.sock.send(msg)

  def receive(self):
    msg=self.sock.recv(MSGLEN)
    message=self.key.decrypt(msg).decode('utf-8')
    return message

  def wait_for_cmd(self):
    using=True
    while using:
      match self.receive():
        case "hi":
          print("hi")
        case "ho":
          print("ho")
        case "exit":
          print("exit")
          using=False
        case _:
          print("unknown")

sock=SecureSocket()
sock.wait_for_cmd()
