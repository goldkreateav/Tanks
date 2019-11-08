from gameObjects import Player,Wall,Bullet,BreakingWall,TextObject
import pygame,time

player1 = Player()
player2 = Player()
bullets = []
tanks = []
walls = []
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
    f=open('frclient2.txt','w+')
    f.writelines([str(wasd),'\n',str(space)])
    f.close()


size = width, height = 800, 399  # Размеры экрана
black = (0, 0, 0)
pygame.init()
screen = pygame.display.set_mode(size, pygame.RESIZABLE)  # pygame.RESIZABLE - позволяет окну изменять размер
c=0
text1 = TextObject('You health:' + str(player2.health), 20)
text2 = TextObject('Enemy health:' + str(player1.health), 20, 0, 60)
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
        try:
            player1 = Player()
            player2 = Player()
            bullets = []
            tanks = []
            walls = []
            breakingWals = []
            f = open('foclients.txt', 'r')
            gg=f.readlines()
            f.close()
            for i in gg:
                i = i.replace('\n', '')
                i = i.split('|')

                if (i[0][0] == 'W'):
                    walls += [i]
                elif (i[0][0] == 'B' and i[0][1] == 'W'):
                    breakingWals += [i]
                elif (i[0][0] == 't'):
                    tanks += [i]
                elif (i[0][1] == 'u'):
                    bullets += [i]
            breakingWals1 = breakingWals
            breakingWals = []
            for i in breakingWals1:
                a = BreakingWall()
                a.load([i[1], i[2]])
                breakingWals += [a]

            walls1 = walls
            walls = []
            for i in walls1:
                a = Wall()
                a.load([i[1], i[2]])
                walls += [a]
            bullets1 = bullets
            bullets = []
            for i in bullets1:
                print((Bullet('bullet.png', [1, 9], [1, 1])).load([i[1], i[2]], [i[3], i[4]]))
                a = Bullet('bullet.png', [1, 9], [1, 1])
                a.load([i[1], i[2]], [i[3], i[4]])
                bullets += [a]
            player1.load(tanks[0][0], [tanks[0][1], tanks[0][2]], [tanks[0][3], tanks[0][4]], tanks[0][5])
            player2.load(tanks[1][0], [tanks[1][1], tanks[1][2]], [tanks[1][3], tanks[1][4]], tanks[1][5])
            player1.death()
            player2.death()
            Sucess = True
        except:
            Sucess = False

            walls = walls1
            player1 = player11
            player2 = player21
            bullets = bullets1
        Send()
        if (len(walls)<1):
            print(walls)
            walls=walls1
        try:
            for i in range(len(bullets)):
                bullets[i].draw(screen)
        except:
            ssss=1
        try:
            for i in range(len(walls)):
                walls[i].draw(screen)
        except:
            ssss=1
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
        pygame.display.flip()
        pygame.time.wait(50)
        screen.fill(black)