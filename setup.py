import os
import subprocess
import sys

from Constants import *

if not os.path.isdir(DIR):
    os.mkdir(DIR)

if not os.path.isfile('./lib/mpv.py'):
    os.system(f"pip install mpv -t ./lib --upgrade")


host = input("Server's address (for client): ")
local_host = input("Host computer's address (for server): ")
port = input("What port is the server on: ")

f = open('conn_data.py', 'w')
f.write(f"HOST = '{host}'\n")
f.write(f"LOCAL_HOST = '{local_host}'\n")
f.write(f"PORT = {port}")

f.close()