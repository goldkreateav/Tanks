from gameObjects import SpriteObject,width,height,size,Player,InputBox
import pygame


black = (0, 0, 0)
pygame.init()
screen = pygame.display.set_mode(size, pygame.RESIZABLE)  # pygame.RESIZABLE - позволяет окну изменять размер

solo = SpriteObject('solo.png')
solo.rect.x = int(width/2.1)
solo.rect.y = int(width/10)
multi = SpriteObject('multi.png')
multi.rect.x = int(width/2.1)
multi.rect.y = int(width/4.43)
start = False
exit = SpriteObject('exit.png')
exit.rect.x = int(width/2.1)
exit.rect.y = int(width/2.85)
Solo = False
stats = False
over=False

while not over:
    solo.draw(screen)
    exit.draw(screen)
    multi.draw(screen)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print('This is the end of the game')
            gameover = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            Solo = solo.clicked()
            over = exit.clicked()
            Multi = multi.clicked()
            if (Multi):
                IP = InputBox(int(width/2.1),int(height/3),200,40)

                Start = SpriteObject('start.png')
                Start.rect.x = int(width / 2.1)
                Start.rect.y = int(width / 2.2)
                s=False
                while( not s):
                    Start.draw(screen)
                    IP.draw(screen)

                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            print('This is the end of the game')
                            gameover = True
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            s = Start.clicked()
                        IP.handle_event(event)

                    pygame.display.flip()
                    pygame.time.wait(5)
                    screen.fill((255, 255, 255))
                ip=IP.text
                try:
                    exec('\n'.join(open('client.py','r').readlines()))
                except:
                    s=False
                    IP.text='This game cant to start'
            if (Solo):
                size = width, height = 800, 399  # Размеры экрана
                player1 = Player()
                player2 = Player()
                bullets = []
                tanks = []
                walls = []
                exec('\n'.join(open('solo.py','r').readlines()))
    pygame.display.flip()
    pygame.time.wait(5)
    screen.fill((255, 255, 255))
