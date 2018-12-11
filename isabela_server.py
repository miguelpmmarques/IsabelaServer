'''

	Isabela Server Project made by Miguel Marques and Paulo Cardoso
		The project was made in Linux, so we're not sure if
						this will work in windows.

	All of this was made with Python 2.7.15rc1 and for GUI we used Tkinter.

	This file only has the server part of the project, don't forget to run
				this file with python3 isabela_server.py

'''
import socket
import sys
from _thread import *
import time
import signal
import random
import requests
import struct


class User:

    SUBS_calls_duration = False
    SUBS_calls_missed = False
    SUBS_calls_made = False
    SUBS_calls_received = False
    SUBS_sms_received = False
    SUBS_sms_send = False

    def __init__(self,ide,tipo,activity,calls_duration,calls_missed,calls_made,calls_received,department,location,sms_received,sms_send):
        self.ide = ide
        self.tipo = tipo
        self.activity = activity
        self.calls_duration = calls_duration
        self.calls_missed = calls_missed
        self.calls_made = calls_made
        self.calls_received = calls_received
        self.department = department
        self.location = location
        self.sms_received = sms_received
        self.sms_send = sms_send

    def do_subscription(self,atual_avg,ssubs):

        if ((self.SUBS_sms_send and (self.average.sms_send != atual_avg.sms_send)) or (self.SUBS_sms_received and (self.average.sms_received != atual_avg.sms_received)) or (self.SUBS_calls_received and (self.average.calls_received != atual_avg.calls_received)) or (self.SUBS_calls_made and (self.average.calls_made != atual_avg.calls_made)) or (self.SUBS_calls_duration and (self.average.calls_duration != atual_avg.calls_duration)) or (self.SUBS_calls_missed and (self.average.calls_missed != atual_avg.calls_missed))):
            try:
                ssubs.send("sss".encode())
            except BrokenPipeError as e:
                return False

        if self.SUBS_calls_duration:
            if self.average.calls_duration != atual_avg.calls_duration:
                var = "\nAverage calls duration changed to "+str(round(atual_avg.calls_duration,2))+" [AVERAGE CALLS DURATION SUBSCRITION]\n "
                try:
                    ssubs.send(var.encode())
                except BrokenPipeError as e:
                    return False
        if self.SUBS_calls_missed:
            if self.average.calls_missed != atual_avg.calls_missed:
                var = "\nAverage calls missed changed to "+str(round(atual_avg.calls_missed,2))+" [AVERAGE CALLS MISSED SUBSCRITION]\n "
                try:
                    ssubs.send(var.encode())
                except BrokenPipeError as e:
                    return False
        if self.SUBS_calls_made:
            if self.average.calls_made != atual_avg.calls_made:
                var = "\nAverage calls made changed to "+str(round(atual_avg.calls_made,2))+" [AVERAGE CALLS MADE SUBSCRITION]\n "
                try:
                    ssubs.send(var.encode())
                except BrokenPipeError as e:
                    return False
        if self.SUBS_calls_received:
            if self.average.calls_received != atual_avg.calls_received:
                var = "\nAverage calls Received changed to "+str(round(atual_avg.calls_received,2))+" [AVERAGE CALLS RECEIVED SUBSCRITION]\n "
                try:
                    ssubs.send(var.encode())
                except BrokenPipeError as e:
                    return False
        if self.SUBS_sms_received:
            if self.average.sms_received != atual_avg.sms_received:
                var = "\nAverage sms received changed to "+str(round(atual_avg.sms_received,2))+" [AVERAGE SMS RECEIVED SUBSCRITION]\n "
                try:
                    ssubs.send(var.encode())
                except BrokenPipeError as e:
                    return False
        if self.SUBS_sms_send:
           if self.average.sms_send != atual_avg.sms_send:
                var = "\nAverage sms send changed to "+str(round(atual_avg.sms_send,2))+" [AVERAGE SMS RECEIVED SUBSCRITION]\n "
                try:
                    ssubs.send(var.encode())
                except BrokenPipeError as e:
                    return False

        self.average = atual_avg
        return True

    def setAverage(self,average):
        self.average = average

    def displaySubscrition(self,reply,connection):
        connection.send("\n\n\n\tChoose your subscrition:\n".encode())
        connection.send("\n\t1 - Calls Duration\t\t".encode())
        if self.SUBS_calls_duration == False:
            connection.send("[NOT SUBSCRIBED]".encode())
        else:
            connection.send("[SUBSCRIBED]".encode())
        connection.send("\n\t2 - Calls Missed  \t\t".encode())
        if self.SUBS_calls_missed == False:
            connection.send("[NOT SUBSCRIBED]".encode())
        else:
            connection.send("[SUBSCRIBED]".encode())
        connection.send("\n\t3 - Calls Made      \t\t".encode())
        if self.SUBS_calls_made == False:
            connection.send("[NOT SUBSCRIBED]".encode())
        else:
            connection.send("[SUBSCRIBED]".encode())
        connection.send("\n\t4 - Calls Received \t\t".encode())
        if self.SUBS_calls_received == False:
            connection.send("[NOT SUBSCRIBED]".encode())
        else:
            connection.send("[SUBSCRIBED]".encode())
        connection.send("\n\t5 - Sms Received \t\t".encode())
        if self.SUBS_sms_received == False:
            connection.send("[NOT SUBSCRIBED]".encode())
        else:
            connection.send("[SUBSCRIBED]".encode())
        connection.send("\n\t6 - Sms Send      \t\t".encode())
        if self.SUBS_sms_send == False:
            connection.send("[NOT SUBSCRIBED]".encode())
        else:
            connection.send("[SUBSCRIBED]".encode())
        connection.send("\n\t7 - EXIT".encode())

    def displayCallSmsInfo(self):
        return "\n\t\tAVERAGE\n\tCalls Duration -> "+str(self.calls_duration)+"\n\tCalls Missed -> "+str(self.calls_missed)+"\n\tCalls Made -> "+str(self.calls_made)+"\n\tCalls Received -> "+str(self.calls_received)+"\n\tSms Received -> "+str(self.sms_received)+"\n\tSms Send -> "+str(self.sms_send)+"\n"

    def displayEveryting(self):
        return "\n\tID -> "+self.ide+"\n\tType -> "+self.tipo+"\n\tActivity -> "+self.activity+"\n\tCalls Duration -> "+str(self.calls_duration)+"\n\tCalls Missed -> "+str(self.calls_missed)+"\n\tCalls Made -> "+str(self.calls_made)+"\n\tCalls Received -> "+str(self.calls_received)+"\n\tDepartment -> "+self.department+"\n\tLocation -> "+self.location+"\n\tSms Received -> "+str(self.sms_received)+"\n\tSms Send -> "+str(self.sms_send)

