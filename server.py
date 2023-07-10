import socket
import threading 
from Constants import *
from conn_data import *
from helper import *
import time
import os

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((LOCAL_HOST,PORT))

server_data = {
    "connection_list" : [],
    "main_conn" : None,
    "new_conn" : None,
    "waiting" : False
}

def disconnect(message, server_data, conn):
    try:
        server_data["connection_list"].remove(conn)
    except:
        pass

    if conn == server_data['main_conn']:
        if len(server_data["connection_list"]) == 0:
            server_data['main_conn'] = None
            return
        server_data['main_conn'] = server_data["connection_list"][0]
    
def get_current_information(server_data, conn):
    if server_data['main_conn'] == None:
        send_message("NONE#", conn)
        return

    for c in server_data["connection_list"]:
        if c == conn:
            continue
        send_command("n","0",c)
        server_data['waiting'] = True
        server_data['new_conn'] = conn
    send_message(GET_INFORMATION+PERIOD,server_data['main_conn'])

def stop_waiting_for_new_conn(server_data):
    for i in server_data["connection_list"]:
        send_message(CONTINUE+",0"+PERIOD,i)
    server_data["new_conn"] = None
    server_data["waiting"] = False

def handle_client(conn,address,server_data):
    connected= True

    while (connected):
        try:
            message = conn.recv(MAX_SIZE)
        except:
            disconnect("Disconnecting (b)",server_data,conn)
            connected=False
            break
        
        if not message:
            disconnect("Disconnecting (e)",server_data,conn)
            connected=False
            break

        message_decoded = message.decode(FORMAT)
        message_split = message_decoded.split(PERIOD)[0]
        #print(f"From: {conn} : {message_split}|")

        if message_split == DC:
            disconnect("Disconnecting (q)",server_data,conn)
            connected=False
            break

        if message_split == SD:
            for i in server_data["connection_list"]:
                conn.send(SD.encode(FORMAT))

            for i in server_data["connection_list"]:
                i.close()

            print("Done")
            os._exit(1)

        if message_split[0] == SEND_TO_NEW:
            
            send_message(message_split[1:],server_data["new_conn"])
            try:
                m = server_data["new_conn"].recv(MAX_SIZE)
            except:
                stop_waiting_for_new_conn(server_data)
                disconnect("Disconnecting (n)", server_data, server_data["new_conn"])
                continue

            stop_waiting_for_new_conn(server_data)
            
            if message == '':
                disconnect("Disconnecting (n)", server_data, server_data["new_conn"])
            continue
        

        if message_split[:2] == PLAY_WAIT:
            server_data["main_conn"] = conn

        for i in server_data["connection_list"]:
            i.send(message)
    
    conn.close()

def info(server_data):
    while True:
        x = input()
        print(f"Connection List: {server_data['connection_list']}")
        print(f"Main: {server_data['main_conn']}")
        print(threading.enumerate())

t = threading.Thread(target=info, args=(server_data,))
t.daemon = True
t.start()

while True:
    server.listen()
    conn, address = server.accept()
    if conn in server_data['connection_list']:
        continue
    
    server_data['connection_list'].append(conn)
    print(f"{conn}, {address} is connected")

    get_current_information(server_data, conn)

    while (server_data['waiting']):
        continue

    thread = threading.Thread(target=handle_client, args=(conn,address,server_data))
    thread.start()



