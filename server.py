import socket
import threading 
from Constants import *
from local_server import *

import time
import os

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST,PORT))

server_data = {
    "connection_list" : [],
    "main_conn" : None
}


def handle_client(conn,address,server_data):
    connected= True

    while (connected):
        try:
            message = conn.recv(MAX_SIZE)
        except:
            print(f"Disconnecting {conn}")
            server_data["connection_list"].remove(conn)
            connected=False
            break
        
        if not message:
            print(f"Disconnecting {conn}")
            server_data["connection_list"].remove(conn)
            connected=False
            break

        message_decoded = message.decode(FORMAT)
        
        message_split = message_decoded.split("#")[0]

        if message_split == DC or message_decoded == '':
            print(f"Disconnecting {conn}")
            server_data["connection_list"].remove(conn)
            connected=False
            break

        if message_split == SD:
            for i in connection_list:
                conn.send(SD.encode(FORMAT))

            for i in connection_list:
                i.close()

            print("Done")
            os._exit(1)

        if message_split == "pw,0":
            server_data["main_conn"] = conn

        for i in connection_list:
            i.send(message)
    
    conn.close()


while True:
    server.listen()
    conn, address = server.accept()
    if conn in connection_list:
        continue
    connection_list.append(conn)
    print(f"{conn}, {address} is connected")
    thread = threading.Thread(target=handle_client, args=(conn,address,connection_list))
    thread.start()