def catch_ctrl_c(sig, frame):
	global all_sockets
	print('--> CTRL C pressed!\nIsabela server is closing')
	for socket in all_sockets:
		socket.close();
	sys.exit()

def readapi(url,headers,lista):
    r = requests.get(url, headers=headers)
    data = r.json()
    conta = 0
    avgcalls_duration = 0
    avgcalls_missed = 0
    avgcalls_made = 0
    avgcalls_received = 0
    avgsms_received = 0
    avgsms_send = 0
    for dic in data:
        conta += 1
        try:
            ID=dic['id']
        except KeyError as name:
            ID = "none"
        try:
            TIPO=dic['type']
        except KeyError as name:
            TIPO = "none"
        try:
            ACT=dic['activity']
        except KeyError as name:
            ACT = "none"
        try:
            CALLS_DUR=dic['calls_duration']
        except KeyError as name:
            CALLS_DUR = "0"
        try:
            CALLS_MISS=dic['calls_missed']
        except KeyError as name:
            CALLS_MISS = "0"
        try:
            CALLS_MADE=dic['calls_made']
        except KeyError as name:
            CALLS_MADE = "0"
        try:
            CALLS_REC=dic['calls_received']
        except KeyError as name:
            CALLS_REC = "0"
        try:
            DEP=dic['department']
        except KeyError as name:
            DEP = "none"
        try:
            LOC=dic['location']
        except KeyError as name:
            LOC = "none"
        try:
            SMS_REC=dic['sms_received']
        except KeyError as name:
            SMS_REC = "0"
        try:
            SMS_SENT=dic['sms_sent']
        except KeyError as name:
            SMS_SENT = "0"
        client = User(ID,TIPO,ACT,CALLS_DUR,CALLS_MISS,CALLS_MADE,CALLS_REC,DEP,LOC,SMS_REC,SMS_SENT)
        avgcalls_duration += int(CALLS_DUR)
        avgcalls_missed += int(CALLS_MISS)
        avgcalls_made += int(CALLS_MADE)
        avgcalls_received += int(CALLS_REC)
        avgsms_received += int(SMS_REC)
        avgsms_send += int(SMS_SENT)
        lista.append(client)

    media = User("AVERAGE","","",round(avgcalls_duration/conta,2),round(avgcalls_missed/conta,2),round(avgcalls_made/conta,2),round(avgcalls_received/conta,2),"","",round(avgsms_received/conta,2),round(avgsms_send/conta,2))
    for elem in lista:
        elem.setAverage(media)

