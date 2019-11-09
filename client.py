from gameObjects import Player,Wall,Bullet,BreakingWall,TextObject
import pygame,time


size = width, height = 800, 399  # Размеры экрана
player1 = Player()
player2 = Player()
bullets = []
tanks = []
walls = []
for i in range(int(height/19)):
        for j in range(int(width/32)):
            if (i==0 or j==0 or i==20 or j==24 ):
                walls+=[Wall(j*32,i*19)]
breakingWals = []
def Send():
    wasd=0
    space=0
    if pygame.key.get_pressed()[pygame.K_s]:
        wasd=1
    elif pygame.key.get_pressed()[pygame.K_a]:
        wasd=2
    elif pygame.key.get_pressed()[pygame.K_w]:
        wasd=3
    if pygame.key.get_pressed()[pygame.K_d]:
        wasd=4
    if pygame.key.get_pressed()[pygame.K_SPACE]:
        space=1
    f=open('frclient.txt','w+')
    f.writelines([str(wasd),'\n',str(space)])
    f.close()

black = (0, 0, 0)
pygame.init()
screen = pygame.display.set_mode(size, pygame.RESIZABLE)  # pygame.RESIZABLE - позволяет окну изменять размер
c=0
text2 = TextObject('You health:' + str(player2.health), 20)
text1 = TextObject('Enemy health:' + str(player1.health), 20, 0, 60)
over=False
while(not over):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print('This is the end of the game')
                gameover = True
                over = True
        Sucess = False
        walls1=walls
        player11=player1
        player21=player2
        bullets1=bullets

        if (player2.health>0):
            text2.update_text('You health:' + str(player2.health))
        else:
            text2.update_text('You health:0')
        if (player1.health>0):
            text1.update_text('Enemy health:' + str(player1.health))
        else:
            text1.update_text('Enemy health:0')
        try:
            player11 = Player()
            player12 = Player()
            bullets1 = []
            tanks = []
            breakingWals1 = []
            f = open('foclients.txt', 'r')
            gg=f.readlines()
            f.close()
            for i in gg:
                i = i.replace('\n', '')
                i = i.split('|')

                if (i[0][0] == 'B' and i[0][1] == 'W'):
                    breakingWals1 += [i]
                elif (i[0][0] == 't'):
                    tanks += [i]
                elif (i[0][1] == 'u'):
                    bullets1 += [i]
            if (len(breakingWals1)>0):
                breakingWals=[]
                for i in breakingWals1:
                    a = BreakingWall()
                    a.load([i[1], i[2]])
                    breakingWals += [a]
            try:
                if (len(bullets1)>0 or not bullets[0].dead):
                    bullets=[]
                    for i in bullets1:
                        a = Bullet('bullet.png', [1, 9], [1, 1])
                        a.load([i[1], i[2]], [i[3], i[4]])
                        bullets += [a]
            except:
                NuBivaaaet=True
            player1.load(tanks[0][0], [tanks[0][1], tanks[0][2]], [tanks[0][3], tanks[0][4]], tanks[0][5])
            player2.load(tanks[1][0], [tanks[1][1], tanks[1][2]], [tanks[1][3], tanks[1][4]], tanks[1][5])
            player1.death()
            player2.death()
            Sucess = True
        except:
            Sucess = False
        Send()
        if (len(walls)<1):
            print(walls)
        try:
            for i in range(len(bullets)):
                bullets[i].draw(screen)
        except:
            ssss=1
        for i in range(len(walls)):
            walls[i].draw(screen)
        try:
            for i in range(len(breakingWals)):
                breakingWals[i].draw(screen)
        except:
            ssss=1
        try:
            player1.draw(screen)
        except:
            ssss=1
        try:
            player2.draw(screen)
        except:
            sss=1
        text1.draw(screen)
        text2.draw(screen)
        pygame.display.flip()
        pygame.time.wait(50)
        screen.fill(black)