import socket
import threading 
from Constants import *
import time
import os

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST,PORT))

connection_list = []


def handle_client(conn,address,connection_list):
    connected= True

    while (connected):
        message = conn.recv(MAX_SIZE)
        message_decoded = message.decode(FORMAT)

        if message_decoded == DC or message_decoded == '':
            connection_list.remove(conn)
            connected=False
            break

        if message_decoded == SD:
            for i in connection_list:
                conn.send(SD.encode(FORMAT))

            for i in connection_list:
                i.close()

            print("Done")
            os._exit(1)
        

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


