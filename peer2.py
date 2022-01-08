import socket
import os
import threading
from tkinter import *
from tkinter import filedialog


def receive():
    size = 135
    while 1:
        host = "127.0.0.1"
        port = 5001
        SEPARATOR = "<SEPARATOR>"
        tao_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tao_socket.bind((host, port))
        tao_socket.listen(5)
        ketnoi, diachi = tao_socket.accept()
        received_data = ketnoi.recv(4096).decode()
        filename, filesize = received_data.split(SEPARATOR)
        filename = os.path.basename(filename)
        filesize = int(filesize)

        with open(filename, "wb") as f:
            while True:
                bytes_read = ketnoi.recv(4096)
                if not bytes_read:
                    break
                f.write(bytes_read)

        label = Label(peer.frame4, text=host, font="Times 13", bg="white").place(
            y=size, x=50
        )
        label1 = Label(peer.frame4, text=filename, font="Times 13", bg="white").place(
            y=size, x=180
        )
        label2 = Label(peer.frame4, text="Received", font="Times 13", bg="white").place(
            y=size, x=430
        )
        size = size + 33
        ketnoi.close()
        tao_socket.close()


def send_():
    host = "127.0.0.1"
    port = 5000
    tao_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tao_socket.connect((host, port))
    SEPARATOR = "<SEPARATOR>"
    filename = peer.entry1.get()

    filesize = os.path.getsize(filename)
    tao_socket.send(f"{filename}{SEPARATOR}{filesize}".encode())
    with open(filename, "rb") as f:
        while True:
            bytes_read = f.read(4096)
            if not bytes_read:
                break
            tao_socket.sendall(bytes_read)

    peer.entry1.delete(0, 100)
    filename1 = os.path.basename(filename)

    label = Label(peer.frame5, text=host, font="Times 13", bg="white").place(
        y=peer.size1, x=50
    )
    label1 = Label(peer.frame5, text=filename1, font="Times 13", bg="white").place(
        y=peer.size1, x=180
    )
    label2 = Label(peer.frame5, text="Sended", font="Times 13", bg="white").place(
        y=peer.size1, x=430
    )
    peer.size1 = peer.size1 + 33
    tao_socket.close()


win = Tk()
win.title("Peer 2")


def browser_btt():
    filename = filedialog.askopenfilename()
    peer.entry1.insert(0, filename)


class Peer(Frame):
    size1 = 353

    def __init__(self, master):
        super().__init__(master)
        ###################
        self.frame1 = Frame(self).pack()
        self.label1 = Label(
            self.frame1, text="IP Address: 127.0.0.1", font="Times 15"
        ).place(width=200, height=30)
        self.label2 = Label(
            self.frame1, text="Port_receive: 5001", font="Times 15"
        ).place(width=200, height=30, x=215)
        self.label3 = Label(self.frame1, text="Port_send: 5000", font="Times 15").place(
            width=200, height=30, x=410
        )
        ####################
        self.frame2 = Frame(self).pack()
        self.filename = StringVar()
        self.label4 = Label(self.frame2, text="File name", font="Times 15").place(
            width=105, height=30, y=50
        )
        self.entry1 = Entry(self.frame2, font="Times 13", textvariable=self.filename)
        self.entry1.place(width=350, height=30, y=50, x=100)
        self.btt1 = Button(
            self.frame2,
            text="Browser",
            font="Times 15",
            bg="blue",
            fg="white",
            command=browser_btt,
        ).place(width=100, height=30, y=50, x=460)
        ####################
        self.frame3 = Frame(self).pack()
        self.can = Canvas(self.frame3, bg="white", width=500, height=200)
        self.can.place(y=100, x=45)
        self.label5 = Label(
            self.frame3, text="IP Address", font="Times 13", bg="white"
        ).place(y=108, x=50)
        self.label5 = Label(
            self.frame3, text="File name", font="Times 13", bg="white"
        ).place(y=108, x=180)
        self.label5 = Label(
            self.frame3, text="Status(receive)", font="Times 13", bg="white"
        ).place(y=108, x=430)
        ####################
        self.frame5 = Frame(self).pack()
        self.can = Canvas(self.frame5, bg="white", width=500, height=200)
        self.can.place(y=320, x=45)
        self.label6 = Label(
            self.frame5, text="IP Address", font="Times 13", bg="white"
        ).place(y=328, x=50)
        self.label6 = Label(
            self.frame5, text="File name", font="Times 13", bg="white"
        ).place(y=328, x=180)
        self.label6 = Label(
            self.frame5, text="Status(send)", font="Times 13", bg="white"
        ).place(y=328, x=430)
        ####################
        self.frame4 = Frame(self).pack()
        self.btt2 = Button(
            self.frame4,
            text="Send",
            font="Times 15",
            bg="blue",
            fg="white",
            command=send_,
        ).place(y=550, x=258)


win.geometry("600x600")
win.resizable(width=False, height=False)
peer = Peer(win)
receive_thread = threading.Thread(target=receive)
receive_thread.start()
win.mainloop()

