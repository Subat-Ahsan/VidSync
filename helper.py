from Constants import *
from local_server import *
import time
import os
def check_int(i):
    try:
        x = int(i)
    except ValueError:
        return False
    else:
        return True

def format_time(time):
    try:
        time = round(time)
    except TypeError:
        return ""

    hours = time//3600
    time = time - hours * 3600
    minutes = time//60
    time = time - minutes * 60
    seconds = time

    return f"{hours:02}:{minutes:02}:{seconds:02}"


def get_time(message):
    seconds = 0
    multiply = 1

    i = input(message)
    l = i.split(":")

    for t in reversed(l):
        if not check_int(t):
            return -1

        t = int(t)
        if t < 0:
            return -1
        
        seconds += t*multiply
        multiply *= 60

    return seconds

def swap(value):
    if(value == False):
        return True
    return False

def sendMessage(message,socket):
    try:
        socket.send((message+" "*(MAX_SIZE - len(message))).encode(FORMAT))
    except ConnectionResetError:
        print("Connection Reset Error")
        return

def sendCommand(command,argument,socket):
    s = command+","+argument+"#"
    sendMessage(s,socket)

def get_track(message):
    x = input(message)
    if not check_int(x):
        return '1'
    return x

def play_file(player, socket):
    while True:
        fn = input("Enter filename (q to quit): ")
        if (fn == 'q'):
            sendMessage(DC+"#",socket)
            exit()
        if (not (os.path.exists(f"./{DIR}/{fn}"))):
            print("File not found")
            continue
        fileType=fn.split(".")[-1]
        if ( fileType not in {'mp4', 'mkv', 'mp3'}):
            print("Invalid type")
            continue
        break

    sendCommand("sfn",fn,socket)
    sendCommand("pw","0",socket)
    
    audioTrack=1
    VideoTrack=1

    count = 0
    if (fileType=="mkv"):
        time.sleep(0.5)
        print("\nAudio Tracks:")

        for i in player.get_media().track_list:
            if (i['type'] == 'audio'):
                if ('title' in i.keys()):
                    print(f"{i['id']}. {i['title']} ({i['lang']})")
                else:
                    print(f"{i['id']}. ({i['lang']})")
            count += 1

        audioTrack = get_track("Enter audio track: ")
        
        count = 0
        print("\nSub Tracks:")
        for i in player.get_media().track_list:
            if (i['type'] == 'sub'):
                if ('title' in i.keys()):
                    print(f"{i['id']}. {i['title']} ({i['lang']})")
                else:
                    print(f"{i['id']}. ({i['lang']})")
            count += 1
        subTrack = get_track("Enter subtitle track: ")
        
        sendCommand("aid",audioTrack,socket)
        sendCommand("sid",subTrack,socket)
        
        print("Hit play")
    else:
        pass

if __name__ == '__main__':
    print(format_time(233))
