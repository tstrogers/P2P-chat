# first of all import the socket library
import socket            
import threading
from _thread import *
import time

thread_count=0
status_dict={}
#information_dict={}
 
socket_dict={}
# next create a socket object
s = socket.socket()        
print ("Socket successfully created")
 
# reserve a port on your computer in our
# case it is 12345 but it can be anything
port = 12394
 
# Next bind to the port
try:
  s.bind(('', port))    
  s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)            
  print ("socket binded to %s" %(port))
except socket.error as e:
  print(str(e))
 


def multi_threaded_client(c,addr):
  c.send(str.encode('Welcome to P2P chat! You are now online! Who would you like to chat with?'))

  time.sleep(30)
  while True:
    data = c.recv(1024).decode()
    data = data[1:]
    print('reply: ',data)
    if data in status_dict and status_dict[data] == "online" and c.getpeername() != data:
      try:
        c.send(str.encode('{} {} {}'.format(data, socket_dict[data], 50055)))
        print("Information successfully sent to client...")
        print("Listening for new connections...")
      except:
        raise Exception("Error sending msg to client")
    else:
      c.send(str.encode('{} {}'.format('Offline', data)))

      #data = c.recv(1024).decode()
    break
      


while True:
        #s.close()
        s.listen(5)    
        print ("socket is listening")           
        
        # a forever loop until we interrupt it or
        # an error occurs
        c, addr = s.accept()
        #try: 
       
        print ('Got connection from', addr )
        status_dict[addr[0]]= "online"
        socket_dict[addr[0]] = addr[1]
        print("status: ", status_dict)
        
      
        
        #CALL MLTIPLE CLINT FUNC HERE
        start_new_thread(multi_threaded_client, (c, addr, ))
        thread_count += 1
       