#!/usr/bin/env python3
import time
import mpv
from os import listdir
from os.path import exists
import pymkv

DIR="videos"

def swap(value):
    if(value == False):
        return True
    return False


player = mpv.MPV(fs=False)
player.window_maximized=True
while True:
    fn = input("Enter filename (q to quit): ")
    if (fn == 'q'):
        exit()
    print(fn)
    if (not (exists(f"./{DIR}/{fn}"))):
        print("File not found")
        continue
    fileType=fn.split(".")[-1]
    if ( fileType not in {'mp4', 'mkv', 'mp3'}):
        print("Invalid type")
        continue
    break

if (fileType == "mkv"):
    pass

player.play(f'./{DIR}/{fn}')
player.wait_until_playing()

audioTrack=1
VideoTrack=1

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

@player.on_key_press('f')
def my_q_binding():
    player.fs = swap(player.fs)

@player.on_key_press('space')
def my_q_binding():
    player.pause = swap(player.pause)
 


player.show_text("hello", 1000)
while not player._core_shutdown:
   
    continue


