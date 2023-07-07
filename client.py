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
    duration = 0
    playing = False

    @media_player.on_key_press('f')
    def my_f_binding():
        player.swap_fullscreen()
       
    @media_player.on_key_press('q')
    def my_q_binding():
        player.shutdown()

    @media_player.on_key_press('space')
    def my_space_binding():
        send_command(PAUSE, str(int(swap(player.get_property('pause')))),socket)

    @media_player.on_key_press('RIGHT')
    def my_RIGHT_binding():
        send_command(RIGHT_SEEK, str(SEEK_VALUE) ,socket)

    @media_player.on_key_press('LEFT')
    def my_LEFT_binding():
        send_command(LEFT_SEEK, str(SEEK_VALUE) ,socket)

    @media_player.on_key_press('g')
    def my_g_binding():
        x = get_time("Enter position (-1 to quit):")
        if (x < 0 ):
            return
        send_command("g", str(x) ,socket)

    def play(self):
        self.media_player.play(f'./{self.DIR}/{self.fn}')
        self.wait_until_playing()
        self.set_duration()
        self.playing = True

    def pause(self, state):
        self.media_player.pause = state

    def wait_until_playing(self):
        self.media_player.wait_until_playing()
    
    def swap_fullscreen(self):
        self.media_player.fs = swap(self.media_player.fs)

    def get_property(self,p):
        if self.playing == False:
            return None
        return getattr(self.media_player, p)
        
    def get_media(self):
        return self.media_player

    def shutdown(self):
        self.media_player.quit(0)

    def set_aid(self, value):
        self.aid = value
        self.media_player.aid = self.aid
    
    def seek(self, amount, r = "relative", p = "keyframes"):
        if self.playing == False:
            return 
        self.media_player.seek(amount, r, p)

    def set_sid(self, value):
        self.sid = value
        self.media_player.sid = self.sid
    
    def get_duration(self):
        return self.duration

    def set_duration(self):
        self.duration = self.media_player.duration
        
    def get_current_information(self):
        if self.fn == "":
            return "NONE"
        return f"{self.fn},{self.media_player.time_pos},{self.duration},{self.aid},{self.sid},{int(self.media_player.pause)}"

    def set_from_information(self,info):
        info_lis = info.split(",")
        if info_lis[0] == "":
            return
        fn = info_lis[0]

        time_pos = float(info_lis[1])
        duration = float(info_lis[2])
        aid = int(info_lis[3])
        sid = int(info_lis[4])
        pause = bool(int(info_lis[5]))
        
        self.fn = fn
        
        self.play()
        self.media_player.time_pos = time_pos 
        self.media_player.pause = pause
        
        self.set_aid(aid)
        self.set_sid(sid)

def show_time(player, media):
    for i in range(5):
        media.show_text(f"{format_time(media.time_pos)}/{format_time(player.get_duration())}")
        time.sleep(0.5)

def handleMessage(player):
    while True:
        try:
            y = (socket.recv(MAX_SIZE)).decode(FORMAT)
        except ConnectionResetError:
            exit()

        m=y.split(PERIOD)[0]
        c=m.split(",")[0]
        a=m.split(",")[1]
        
        if (c == SET_FILE_NAME):
            player.fn = a

        elif (c == PLAY_WAIT):
            player.play()
            player.pause(True)

        elif (c == SET_AID):
            player.set_aid(int(a))
        
        elif (c == SET_SID):
            player.set_sid(int(a))
        
        elif (c == PAUSE):
            if (a == "0"):
                player.pause(False)
            else:
                player.pause(True)
        
        elif (c == RIGHT_SEEK):
            player.seek(int(a))

        elif (c == LEFT_SEEK):
            player.seek(int(a) * -1)

        elif (c == FIND):
            player.seek(int(a),  r="absolute" , p="exact")

        elif (c == NEW_CLIENT):
            player.pause(True)
            while True:
                try:
                    new_message = socket.recv(MAX_SIZE).decode().split(PERIOD)[0]
                except: 
                    break
                if new_message == GET_INFORMATION:
                    send_message(SEND_TO_NEW+player.get_current_information()+PERIOD,socket)
                if new_message[0] == CONTINUE:
                    break

        continue 

player = Player()

socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
socket.connect((HOST,PORT))
info = socket.recv(MAX_SIZE).decode(FORMAT)

print("Socket 1:" + str(socket))
    
input_thread = threading.Thread(target=handleMessage,args=(player,) )
input_thread.daemon = True
input_thread.start()

info_split= info.split(PERIOD)[0]

if info_split == "NONE":
    state = play_file(player, socket)
    if state == 'w':
        player.wait_until_playing()
else:
    player.set_from_information(info_split)
    send_command(CONTINUE,"0",socket)


@player.get_media().on_key_press('t')
def my_t_binding():
    for i in threading.enumerate():
        if (i._target == show_time):
            return

    time_show = threading.Thread(target=show_time, args=(player, player.get_media()))
    time_show.daemon = True
    time_show.start()

@player.get_media().on_key_press('n')
def my_n_binding():
    play_file(player, socket)

player.media_player.wait_for_shutdown()

print('Quitting...')
send_message(DC+"#", socket)
