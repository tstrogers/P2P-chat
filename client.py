import socket
import sys
import threading
import time
import sqlite3

class chatter:

    ip = '10.0.0.188'

    def __init__(self,ip,sport,dport):
        self.ip = ip
        self.sport = sport
        self.dport = dport

        # punch hole
        # equiv: echo 'punch hole' | nc -u -p 50001 x.x.x.x 50002
        print('punching hole')


        print('\ngot peer')
        print('  ip:          {}'.format(ip))
        print('  source port: {}'.format(sport))
        print('  dest port:   {}\n'.format(dport))

        print('ready to exchange messages\n')



   
    def listen(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(('0.0.0.0', self.dport))

        while True:
            data = sock.recv(1024)
            print('\rpeer: {}\n> '.format(data.decode()), end='')
            if data == 'exit':
                sock.close()
                break

    def talk(self):
        con = sqlite3.connect("chatDB.db")
        cur = con.cursor()
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(('0.0.0.0', self.sport))
        for row in cur.execute("SELECT Message FROM Chats WHERE Sent = \"not sent\" AND IP = \"" + self.ip + "\""):
            sock.sendto(str.encode(row[0]), (self.ip, self.dport))
            cur.execute("INSERT INTO Chats VALUES(?,?,?)", (self.ip, row[0], 'sent'))
            con.commit()
        cur.execute("DELETE FROM Chats WHERE Sent = \"not sent\" AND IP = \"" + self.ip + "\"")
        con.commit()
        while True:
            msg = input('> ')
            sock.sendto(msg.encode(), (self.ip, self.dport))
            cur.execute("INSERT INTO Chats VALUES(?,?,?)", (self.ip, msg, 'sent'))
            con.commit()
            if msg == 'exit':
                sock.close()
                break

    def startChat(self):
        listener = threading.Thread(target=self.listen, daemon=True)
        listener.start()
        self.talk()
    
    def startOfflineChat(self):
        con = sqlite3.connect("chatDB.db")
        cur = con.cursor()

        while True:
            msg = input('> ')
            cur.execute("INSERT INTO Chats VALUES(?,?,?)", (self.ip,msg, 'not sent'))
            con.commit()
            if msg == 'exit':
                break



def main(argv):
    con = sqlite3.connect("chatDB.db")
    cur = con.cursor()
    peer_info = None
    s = socket.socket()
    port = 12394
    s.connect((chatter.ip,port))
    s.sendto(b'0', (chatter.ip,port))
    
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    while True:
        data = s.recv(1024).decode()
        print('data: ', data)
        msg = input("Enter the users IP address: ")
        s.sendto(msg.encode(), (chatter.ip, 12382))
        time.sleep(60)
        data = s.recv(1024).decode()
        print("data: ", data)
        if not data:
            raise Exception("No data was received")
        else:
            peer_info = data
            break
      
    if  peer_info.split(' ')[0] == 'Offline':
        ip =  peer_info.split(' ')[1]
        sport = 'offline'
        dport = 'offline'
    else:
        ip, sport, dport = peer_info.split(' ')
        sport = int(sport)
        dport = int(dport)

    print('\ngot peer')
    print('  ip:          {}'.format(ip))
    print('  source port: {}'.format(sport))
    print('  dest port:   {}\n'.format(dport))



    #sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    #sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    #sock.sendto(b'0', (ip, dport))

    if  peer_info.split(' ')[0] == 'Offline':
        print('This user is currently offline. Any messages sent will be saved and sent when they log on again')
    else:
        print('ready to exchange messages\n')

    
    chat = chatter(ip,sport,dport)#argv[0],argv[1],argv[2])
    if  peer_info.split(' ')[0] == 'Offline':
        chat.startOfflineChat()
    else:
        chat.startChat()



    # send messages
    # equiv: echo 'xxx' | nc -u -p 50002 x.x.x.x 50001

    #"""

if __name__ == "__main__":

    main(sys.argv[1:])