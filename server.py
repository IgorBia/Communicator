import socket, threading

HOST = ''
PORT = 12345

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(4)
clients = []
lock = threading.Lock()


class chatServer(threading.Thread):
    def __init__(self, info):
        threading.Thread.__init__(self)
        self.socket = info[0]
        self.address= info[1]
    def send(self, x):
        for c in clients:
            c.socket.send(x)
    def run(self):
        lock.acquire()
        clients.append(self)
        lock.release()
        id = str(self.address[1])
        ide = id.encode()
        print(id, 'connected')
        self.send((id+' connected\r\n').encode())
        self.send(ide+b'!\r\nType CTRL + ] in your telnet app and type:\r\n> mode line\r\n> toggle crlf\r\n\r\n')
        while True:
            data = self.socket.recv(1024)
            if not data:
                break
            self.send(ide+b'> '+data)
        self.socket.close()
        lock.acquire()
        clients.remove(self)
        lock.release()
        print(self.address, 'disconnected')
        self.send((id+' disconnected\r\n').encode())
try:
    while True:
        chatServer(s.accept()).start()
finally:
    s.close()
