import tkinter as tk
import socket

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.server_address = ('', 12345)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.pack()
        self.config()
        self.create_widgets()
        self.connectToServer()

    def config(self):
        root.minsize(768,432)
        root.geometry('768x432')

    def send(self):
        self.message = str(self.entry_widget1.get())
        self.message = self.message.encode() + '\n'.encode()
        self.sock.sendall(self.message)
        self.entry_widget1.delete(0, 'end')
        self.entry_widget1.insert(0, '')

    def create_widgets(self):
        self.entry_widget1 = tk.Entry(self)
        self.entry_widget1.insert(0, '')
        self.entry_widget1.pack(side='bottom')
        self.send = tk.Button(self, text='SEND', fg='blue',
                              command=self.send)
        self.send.pack(side='top')

    def connectToServer(self):
        self.sock.connect(self.server_address)
        print('connected')

root = tk.Tk()
app = Application(master=root)
app.mainloop()
