from gameObjects import SpriteObject,width,height,size
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
                exec('\n'.join(open('client.py','r').readlines()))
            if (Solo):
                exec('\n'.join(open('solo.py','r').readlines()))
    pygame.display.flip()
    pygame.time.wait(5)
    screen.fill((255, 255, 255))
