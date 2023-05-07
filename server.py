import socket            
import threading
from _thread import *
import time
import loginpage as app

thread_count=0
status_dict={}
friends_dict={}
port_dict={}
socket_dict={}

s = socket.socket()        
print ("Socket successfully created")
 
port = 12345
 
try:
  s.bind(('', port))    
  s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)            
  print ("socket binded to %s" %(port))
except socket.error as e:
  print(str(e))
 


def multi_threaded_client(c,addr):
  print("addr: ", addr)
  time.sleep(10)
  username = c.recv(1024).decode()
  username = username[1:]
  port_dict[username] = addr[1]
  friends_dict[username] = "Online"
  data = "0"
  while True:
    while True:
      data = c.recv(1024).decode()
      if not data:
        continue
      if data!="0":
        break
    if data in friends_dict and friends_dict[data] == "Online":
      try:
        c.send(str.encode(str(addr[0])+" "+str(port_dict[data])+" "+"50055"+" "+str(friends_dict[data])))
        print("Information successfully sent to client...")
        print("Listening for new connections...")
      except:
        raise Exception("Error sending msg to client")
    else:
      c.send(str.encode('Offline'))
    break
      


while True:
        s.listen(5)    
        print ("socket is listening")           
        
        c, addr = s.accept()
       
        print ('Got connection from', addr )
        status_dict[addr[0]]= "online"
        socket_dict[addr[1]] = "online"
        
        #CALL MLTIPLE CLINT FUNC HERE
        start_new_thread(multi_threaded_client, (c, addr, ))
        thread_count += 1
       
       
