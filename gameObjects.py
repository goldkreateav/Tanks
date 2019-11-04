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
    def clicked(self,x,y):
        return x >= self.rect.x and y >= self.rect.y and x <= self.rect.x + self.rect.width and y <= self.rect.y + self.rect.height
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
    def Collide(self,ob,n=-1):
        hit = pygame.sprite.spritecollide(self, ob,False)
        if hit:
            try:
                if (n!=-1):
                    self.CollideDo(ob,n)
                else:
                    self.CollideDo(ob)
            except:
                if (n!=-1):
                    self.CollideDo([ob],n)
                else:
                    self.CollideDo([ob])

    def CollideDo(self,ob):
        pass
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

    def CollideDo(self,ob):
        self.health -= 1
        self.death()
class Wall(SpriteObject):
    def __init__(self,x=0,y=0):
        super().__init__('wall.png')
        self.rect.x = x
        self.rect.y = y
class BreakingWall(BreakingObject):
    def __init__(self,x=0,y=0,health=1):
        super().__init__('wall.png',health)
        self.rect.x=x
        self.rect.y=y

class Bullet(BreakingObject):
    def __init__(self,image,shift,rect,):
        super().__init__(image)
        self.shift[0]=shift[0]*2
        self.shift[1]=shift[1]*2
        self.rect.x = rect.x
        self.rect.y = rect.y
        self.health=2
        s=[0,0]
        if (shift[0] < 0):
            s[0] = -1
        else:
            s[0] = 1
        if (shift[1] < 0):
            s[1] = -1
        else:
            s[1] = 1

        self.rect.x += shift[0] * 15 + s[0]*15

        self.rect.y += shift[1] * 15 + s[1]*15
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

    def CollideDo(self,ob,n):
        if (n==1):
            if (self.shift[0] != 0):
                collides[0] = self.shift[0] * -1
            if (player1.shift[1] != 0):
                collides[1] = self.shift[1] * -1

            self.shift = collides

            self.move()
            self.shift[0] = 0
            self.shift[1] = 0
        elif (n==2):
            self.health -= 1
            self.death()
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
class TextObject():
    def __init__(self, text, size, x=0, y=0, color=(255, 255, 255)):
        self.position = (x, y)
        self.text = text
        self.size = size
        self.color = color
        self.font = pygame.font.SysFont('Comic Sans MS', self.size, True)  # Шрифт Comic Sans MS, размер 15, полужирный
        self.surface = self.font.render(self.text, False, self.color)

    def update_text(self, new_text):
        self.text = new_text
        self.surface = self.font.render(self.text, False, self.color)

    def update_position(self, x, y):
        self.position = (x, y)

    def get_text_size(self):
        r = self.surface.get_rect()
        return [r.width, r.height]

    def draw(self, screen):
        screen.blit(self.surface, self.position)
class Button(TextObject):
    def __init__(self, text, size, x=0, y=0, color=(255, 255, 255)):
        super().__init__(text,size,x,y,color)
over=False
while(not over):

    black=(0,0,0)
    pygame.init()
    screen = pygame.display.set_mode(size, pygame.RESIZABLE)  # pygame.RESIZABLE - позволяет окну изменять размер
    Start=SpriteObject('start.png')
    Start.rect.x = 380
    Start.rect.y = 40
    exit = SpriteObject('exit.png')
    exit.rect.x = 380
    exit.rect.y = 140
    start=False

    while not start:
        start=over
        Start.draw(screen)
        exit.draw(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print('This is the end of the game')
                gameover = True
            (x, y)= pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONDOWN:
                start = Start.clicked(x,y)
                over = exit.clicked(x,y)

        pygame.display.flip()
        pygame.time.wait(5)
        screen.fill((255,255,255))


    gameover = False
    player1=Player('tankUP.png')
    tankk=Tank('tankUP.png')
    text1=TextObject('You health:'+str(player1.health),20)
    bullets=[]
    walls=[]
    breakingWals=[]
    for i in range(int(height/19)):
        for j in range(int(width/32)):
            if (i==0 or j==0 or i==20 or j==24 ):
                walls+=[Wall(j*32,i*19)]
    collides=[0,0]
    for i in range(int(height / 19)):
        for j in range(int(width / 32)):
            if (j%4==3 and j<13 and i>4):
                breakingWals+=[BreakingWall(j*32,i*19)]

    while not over and not gameover:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print('This is the end of the game')
                gameover = True
            t=player1.process_event(event)
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

        player1.Collide(walls+breakingWals,1)
        player1.Collide(bullets,2)
        for i in range(len(breakingWals)):
            breakingWals[i].Collide(bullets)
        for i in range(len(bullets)):
            bullets[i].Collide(walls)
            bullets[i].Collide(breakingWals)
            bullets[i].Collide([player1,tankk])
        if (False):
            bullets+=[t]
            tankk.atack=1
        tankk.atack-=0.015
        tankk.move()
        tankk.draw(screen)
        text1.update_text('You health:'+str(player1.health))
        text1.draw(screen)
        player1.move()
        player1.draw(screen)
        player1.atack-=0.015
        pygame.display.flip()
        pygame.time.wait(5)
        screen.fill(black)