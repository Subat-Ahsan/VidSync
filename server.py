import socket
import threading 
from Constants import *
from local_server import *
from helper import *
import time
import os

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST,PORT))

server_data = {
    "connection_list" : [],
    "main_conn" : None
}

def disconnect(message, server_data, conn):
    print(message,conn)
    server_data["connection_list"].remove(conn)
    if conn == server_data['main_conn']:
        if len(server_data["connection_list"]) == 0:
            server_data['main_conn'] = None
            return
        server_data['main_conn'] = server_data["connection_list"][0]
    
def get_current_information(server_data):
    if server_data['main_conn'] == None:
        return "NONE#"

    sendCommand("i",'0',server_data['main_conn'])
    try:
        info = server_data['main_conn'].recv(MAX_SIZE).decode(FORMAT)
        
    except:
        return "NONE#"

    return info


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
        
        message_split = message_decoded.split("#")[0]

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

        if message_split == "pw,0":
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

    info = get_current_information(server_data)
    sendMessage(info,conn)

    thread = threading.Thread(target=handle_client, args=(conn,address,server_data))
    thread.start()



