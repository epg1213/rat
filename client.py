#!/usr/bin/python3
from sys import argv
import socket
import rsa
from cryptography.fernet import Fernet
MSGLEN=2048
from platform import system as find_system
from subprocess import check_output

class Linux:
  def ipconfig(self):
    return check_output(["ip", "a"]).decode('utf-8')

class Windows:
  def ipconfig(self):
    return check_output(["ipconfig"]).decode('utf-8')

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
    match find_system():
      case "Linux":
        self.system=Linux()
      case "Windows":
        self.system=Windows()
      case _:
        exit('OS not supported.')

  def send(self, message):
    msg=self.key.encrypt(str(message).encode('utf-8'))
    self.sock.send(msg)

  def send_text(self, bytes_array):
    self.send(len(bytes_array))
    for line in bytes_array:
      self.send(line)

  def receive(self):
    msg=self.sock.recv(MSGLEN)
    message=self.key.decrypt(msg).decode('utf-8')
    return message

  def wait_for_cmd(self):
    using=True
    while using:
      match self.receive():
        case "ip":
          self.send(self.system.ipconfig())
        case "ho":
          print("ho")
        case "exit":
          using=False
        case _:
          print("unknown")
    self.sock.close()

if __name__ == "__main__":
  try:
    port=int(argv[1])
    if port<1025 or port>65535:
      port=62832
  except:
    port=62832
  sock=SecureSocket(port=port)
  sock.wait_for_cmd()
  print("exit")
