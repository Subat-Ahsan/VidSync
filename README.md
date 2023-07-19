# VidSync
Syncs videos across multiple computers using the sockets module in pythons. 

1. [Tutorial (server)](#id-ts)  
2. [Tutorial (client)](#id-tc)  
3. [Key Bindings](#id-kb)

## Tutorial (server) <div id='id-ts'/>
#### 1. Run setup.py 
```
C:\Your\Path\VidSync>python setup.py
Collecting mpv
  Using cached mpv-1.0.3-py3-none-any.whl (44 kB)
Installing collected packages: mpv
Successfully installed mpv-1.0.3

Server's address (for client): [Not required unless client on same computer]
Host computer's address (for server):[Computer's IPv4 Address]
What port is the server on: [Port Number]
```
For access outside the local area network, the network that the server is running on requires port forwarding to the computer running the server on the port 'Port Number' to be enabled.

Input the server address as either the public address of the network or IPv4 address of the computer
if both client and server are running on the same machine

#### 2. Run the server
```
C:\Your\Path\VidSync>python server.py
Server Running on
IpV4: [Computer's IPv4 address]        
Public IPv4: [Network's public IPv4 address]
Port: [Port]

Press enter for server data: 
```

## Tutorial (client) <div id='id-tc'/>
#### Run setup.py 
```
C:\Your\Path\VidSync>python setup.py
Collecting mpv
  Using cached mpv-1.0.3-py3-none-any.whl (44 kB)
Installing collected packages: mpv
Successfully installed mpv-1.0.3

Server's address (for client): [Public or Local IPv4 address of server]
Host computer's address (for server):[Not required unless server on same computer]
What port is the server on: [Port Number]
```

Input the the computer's IPv4 address as 'host computer's address' if it is running both  
client and server. 

If client and server are running on the same network, the public IPv4 address of the network
or local IPv4 address of the server computer can be used.

The server can only be accessed from different network if port forwarding is enabled
on server's network.  
The server hosting network's public IPv4 Address has to be used. 

#### 2. Add videos
Place all videos in the 'videos' directory at C:\Your\Path\VidSync\'videos'.  
Make sure the video files have the same name across all computers it will be synced.

(Currently only mp4 and mkv supported)

#### 3. Run client.py
```
C:\Your\Path\VidSync>python client.py
Connected to: ([Server address], [Port])
Enter filename (q to quit or w to wait): filename.mp4
```
Enter the filename to begin playing file. Enter 'w' to wait
for other user to play file.  
If video was already playing for other users when new user joins,
it will open the video for them and pause it for all users. 

## Key Bindings <div id='id-kb'/>
| Key        | Function| 
| :--------: |:------------:| 
|f| Toggle full screen |
|t| Show current and remaining time|
|q| Quit player|
|space| Toggle pause |
|RIGHT| Skip forward 5 seconds <br />Can be changed by changing seek value in constants.py |
|LEFT|  Skip backwards 5 seconds<br /> Can be changed by changing seek value in constants.py |
|d| Skip right certain amount <br /> Input amount in terminal (hh:mm:ss)|
|a| Skip left certain amount <br /> Input amount in terminal (hh:mm:ss)|
|g| Seek to position <br /> Input position in terminal (hh:mm:ss)|
|r| Re-sync all players by seeking to same position |
|n| Play new file <br /> Input new file in terminal |
