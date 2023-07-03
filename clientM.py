#!/usr/bin/env python3
import time
import mpv
import os
import pymkv

import socket
import threading 

from Constants import *
from helper import *
from local_server import *


class Player():
    media_player= mpv.MPV(fs=False, keep_open=True)
    fn = ""
    media_player.window_maximized = True
    aid = 1
    sid = 1
    DIR="videos"

    def play(self):
        self.media_player.play(f'./{self.DIR}/{self.fn}')

    def wait(self):
        self.media_player.wait_until_playing()

    def set_aid(self, value):
        self.aid = value
        self.media_player.aid = self.aid
    
    def set_sid(self, value):
        self.sid = value
        self.media_player.sid = self.sid

    def get_media(self):
        return self.media_player
    
    
player = Player()

socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
socket.connect((HOST,PORT))

print("Socket 1:" + str(socket))

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
            player.get_media().wait_until_playing
            player.get_media().pause=True

        if (c == "aid"):
            player.set_aid(int(a))
        if (c == "sid"):
            player.set_sid(int(a))
        
        if (c == "p"):
            if (a == "0"):
                player.get_media().pause = False
            else:
                player.get_media().pause = True
        
        if (c == "p"):
            if (a == "0"):
                player.get_media().pause = False
            else:
                player.get_media().pause = True
        
        if (c == "r"):
            player.get_media().seek(int(a))

        if (c == "l"):
            player.get_media().seek(-1 * int(a))

        if (c == "g"):
            print(a)
            player.get_media().seek(int(a),  reference="absolute" , precision="exact")

input_thread = threading.Thread(target=handleMessage,args=(player,) )
input_thread.daemon = True
input_thread.start()

play_file(player, socket)

@player.get_media().on_key_press('f')
def my_f_binding():
    player.get_media().fs = swap(player.get_media().fs)

@player.get_media().on_key_press('q')
def my_q_binding():
    player.get_media().quit(0)

def show_time(media):
    for i in range(5):
        media.show_text(f"{format_time(media.time_pos)}/{format_time(media.duration)}")
        time.sleep(0.5)

@player.get_media().on_key_press('t')
def my_t_binding():
    for i in threading.enumerate():
        if (i._target == show_time):
            return

    time_show = threading.Thread(target=show_time, args=(player.get_media(),))
    time_show.daemon = True
    time_show.start()

@player.get_media().on_key_press('space')
def my_space_binding():
    sendCommand("p", str(int(swap(player.get_media().pause))),socket)

@player.get_media().on_key_press('n')
def my_n_binding():
    play_file(player, socket)

@player.get_media().on_key_press('RIGHT')
def my_RIGHT_binding():
    sendCommand("r", str(SEEK_VALUE) ,socket)

@player.get_media().on_key_press('LEFT')
def my_LEFT_binding():
    sendCommand("l", str(SEEK_VALUE) ,socket)

@player.get_media().on_key_press('g')
def my_g_binding():
    x = get_time("Enter position (-1 to quit):")
    if (x < 0 ):
        return
    sendCommand("g", str(x) ,socket)

player.media_player.wait_for_shutdown()

print('Quitting')
os._exit(0)
