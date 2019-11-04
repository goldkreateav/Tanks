import sys, pygame

size = width, height = 800, 399  # Размеры экрана
class SpriteObject():
    def __init__(self,image=''):
        self.image_filename='images/'+image
        self.image = pygame.image.load(self.image_filename)
        self.rect = self.image.get_rect()
    def set_center_position(self, x, y):
        self.rect.center = (x, y)
    def updateImage(self, newimage):
        self.image_filename='images/'+newimage
        self.image = pygame.image.load(self.image_filename)
        newrect=self.image.get_rect()

        newrect.x=self.rect.x
        newrect.y=self.rect.y
        self.rect=newrect

    def draw(self,screen):
        screen.blit(self.image, self.rect)
class DinamicObject(SpriteObject):
    def __init__(self, image=''):
        super().__init__(image)
        self.speed = [1, 1]
        self.shift = [0, 0]
    def check_edges(self):
        if self.rect.top <= 0 or self.rect.bottom >= height:
            self.shift[1] = 0
        if self.rect.left <= 0 or self.rect.right >= width:
            self.shift[0] = 0
    def move(self):
        self.rect.x += self.shift[0]
        self.rect.y += self.shift[1]
        self.check_edges()
class BreakingObject(DinamicObject):
    def __init__(self,image,health=1):
        self.dead=False
        super().__init__(image)
        self.health=health
    def death(self):
        if (self.health<=0):
            self.dead=True
            return True
        return False
class Wall(SpriteObject):
    def __init__(self,x=0,y=0):
        super().__init__('wall.png')
        self.rect.x = x
        self.rect.y = y


class BreakingWall(Wall):
    def __init__(self,x=0,y=0,health=1):
        super().__init__(x,y)
        self.dead=False
        self.health=health
    def death(self):
        if (self.health <= 0):
            self.dead = True
            return True
        return False

class Bullet(BreakingObject):
    def __init__(self,image,shift,rect):
        super().__init__(image)
        self.shift[0]=shift[0]*2
        self.shift[1]=shift[1]*2
        self.rect.x = rect.x
        self.rect.y = rect.y

        self.rect.x += shift[0] * 16+13

        self.rect.y += shift[1] * 16+13

    def check_edges(self):
        if self.rect.top <= 0 or self.rect.bottom >= height:
            self.dead=True
        if self.rect.left <= 0 or self.rect.right >= width:
            self.dead=True
class Tank(BreakingObject):
    def __init__(self,image):
        super().__init__(image)
        self.rect.x=width/2
        self.rect.y=height/2
        self.health=5
        self.atackspeed=1
        self.atack=0
        self.vector=[0,1]
    def Shoot(self):
        if (self.atack<=0):
            self.atack=self.atackspeed
            return Bullet('bullet.png',self.vector,self.rect)
        else:
            return False
class Player(Tank):
    def __init__(self,image):
        super().__init__(image)

    def process_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                self.shift[1] = -1
                self.shift[0] = 0
                self.updateImage('tankUP.png')
                self.vector[1] = -1
                self.vector[0] = 0
            elif event.key == pygame.K_s:
                self.shift[1] = 1
                self.shift[0] = 0
                self.updateImage('tankDO.png')
                self.vector[1] = 1
                self.vector[0] = 0
            if event.key == pygame.K_d:
                self.shift[0] = 1
                self.shift[1] = 0
                self.updateImage('tankRI.png')
                self.vector[0] = 1
                self.vector[1] = 0
            elif event.key == pygame.K_a:
                self.shift[0] = -1
                self.shift[1] = 0
                self.updateImage('tankLE.png')
                self.vector[0] = -1
                self.vector[1] = 0
            if event.key == pygame.K_SPACE:
                return self.Shoot()
        elif event.type == pygame.KEYUP:
            if not (pygame.key.get_pressed()[pygame.K_w]) and not (pygame.key.get_pressed()[pygame.K_s]):

                if (self.vector[0] != 0):
                    self.vector[1] = 0
            if not pygame.key.get_pressed()[pygame.K_a] and not (pygame.key.get_pressed()[pygame.K_d]):
                if (self.vector[1] != 0):
                    self.vector[0] = 0

            if (pygame.key.get_pressed()[pygame.K_w] or pygame.key.get_pressed()[pygame.K_s]) and (
                    pygame.key.get_pressed()[pygame.K_a] or pygame.key.get_pressed()[pygame.K_d]):
                if (self.vector[1] != 0):
                    self.vector[0] = 0
                if (self.vector[0] != 0):
                    self.vector[1] = 0
            if not (pygame.key.get_pressed()[pygame.K_w] and pygame.key.get_pressed()[pygame.K_s]) and (
                    event.key == pygame.K_w or event.key == pygame.K_s):
                self.shift[1] = 0
            if not (pygame.key.get_pressed()[pygame.K_a] and pygame.key.get_pressed()[pygame.K_d]) and (
                    event.key == pygame.K_a or event.key == pygame.K_d):
                self.shift[0] = 0
        return False
black=(0,0,0)
pygame.init()
screen = pygame.display.set_mode(size, pygame.RESIZABLE)  # pygame.RESIZABLE - позволяет окну изменять размер
gameover = False
tank=Player('tankUP.png')
bullets=[]
walls=[]
breakingWals=[]
for i in range(int(height/19)):
    for j in range(int(width/32)):
        if (i==0 or j==0 or i==20 or j==24 ):
            walls+=[Wall(j*32,i*19)]

for i in range(int(height / 19)):
    for j in range(int(width / 32)):
        if (j%4==3 and j<13 and i>4):
            breakingWals+=[BreakingWall(j*32,i*19)]
while not gameover:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print('This is the end of the game')
            gameover = True
        t=tank.process_event(event)
        if t:
            bullets+=[t]

    for i in range(len(bullets)):
        if (i<len(bullets)):
            if (bullets[i].dead!=True):

                bullets[i].death()
                bullets[i].move()
                bullets[i].draw(screen)
            else:
                del bullets[i]
    for i in range(len(walls)):
        walls[i].draw(screen)
    for i in range(len(breakingWals)):
        if (i<len(breakingWals)):
            if (breakingWals[i].dead!=True):

                breakingWals[i].death()
                breakingWals[i].draw(screen)
            else:
                del breakingWals[i]


    hits = pygame.sprite.spritecollide(tank, walls+breakingWals, False)
    if hits:
        tank.shift[0] *= -1
        tank.shift[1] *= -1
        tank.move()
        tank.move()
        tank.move()
        tank.move()
        tank.shift[0] = 0
        tank.shift[1] = 0
    for i in range(len(bullets)):
        hits = pygame.sprite.spritecollide(bullets[i], walls, False)
        hits1 = pygame.sprite.spritecollide(bullets[i], breakingWals, False)
        if hits or hits1:
            bullets[i].dead=True
    for i in range(len(breakingWals)):
        hits1 = pygame.sprite.spritecollide(breakingWals[i], bullets, False)
        if (hits1):
            breakingWals[i].dead=True

    tank.move()
    tank.draw(screen)
    tank.atack-=0.015
    pygame.display.flip()
    pygame.time.wait(5)
    screen.fill(black)