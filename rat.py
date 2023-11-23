#!/usr/bin/python3
import socket
import rsa
from cryptography.fernet import Fernet

def create_socket(ip, port):
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.setblocking(False)
  s.settimeout(0.5)
  s.bind((ip, port))
  s.listen()
  print("[*] Listening on 62832...")
  return s

if __name__ == "__main__":
  public_key, private_key=rsa.newkeys(2048)
  s = create_socket("127.0.0.1", 62832)
  running=True
  try:
    while running:
      try:
        client_socket, client_address = s.accept()
        print(client_address)
        client_socket.send(public_key.save_pkcs1())

        print("[+] Agent recieved !")
        encrypted_key=client_socket.recv(2048)
        client_fernet=rsa.decrypt(encrypted_key, private_key)
        print(client_fernet)
      except Exception as e:
        pass
  except KeyboardInterrupt:
    print("\nServer stopped.")