def atualizapi(url,headers):
    r = requests.get(url, headers=headers)
    data = r.json()
    conta = 0
    avgcalls_duration = 0
    avgcalls_missed = 0
    avgcalls_made = 0
    avgcalls_received = 0
    avgsms_received = 0
    avgsms_send = 0
    for dic in data:
        conta += 1
        try:
            CALLS_DUR=dic['calls_duration']
        except KeyError as name:
            CALLS_DUR = "0"
        try:
            CALLS_MISS=dic['calls_missed']
        except KeyError as name:
            CALLS_MISS = "0"
        try:
            CALLS_MADE=dic['calls_made']
        except KeyError as name:
            CALLS_MADE = "0"
        try:
            CALLS_REC=dic['calls_received']
        except KeyError as name:
            CALLS_REC = "0"
        try:
            SMS_REC=dic['sms_received']
        except KeyError as name:
            SMS_REC = "0"
        try:
            SMS_SENT=dic['sms_sent']
        except KeyError as name:
            SMS_SENT = "0"
        avgcalls_duration += int(CALLS_DUR);
        avgcalls_missed += int(CALLS_MISS)
        avgcalls_made += int(CALLS_MADE)
        avgcalls_received += int(CALLS_REC)
        avgsms_received += int(SMS_REC)
        avgsms_send += int(SMS_SENT)
    media = User("AVERAGE","","",round(avgcalls_duration/conta,2),round(avgcalls_missed/conta,2),round(avgcalls_made/conta,2),round(avgcalls_received/conta,2),"","",round(avgsms_received/conta,2),round(avgsms_send/conta,2))
    return media

def atuliza_users_api():
    users_list_comp = []
    readapi(url,headers,users_list_comp)
    return users_list_comp

def subsclientthread(my_user,subsport):
    global all_sockets
    try:
        ssubs = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    except socket.error:
        print("Failed to connect the socket")
        sys.exit()
    try:
        remote_ip=socket.gethostbyname(host)
        print(remote_ip)
    except socket.gaierror:
        print("Hostname could not be resolved")
        sys.exit()
    ssubs.connect((remote_ip,subsport))
    all_sockets.append(ssubs)
    print("Subs socket connected to: "+host+" using IP "+ remote_ip)
    check = True
    while check:
        new_avg = atualizapi(url,headers)
        check = my_user.do_subscription(new_avg,ssubs);
        time.sleep(60)
    ssubs.close()

