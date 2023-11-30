#!/usr/bin/python3
import socket
import rsa
from cryptography.fernet import Fernet
MSGLEN=4096

HOSTNAME=socket.gethostname()

# socket class, parent for Server and Client, should not be instantiated by itself
class Socket:
  def __init__(self, host, port):
    self.host = host
    self.port = port
    self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.connected = False

  def __str__(self):
    return f"secure socket at ({self.host}:{self.port})"

  def send(self, message):
    msg=self.key.encrypt(str(message).encode('utf-8'))
    self.connection.send(msg)

  def receive(self):
    msg=self.connection.recv(MSGLEN)
    message=self.key.decrypt(msg).decode('utf-8')
    return message

  def disconnect(self):
    if not self.connected:
      return
    self.send("exit")
    self.connection.close()
    self.connected = False

class Server(Socket):
  def __init__(self, host="127.0.0.1", port=62832):
    super(Server, self).__init__(host, port)
    
    self.public_key, self.private_key = rsa.newkeys(2048)
    self.sock.bind((host, port))
    self.sock.listen()
    print(f"[*] Listening on {port}...")

  def accept_client(self):
    self.connection, client_address = self.sock.accept()
    self.connection.send(self.public_key.save_pkcs1())
    self.key=Fernet(rsa.decrypt(self.connection.recv(2048), self.private_key))
    self.connected = True
  
  def stop(self):
    self.disconnect()
    self.sock.close()

class Client(Socket):
  def __init__(self, host="127.0.0.1", port=62832):
    super(Client, self).__init__(host, port)
    
    self.sock.connect((host, port))
    self.connection=self.sock
    self.connected = True
    
    connection_key=rsa.PublicKey.load_pkcs1(self.connection.recv(2048))
    key = Fernet.generate_key()
    encrypted_key=rsa.encrypt(key, connection_key)
    self.connection.send(encrypted_key)
    self.key = Fernet(key)

  def get_params(self):
    return self.receive().split(" ")
