'''

    Isabela Server Project made by Miguel Marques and Paulo Cardoso
        The project was made in Linux, so we're not sure if
                        this will work in windows.

    All of this was made with Python 2.7.15rc1 and for GUI we used Tkinter.

    This file only has the client part of the project, don't forget
            to have isabella_layout.png in the folder. To run
                this file use python3 isabela_client.py

'''
import socket
import sys
import cmd
from _thread import *
import signal
import struct
from tkinter import *
import time
def substhreadserver():
    global text_subs
    global ssubs
    time.sleep(2)
    global subsport
    try:
        ssubs = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    except socket.error:
        print("Failed to connect the socket")
        sys.exit()
    try:
        ssubs.bind((host,subsport))
    except socket.error:

        print("Binding Failed")
        sys.exit()
    ssubs.listen()
    print("Subs Socket Created")
    subsconnection, subsaddr = ssubs.accept()
    subsconnection.send("CONNECTION CREATED".encode())
    while True:
        subsdata = subsconnection.recv(4096)
        if not subsdata:
            break
        reply = subsdata.decode()
        if (reply == "sss"):
            reply = ""
            text_subs.delete(0.0,END)
        text_subs.insert(END,reply)

def catch_ctrl_c(sig, frame):
    ignore()

def gotoserver():
    time.sleep(1)
    global subsport
    global output_info
    aux = s.recv(2)
    subsport = struct.unpack('!H',aux)[0]
    print("SUBSPORT --> {0}".format(subsport))
    while True:
        reply = s.recv(4096)
        print(reply.decode(),end="")
        if not reply:
            break
        if reply.decode() == "Exit\n":
            s.close()
            sys.exit()
        output_info.insert(END,reply)

def click():
    global output_info
    global text_input
    output_info.delete(0.0,END)
    var =text_input.get()+str("_")
    try:
        s.send(var.encode())
    except socket.error:
        print("Did not send successfully")
        s.close()
        sys.exit()
    text_input.delete(0,END)

def enter_key(event):
    click()

def leave():
    global janela
    global ssubs
    var = "3478GFDgu4w639_"
    s.send(var.encode())
    janela.destroy()
    s.close()
    ssubs.close()
    sys.exit()

def ignore():
    pass

def interface():
    global text_input
    global output_info
    global text_subs
    global janela
    janela = Tk()
    frame = Frame(master=janela, width=500, height=500, bg='#2C2C2C')
    janela.title("Isabela App")
    janela.configure(background = "#2C2C2C")
    janela.bind("<Return>",enter_key)
    janela.protocol("WM_DELETE_WINDOW", ignore)
    janela.resizable(width = False, height = False)
    isabella_layout = PhotoImage(file ="isabella_layout.png")
    Label(janela,text ="WELCOME TO ISABELA SERVER",bg = "#2C2C2C",fg="#33D3B3",font ="none 20 bold").grid(row = 0, column =1,sticky = N)
    Label(janela,text ="SUBSCRITIONS",bg = "#2C2C2C",fg="#33D3B3",font ="none 20 bold").grid(row = 1, column =0,sticky = S)
    Label(janela,image = isabella_layout, bg = "#2C2C2C").grid(row = 1, column =0,sticky = N)
    text_input = Entry(janela,width=30,bg = "white",font ="none 13 bold")
    text_input.grid(row=2,column=1,sticky=N)
    text_subs = Text(janela,width = 35,height=20,fg = "#2C2C2C",bg="#33D3B3",font ="none 10 bold")
    text_subs.grid(row=2,column=0,columnspan=1, rowspan=1,sticky = N)
    output_info = Text(janela,width = 50,height = 20,bg = "#2C2C2C",fg="#33D3B3", wrap = WORD,font ="none 15 bold")
    output_info.grid(row = 1, column =1,sticky = N)
    Button(janela, text = "SUBMIT",fg = "#2C2C2C",bg="#33D3B3",width=10,height=9,command = click,font ="none 17 bold").grid(row = 2, column =1,sticky = E,padx=70, pady=60)
    Button(janela, text = "EXIT",fg = "#2C2C2C",bg="#FF4945",width=10,height=9,command = leave,font ="none 17 bold").grid(row = 2, column =1,sticky = W,padx=70, pady=60)

    janela.mainloop()

if __name__ == '__main__':
    global subsport
    global output_info
    global text_input
    global LOGIN
    global text_subs
    global janela
    LOGIN = False
    host = "localhost"
    port = 8880
    signal.signal(signal.SIGINT, catch_ctrl_c)
    try:
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM);
    except socket.error:
        print("Failed to connect");
        sys.exit()
    print("Socket Created")
    try:
        remote_ip=socket.gethostbyname(host)
        print(remote_ip)
    except socket.gaierror:
        print("Hostname could not be resolved")
        sys.exit()
    print("IP Address: "+ remote_ip)
    try:
        s.connect((remote_ip,port))
    except ConnectionRefusedError:
        print("Please make sure the server is on")
        sys.exit()
    print("Socket connected to: "+host+" using IP "+ remote_ip)

    start_new_thread(interface,( ))
    start_new_thread(substhreadserver,( ))
    gotoserver()
    print("Socket fechado")
    s.close()
