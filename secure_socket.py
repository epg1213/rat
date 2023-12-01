#!/usr/bin/python3
import socket
import rsa
from cryptography.fernet import Fernet
SEND_MSG_LEN=2048
RECV_MSG_LEN=4096
from time import sleep

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

  def send(self, message, as_bytes=False):
    if as_bytes==False:
      message=str(message).encode('utf-8')
    # split message in a list of packets with max size SEND_MSG_LEN
    packs=[]
    while len(message) > SEND_MSG_LEN:
      packs.append(message[:SEND_MSG_LEN])
      message=message[SEND_MSG_LEN:]
    if len(message)>0:
      packs.append(message)
    # send packets one by one until sending '/' to terminate
    for pack in packs:
      msg=self.key.encrypt(pack)
      self.connection.send(msg)
      sleep(0.1)
    self.connection.send(self.key.encrypt(b'/'))

  def receive(self, as_bytes=False):
    # get packets one by one until getting '/' to terminate
    to_recv=[]
    ended=False
    while not ended:
      msg=self.connection.recv(RECV_MSG_LEN)
      pack=self.key.decrypt(msg)
      ended=pack==b'/'
      if not ended:
        to_recv.append(pack)
    # join all packets together to get the message
    message=b''.join(to_recv)
    if as_bytes:
      return message
    return message.decode('utf-8')

  def send_file(self, filename_src, filename_dst):
    content=b''
    with open(filename_src, 'rb') as file:
      content=file.read()
    self.send(filename_dst)
    self.send(content, as_bytes=True)

  def receive_file(self):
    filename=self.receive()
    content=self.receive(as_bytes=True)
    with open(filename, 'wb') as file:
      file.write(content)

  def disconnect(self):
    if not self.connected:
      return
    try:
      self.send("exit")
    except BrokenPipeError:
      pass
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