def clientthread(connection,addr):
    global users_list
    subscrition = False
    my_user = None
    first_entry = True
    while True:
        subsport = random.randint(1024,49151)
        if subsport not in used_ports:
            used_ports.append(subsport)
            break
    print("SUBSCRITION PORT CREATED [{0}]".format(subsport))

    connection.send(struct.pack("!H", subsport))
    connection.send("\n\n\n\n\n\n\n\n\n\tWelcome to the private Isabella server:\n\t\t\tLogin: ".encode())
    while True:
        data = connection.recv(1024)
        reply = data.decode()[0:-1]
        if not data:
            break
        if my_user is None:
            for u in users_list:
                if(reply == u.ide):
                    my_user = u
        if(reply == "3478GFDgu4w639"):
            print("Disconnected with "+addr[0]+":"+str(addr[1]))
            connection.send("Exit\n".encode())
            break
        if (my_user is None):
            connection.send("\n\n\n\n\n\n\n\t\tId not valid\n\t\tLogin: ".encode())
        else:
            if first_entry:
                start_new_thread(subsclientthread,(my_user,subsport ))
                connection.send("\n\n\n\t\t\tMAIN MENU\n\t[Private information] Submit the letter.......p\n\t[Group information] Submit the letter.........g\n\t[Subscrition] Submit the letter...................s\n".encode())
                first_entry = False
                '''Filtracao da informacao vinda
                do menu das subscricoes'''
            elif (subscrition):
                if(reply == "1" and my_user.SUBS_calls_duration == False):
                    my_user.SUBS_calls_duration = True
                elif(reply == "1" and my_user.SUBS_calls_duration == True):
                    my_user.SUBS_calls_duration = False
                elif(reply == "2" and my_user.SUBS_calls_missed == False):
                    my_user.SUBS_calls_missed = True
                elif(reply == "2" and my_user.SUBS_calls_missed == True):
                    my_user.SUBS_calls_missed = False
                elif(reply == "3" and my_user.SUBS_calls_made == False):
                    my_user.SUBS_calls_made = True
                elif(reply == "3" and my_user.SUBS_calls_made == True):
                    my_user.SUBS_calls_made = False
                elif(reply == "4" and my_user.SUBS_calls_received == False):
                    my_user.SUBS_calls_received = True
                elif(reply == "4" and my_user.SUBS_calls_received == True):
                    my_user.SUBS_calls_received = False
                elif(reply == "5" and my_user.SUBS_sms_received == False):
                    my_user.SUBS_sms_received = True
                elif(reply == "5" and my_user.SUBS_sms_received == True):
                    my_user.SUBS_sms_received = False
                elif(reply == "6" and my_user.SUBS_sms_send == False):
                    my_user.SUBS_sms_send = True
                elif(reply == "6" and my_user.SUBS_sms_send == True):
                    my_user.SUBS_sms_send = False
                elif(reply == "7"):
                    subscrition = False
                if subscrition:
                    my_user.displaySubscrition(reply,connection);
                else:
                    connection.send("\n\n\n\t\t\tMAIN MENU\n\t[Private information] Submit the letter.......p\n\t[Group information] Submit the letter.........g\n\t[Subscrition] Submit the letter...................s\n".encode())
            else:

                if(reply == "s"):
                    subscrition = True
                    my_user.displaySubscrition(reply,connection);
                elif(reply == "p"):
                    aux = atuliza_users_api()
                    for u in aux:
                        if(my_user.ide == u.ide):
                            my_user.tipo = u.tipo
                            my_user.activity = u.activity
                            my_user.calls_duration = u.calls_duration
                            my_user.calls_missed = u.calls_missed
                            my_user.calls_made = u.calls_made
                            my_user.calls_received = u.calls_received
                            my_user.department = u.department
                            my_user.location = u.location
                            my_user.sms_received = u.sms_received
                            my_user.sms_send = u.sms_send
                    connection.send("\nYour Private Information:\n".encode())
                    connection.send(my_user.displayEveryting().encode())
                    connection.send("\n\t\t\tMAIN MENU\n\t[Private information] Submit the letter.......p\n\t[Group information] Submit the letter.........g\n\t[Subscrition] Submit the letter...................s\n".encode())
                elif(reply == "g"):
                    connection.send("\nGroup Information:\n".encode())
                    connection.send(my_user.average.displayCallSmsInfo().encode())
                    connection.send("\n\t\t\tMAIN MENU\n\t[Private information] Submit the letter.......p\n\t[Group information] Submit the letter.........g\n\t[Subscrition] Submit the letter...................s\n".encode())

                elif(reply == "3478GFDgu4w639"):
                    print("Disconnected with "+addr[0]+":"+str(addr[1]))
                    connection.send("Exit\n".encode())
                    break
                else:
                    connection.send("\n\t\t\tMAIN MENU\n\t[Private information] Submit the letter.......p\n\t[Group information] Submit the letter.........g\n\t[Subscrition] Submit the letter...................s\n".encode())

    connection.close()

def main():


    readapi(url,headers,users_list)
    print("Socket Created")
    try:
        s.bind((host,port))
    except socket.error:
        print("Binding Failed")
        sys.exit()
    print("Socket has been bounded")

    s.listen()
    print("Socket is ready")

    while 1:
        connection, addr = s.accept()
        print("Connected with "+ addr[0] +":"+ str(addr[1]))
        start_new_thread(clientthread,(connection,addr, ))


    s.close()

if __name__ == "__main__":
    global all_sockets
    global users_list
    host = "localhost"
    port = 8880
    all_sockets = []
    try:
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    except socket.error:
        print("Failed to connect the socket")
        sys.exit()
    signal.signal(signal.SIGINT, catch_ctrl_c)
    all_sockets.append(s)
    used_ports = []
    host = "localhost"
    used_ports.append(port)
    users_list = []
    url ="http://socialiteorion2.dei.uc.pt:9014/v2/entities?options=keyValues&type=student&attrs=activity,calls_duration,calls_made,calls_missed,calls_received,department,location,sms_received,sms_sent&limit=100"
    headers = {'cache-control':"no-cache","fiware-servicepath":"/", "fiware-service":"socialite"}

    main()
