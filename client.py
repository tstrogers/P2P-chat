import socket
import sys
import threading
import time
import sqlite3
import PySimpleGUI as sg
import loginpage as app

class chatter:

    contact_name = ""
    ip = ''
    global_status = ""
    global_dport = None


    def __init__(self,ip,sport,dport):
        self.ip = ip
        self.sport = sport
        self.dport = dport


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
global_dport = None
global_status = ""
s = socket.socket()
def connect_to_server():
    port = 12345
    s.connect((chatter.ip,port))
    s.sendto(b'0', (chatter.ip,port))
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

def send_name_to_server(name):
    msg = name
    s.sendto(msg.encode(), (chatter.ip, 12382))

def listen(dport):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(('0.0.0.0', dport))

        while True:
            data = sock.recv(1024)
            print('\rpeer: {}\n> '.format(data.decode()), end='')
            if data == 'exit':
                sock.close()
                break

def receive_peer_info():
    data = s.recv(1024).decode()
    if data == "Offline":
        global global_status
        global_status = "Offline"

    else:
        ip, sport, dport, status = data.split(' ')
        sport = int(sport)
        dport = int(dport)
        print("ip: ", ip)
        print("sport: ", sport)
        print("dport: ", dport)
        print("status: ", status)

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(('0.0.0.0', sport))
        sock.sendto(b'0', (ip, dport))

        print('ready to exchange messages\n')
        listener = threading.Thread(target=listen, args=(dport,), daemon=True);
        listener.start()

        #sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        #sock.bind(('0.0.0.0', dport))

        while True:
            msg = input('> ')
            sock.sendto(msg.encode(), (ip, sport))


def main(argv):
    con = sqlite3.connect("chatDB.db")
    cur = con.cursor()
    peer_info = None

    app.start()
    
    
if __name__ == "__main__":

     main(sys.argv[1:])
