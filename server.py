#!/usr/bin/python
"""Server hosting Texas Hold 'Em games

Eventually I want to be able to host more than one table

First, implement a table structure for players to join, watch, and leave
"""
import socket
import player
import pitch

sit='a'
connections=[]
s=socket.socket()
host=socket.gethostname()
port=11037
s.bind((host,port))
s.listen(10)
print '[INFO] Server listening on port '+str(port)

tab = pitch.Pitch()
print '[INFO] Table created'

while True:
    c, addr=s.accept()
    print 'Got connection from', addr
    c.send('Thank you for connecting')
    data = c.recv(1024)
    uname, epass = data.split(' ', 1)
    print 'uname: '+uname+' | encoded passw: '+epass
    c.send('Welcome to the lobby '+uname+'!')
    user = player.Player(uname)
    while sit not in ['p', 'w', 'l']:
        c.send('"p" for play, "w" for watch, or "l" for leave:')
        sit = c.recv(1)
    if sit == 'w':
        tab.watchers.append(user)
    elif sit == 'p':
        tab.players.append(user)
    else:
        del user
        c.close
        continue
    connections.append(c)
    if len(connections) < 2:
        continue
    elif len(tab.players) < 2:
        continue
    else:
        #start game, but continue to accept connections
        break
