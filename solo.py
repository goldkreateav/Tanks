
from gameObjects import Player,Wall,Bullet,BreakingWall,TextObject,SpriteObject,size,width,height
import random
import pygame,time
gameover = False
over=False
pygame.init()
player1 = Player()
player2 = Player()
black = (0, 0, 0)
screen = pygame.display.set_mode(size, pygame.RESIZABLE)  # pygame.RESIZABLE - позволяет окну изменять размер
text1 = TextObject('You health:' + str(player1.health), 20)
text2 = TextObject('You health:' + str(player2.health), 20, 0, 60)
bullets = []
walls = []
breakingWals = []
menu = SpriteObject('menu.png')
menu.rect.x = 3
menu.rect.y = 40
for i in range(int(height / 32)):
    for j in range(int(width / 32)):
        if (i == 0 or j == 0 or i == int(height / 32)-1 or j == int(width / 32)-1):
            walls += [Wall(j * 32, i * 32)]
collides = [0, 0]
pol=(height // 32 + int((height % 32)>=22))//2+(height // 32 + int((height % 32)>=22))%2
pol1=0

list = [] * 2
list2 = [] * 2
for i in range(2):
    list += [random.randrange(1, width // 32, 2)]
    list2 += [random.randrange(1, height // 32, 2)]

for stage in range(height // 32):
    if (stage != list2[0] and stage != list2[1]):
        wls=(stage%2)
    if stage>pol:
        pol1+=1
    for i in range(width // 32) :
        if(i!=list[0] and i!=list[1]):
            if wls==0:
                if(i>=stage-pol1*2 and (i < (width // 32 ) - stage + pol1*2) and stage !=pol):
                    breakingWals += [BreakingWall(i * 32, (stage) * 32)]
                    breakingWals += [BreakingWall (0 , stage * 32)]
                    breakingWals += [BreakingWall(width - 32, stage * 32)]
                if i==2 and stage>=3 and stage<=height//32-3 or i==width//32-3 and stage>=3 and stage<=height//32-3:
                    breakingWals += [BreakingWall(i * 32, (stage) * 32)]
                if i==4 and stage>=5 and stage<=height//32-5 or i==width//32-5 and stage>=5 and stage<=height//32-5:
                    breakingWals += [BreakingWall(i * 32, (stage) * 32)]

while not over and not gameover:
    for event in pygame.event.get():

        if event.type == pygame.MOUSEBUTTONDOWN:
            if (menu.clicked()):
                gameover=True

        if event.type == pygame.QUIT:
            print('This is the end of the game')
            gameover = True
            over = True
        t = player1.process_event(event)
        if t:
            bullets += [t]
        t1 = player2.process_event(event)
        if t1:
            bullets += [t1]

    for i in range(len(bullets)):
        if (i < len(bullets)):
            if (bullets[i].dead != True):

                bullets[i].death()
                bullets[i].move()
                bullets[i].draw(screen)
            else:
                del bullets[i]
    for i in range(len(walls)):
        walls[i].draw(screen)
    for i in range(len(breakingWals)):

        if (i < len(breakingWals)):
            if (breakingWals[i].dead != True):

                breakingWals[i].death()
                breakingWals[i].draw(screen)
            else:
                del breakingWals[i]

    if (not over and not gameover):
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
            bullets[i].health-=0.008
        menu.draw(screen)
        text1.update_text('Player1 health:' + str(player1.health))
        text2.update_text('Player2 health:' + str(player2.health))
        text1.draw(screen)
        text2.draw(screen)
        player1.move()
        player1.draw(screen)
        player1.atack -= player1.atackspeed
        player2.move()
        player2.draw(screen)
        player2.atack -= player2.atackspeed
        pygame.display.flip()
        pygame.time.wait(5)
        screen.fill(black)