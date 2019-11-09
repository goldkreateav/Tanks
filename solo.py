
from gameObjects import Player,Wall,Bullet,BreakingWall,TextObject,SpriteObject,size,width,height
class Map():

    def __init__(self):
        map=[[0]*int(width / 32)]*int(height / 32)
        for i in range(int(height / 32)):
            for j in range(int(width / 32)):
                if not (i == 0 or j == 0 or i == int(height / 32)-1 or j == int(width / 32)-1):
                    if (j % 2 == 1):
                        map[i][j]=0
        self.map=map
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
Nmap=Map()
for i in range(int(height / 32)):
    for j in range(int(width / 32)):
        if (Nmap.map[i][j]==1):
            breakingWals += [BreakingWall(j * 32, i * 32)]
# int maze[height][width]; //создаем матрицу - двумерный массив
# for(i = 0; i < height; i++){
#         for(j = 0; j < width; j++){
#             if((i % 2 != 0  && j % 2 != 0) && //если ячейка нечетная по x и y,
#                (i < height-1 && j < width-1))   //и при этом находится в пределах стен лабиринта
#                    maze[i][j] = CELL;       //то это КЛЕТКА
#             else maze[i][j] = WALL;           //в остальных случаях это СТЕНА.
#         }
#     }

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