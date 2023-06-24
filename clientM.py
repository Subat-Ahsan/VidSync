#!/usr/bin/env python3
import time
import mpv
from os import listdir
from os.path import exists
import pymkv

import socket
import threading 

from Constants import *

DIR="videos"
MAX_SIZE = 512

def swap(value):
    if(value == False):
        return True
    return False

def sendMessage(message,socket):
    socket.send((message+" "*(MAX_SIZE - len(message))).encode(FORMAT))

class Player():
    video_player= mpv.MPV(fs=False)
    fn = ""
    video_player.window_maximized = True
    DIR="videos"
    def play(self):
        self.video_player.play(f'./{self.DIR}/{self.fn}')

player = Player()

while True:
    fn = input("Enter filename (q to quit): ")
    if (fn == 'q'):
        exit()
    if (not (exists(f"./{DIR}/{fn}"))):
        print("File not found")
        continue
    fileType=fn.split(".")[-1]
    if ( fileType not in {'mp4', 'mkv', 'mp3'}):
        print("Invalid type")
        continue
    break

socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
socket.connect((HOST,PORT))

def handleMessage(player):
    while True:
        y = (socket.recv(MAX_SIZE)).decode(FORMAT)
        m=y.split("#")[0]
        c=m.split(",")[0]
        a=m.split(",")[1]
        if (c == "sfn"):
            player.fn = a
        if (c == "pw"):
            player.play()
            player.video_player.wait_until_playing()

t = threading.Thread(target=handleMessage,args=(player,) )
t.start()

sendMessage("sfn,"+fn+"#", socket)
sendMessage("pw,"+"#", socket)

'''
player.play(f'./{DIR}/{fn}')
player.wait_until_playing()
'''

audioTrack=1
VideoTrack=1




'''
if (fileType=="mkv"):
    player.pause=True
    print("\nAudio Tracks:")

    for i in player.track_list:
        if (i['type'] == 'audio'):
            if ('title' in i.keys()):
                print(f"{i['id']}. {i['title']} ({i['lang']})")
            else:
                print(f"{i['id']}. ({i['lang']})")

    audioTrack = int(input("\nSelect audio track: "))
    
    print("\nSub Tracks:")
    for i in player.track_list:
        if (i['type'] == 'sub'):
            if ('title' in i.keys()):
                print(f"{i['id']}. {i['title']} ({i['lang']})")
            else:
                print(f"{i['id']}. ({i['lang']})")

    subTrack = int(input("\nSelect sub track: "))
    
    player.aid=audioTrack
    player.sid=subTrack
    
    print("Hit play")
else:


@player.on_key_press('f')
def my_q_binding():

    player.fs = swap(player.fs)

@player.on_key_press('space')
def my_q_binding():

    player.pause = swap(player.pause)
 

while not player._core_shutdown:
   
    continue
'''

