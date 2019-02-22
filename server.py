#!/usr/bin/env python3

# MIT License

# Copyright (c) 2019 Nircek

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# inspired by https://stackoverflow.com/q/6487772/6732111
import socket
from threading import Thread, Lock

HOST = ''
PORT = 12345

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(4)
clients = []
lock = Lock()

class chatServer(Thread):
    def __init__(self, info):
        Thread.__init__(self)
        self.socket  = info[0]
        self.address = info[1]
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
            data = self.socket.recv(10240)
            if not data:
                break
            self.send(ide+b'> '+data)
        self.socket.close()
        lock.acquire()
        clients.remove(self)
        lock.release()
        print(id, 'disconnected')
        self.send((id+' disconnected\r\n').encode())

try:
    while True:
        chatServer(s.accept()).start()
finally:
    s.close()
