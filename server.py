from gameObjects import Player,Wall,Bullet,BreakingWall
import pygame,time
size = width, height = 800, 399
player1 = Player()
player2 = Player()
bullets = []
tanks = []
walls = []
breakingWals = []
def Send1():
    f = open('foclients.txt', 'w+')
    for i in breakingWals + [player1] + [player2] + bullets:
        f.writelines(str(i) + '\n')
    f.close()

gameover = False
for i in range(int(height/19)):
        for j in range(int(width/32)):
            if (i==0 or j==0 or i==20 or j==24 ):
                walls+=[Wall(j*32,i*19)]
for i in range(int(height / 19)):
    for j in range(int(width / 32)):
        if ( j%5==4):
            breakingWals += [BreakingWall(j * 32, i * 19)]
while(player1.health>0 or player2.health>0):
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
        Send1()
        if (True or Recieve1):
            try:
                f = open('frclient.txt', 'r')
                keys=f.readlines()
                f.close()
                keys[0]=int(keys[0].replace('\n',''))

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
                f = open('frclient2.txt', 'r')
                keys = f.readlines()
                f.close()
                keys[0]=int(keys[0].replace('\n',''))

                if (keys[0]==1):
                    player2.shift=[0,3]
                    player2.vector=[0,3]
                    player2.Image='tankDO.png'

                elif (keys[0]==2):
                    player2.shift=[-3,0]
                    player2.vector=[-3,0]
                    player2.Image='tankLE.png'
                elif (keys[0]==3):
                    player2.shift=[0,-3]
                    player2.vector=[0,-3]
                    player2.Image='tankUP.png'
                elif (keys[0]==4):
                    player2.shift=[3,0]
                    player2.vector=[3,0]
                    player2.Image='tankRI.png'
                else:
                    player2.shift = [0, 0]
                if (int(keys[1]) == 1):
                    sh = player2.Shoot()
                    if (sh):
                        bullets += [sh]

            except:
                k=1
        time.sleep(0.05)