from gameObjects import Player,Wall,Bullet,BreakingWall
import pygame,time
import socket
import random
import threading
size = width, height = 800, 399
player1 = Player()
player2 = Player()
bullets = []
tanks = []
walls = []
breakingWals = []
BUFFSIZE = 2048
clients = set()
clients_r = {}
clients_lock = threading.Lock()
Currentid = 1
def listener(client, address, CurrentId=Currentid):
    global breakingWals,bullets,player1,player2,keys,keys1
    def Send1(breakingWals, Bullets,player1,player2):
        return '\n'.join([str(i) for i in breakingWals] + [str(player1)] + [str(player2)] + [str(i) for i in Bullets])

    print("Accepted connection from: ", address)
    with clients_lock:
        clients.add(client)
        clients_r[Currentid] = client
    while(1):
        try:
           data = client.recv(2048).decode("utf-8")
           gg=data.split('|')[1]

           id = int(data.split("|")[0])
           if id == 1:
                gg=gg.split('\n')
                keys=[int(gg[0]),int(gg[1])]
           if id == 2:
                gg=gg.split('\n')
                keys1=[int(gg[0]),int(gg[1])]
           with clients_lock:
                for i in clients:
                    i.send(bytes(Send1(breakingWals,bullets,player1,player2),encoding="utf8"))
        except:
            L=2
host = ''
port = 7557

s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((host,port))
s.listen(1000)
th = []
while(Currentid<3):
    Currentid += 1
    client, address = s.accept()
    th.append(threading.Thread(target=listener, args=(client, address)).start())

keys=[0,0]
keys1=[0,0]
gameover = False
for i in range(int(height/19)):
        for j in range(int(width/32)):
            if (i==0 or j==0 or i==20 or j==24 ):
                walls+=[Wall(j*32,i*32)]
for i in range(int(height / 32)):
    for j in range(int(width / 32)):
        if ( j%5==4):
            breakingWals += [BreakingWall(j * 32, i * 32)]
while(player1.health>0 and player2.health>0):
        player1.move()
        player2.move()
        player1.atack-=player1.atackspeed*5
        player2.atack-=player2.atackspeed*5
        for i in range(len(bullets)):
            try:
                if (i < len(bullets)):
                    if (bullets[i].dead != True):

                        bullets[i].death()
                        bullets[i].move()
                    else:
                        del bullets[i]
            except:
                krya = 1
        for i in range(len(breakingWals)):

            if (i < len(breakingWals)):
                if (breakingWals[i].dead != True):

                    breakingWals[i].death()
                else:
                    del breakingWals[i]

        player1.Collide(walls + breakingWals, 1)
        player1.Collide(bullets, 2)
        player2.Collide(walls + breakingWals, 1)
        player2.Collide(bullets, 2)
        for i in range(len(breakingWals)):
            breakingWals[i].Collide(bullets)
        for i in range(len(bullets)):
            bullets[i].Collide(walls)
            bullets[i].Collide(breakingWals)
            bullets[i].Collide([player1, player2])
        if (True or Recieve1):
            try:
                if (keys[0]==1):
                    player1.shift=[0,3]
                    player1.vector=[0,3]
                    player1.Image='tankDO.png'

                elif (keys[0]==2):
                    player1.shift=[-3,0]
                    player1.vector=[-3,0]
                    player1.Image='tankLE.png'
                elif (keys[0]==3):
                    player1.shift=[0,-3]
                    player1.vector=[0,-3]
                    player1.Image='tankUP.png'
                elif (keys[0]==4):
                    player1.shift=[3,0]
                    player1.vector=[3,0]
                    player1.Image='tankRI.png'
                else:
                    player1.shift = [0, 0]
                if (int(keys[1]) == 1):
                    sh = player1.Shoot()
                    if (sh):
                        bullets += [sh]
            except:
                print(1)
        if (True or Recieve2):
            try:
                if (keys1[0]==1):
                    player2.shift=[0,3]
                    player2.vector=[0,3]
                    player2.Image='tankDO.png'

                elif (keys1[0]==2):
                    player2.shift=[-3,0]
                    player2.vector=[-3,0]
                    player2.Image='tankLE.png'
                elif (keys1[0]==3):
                    player2.shift=[0,-3]
                    player2.vector=[0,-3]
                    player2.Image='tankUP.png'
                elif (keys1[0]==4):
                    player2.shift=[3,0]
                    player2.vector=[3,0]
                    player2.Image='tankRI.png'
                else:
                    player2.shift = [0, 0]
                if (int(keys1[1]) == 1):
                    sh = player2.Shoot()
                    if (sh):
                        bullets += [sh]

            except:
                k=1
        time.sleep(0.05)