import sys, pygame

size = width, height = 800, 416  # Размеры экрана
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
    def clicked(self):
        (x, y) = pygame.mouse.get_pos()
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

    def draw(self,screen):
        if (not self.dead):
            super().draw(screen)
    def CollideDo(self,ob):
        self.health -= 1
        self.death()
class Wall(SpriteObject):
    def __str__(self):
        return "Wall|"+str(self.rect.x)+'|'+str(self.rect.y)
    def load(self,rect):
        self.rect.x = int(rect[0])
        self.rect.y = int(rect[1])

    def __init__(self,x=0,y=0):
        super().__init__('wall.png')
        self.rect.x = x
        self.rect.y = y
class BreakingWall(BreakingObject):
    def __str__(self):
        return "BWall|"+str(self.rect.x)+'|'+str(self.rect.y)
    def load(self,rect):

        self.rect.x = int(rect[0])
        self.rect.y = int(rect[1])


    def __init__(self,x=0,y=0,health=1):
        super().__init__('wall.png',health)
        self.rect.x=x
        self.rect.y=y
if (False and stats):

    if (stats):
        back = False
        Back = SpriteObject('back.png')
        Back.rect.x = int(width / 2.1)
        Back.rect.y = int(height / 1.1)
        plus1 = SpriteObject('+.png')
        minus1 = SpriteObject('-.png')
        plus2 = SpriteObject('+.png')
        minus2 = SpriteObject('-.png')
        plus3 = SpriteObject('+.png')
        minus3 = SpriteObject('-.png')
        plus1.rect.x = int(width / (1.5))
        plus1.rect.y = int(height / 8)
        minus1.rect.x = int(width / (1.58))
        minus1.rect.y = int(height / 8)
        plus2.rect.x = int(width / (1.5))
        plus2.rect.y = int(height / 5)
        minus2.rect.x = int(width / (1.58))
        minus2.rect.y = int(height / 5)
        plus3.rect.x = int(width / (1.5))
        plus3.rect.y = int(height / 3)
        minus3.rect.x = int(width / (1.58))
        minus3.rect.y = int(height / 3)
        health = TextObject('You health:' + str(player1.health), 20, int(width / 2.3), int(height / 10), (0, 0, 0))
        strenght = TextObject('You strenght:' + str(player1.strenght), 20, int(width / 2.3), int(height / 6), (0, 0, 0))
        atackspeed = TextObject('You atackspeed:' + str(player1.atackspeed), 20, int(width / 3.6), int(height / 3.15),
                                (0, 0, 0))
        while (not back):
            Back.draw(screen)
            plus1.draw(screen)
            minus1.draw(screen)
            plus2.draw(screen)
            minus2.draw(screen)
            plus3.draw(screen)
            minus3.draw(screen)
            health.update_text('You health:' + str(player1.health))
            health.draw(screen)
            strenght.update_text('You strenght:' + str(player1.strenght))
            atackspeed.update_text('You atackspeed:' + str(player1.atackspeed * 100))
            strenght.draw(screen)
            atackspeed.draw(screen)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print('This is the end of the game')
                    back = True
                if event.type == pygame.MOUSEBUTTONDOWN:
                    back = Back.clicked()
                    if (plus1.clicked()):
                        player1.health += 1
                    if (minus1.clicked()):
                        player1.health -= 1
                    if (plus2.clicked()):
                        player1.strenght += 1
                    if (minus2.clicked()):
                        player1.strenght -= 1
                    if (plus3.clicked()):
                        player1.atackspeed += 0.001
                    if (minus3.clicked()):
                        player1.atackspeed -= 0.001

            pygame.display.flip()
            pygame.time.wait(5)
            screen.fill((255, 255, 255))
class Bullet(BreakingObject):
    def __str__(self):
        return "Bullet|"+str(self.rect.x)+'|'+str(self.rect.y)+'|'+str(self.shift[0])+'|'+str(self.shift[1])
    def load(self,rect,vector):
            self.rect.x = int(rect[0])
            self.rect.y = int(rect[1])
            self.shift[0] = int(vector[0])
            self.shift[1] = int(vector[1])
            self.health = 1
            return self
    def __init__(self,image,shift,rect,health=1):
            super().__init__(image)
            self.shift[0]=shift[0]*2
            self.shift[1]=shift[1]*2
            self.rect.x = int(rect[0])
            self.rect.y = int(rect[1])
            self.health=health
            s=[0,0]
            if (shift[0] < 0):
                s[0] = -1
            elif(shift[0] > 0):
                s[0] = 1
            if (shift[1] < 0):
                s[1] = -1
            elif (shift[1] > 0):
                s[1] = 1
            if (s[0]==1):
                self.rect.x += 32
                self.rect.y += 10
            elif (s[1]==1):
                self.rect.y += 32
                self.rect.x += 10
            elif (s[0]==-1):
                self.rect.x -= 18
                self.rect.y += 10

            elif (s[1]==-1):
                self.rect.y -= 18
                self.rect.x += 10


    def check_edges(self):
        if self.rect.top <= 0 or self.rect.bottom >= height:
            self.dead=True
        if self.rect.left <= 0 or self.rect.right >= width:
            self.dead=True
class Tank(BreakingObject):
    def __str__(self):
        return self.Image+'|'+str(self.rect.x)+'|'+str(self.rect.y)+'|'+str(self.vector[0])+'|'+str(self.vector[1])+'|'+str(self.health)
    def load(self,Image,rect,vector,health):
            super().__init__(Image)
            self.Image=Image
            self.atack=0
            self.vector=[0,-1]
            self.atackspeed=0.015
            self.strenght = 1
            self.armor = 0
            self.rect.x = int(rect[0])
            self.rect.y = int(rect[1])
            self.health = int(health)
            self.vector[0] = int(vector[0])
            self.vector[1] = int(vector[1])
    def __init__(self):
        super().__init__("tankUP.png")
        self.rect.x = width / 2
        self.rect.y = height / 2
        self.atack = 0
        self.vector = [0, -1]
        self.health = 5
        self.atackspeed = 0.015
        self.strenght = 1
        self.armor = 0

    def Shoot(self):
        if (self.atack<=0):
            self.atack=1
            return Bullet('bullet.png',self.vector,self.rect,health=self.strenght)
        else:
            return False
class Player(Tank):
    def __init__(self):
        super().__init__()
        self.Image='tankUp.png'
    def CollideDo(self,ob,n):
        if (n==1):
            collides=self.shift
            if (self.shift[0] != 0):
                collides[0] = self.shift[0] * -1
            if (self.shift[1] != 0):
                collides[1] = self.shift[1] * -1
            self.shift = collides

            self.move()
            self.shift[0] = 0
            self.shift[1] = 0
        elif (n==2):
            self.health -= 1
            self.death()
    def process_event(self, event):
        if event.type == pygame.KEYDOWN and not self.dead:
            if event.key == pygame.K_y:
                print(str(self))
            if event.key == pygame.K_w:
                self.shift[1] = -1
                self.shift[0] = 0
                self.Image='tankUP.png'
                self.updateImage('tankUP.png')
                self.vector[1] = -1
                self.vector[0] = 0
            elif event.key == pygame.K_s:
                self.shift[1] = 1
                self.shift[0] = 0
                self.updateImage('tankDO.png')
                self.Image='tankDO.png'
                self.vector[1] = 1
                self.vector[0] = 0
            if event.key == pygame.K_d:
                self.shift[0] = 1
                self.shift[1] = 0
                self.updateImage('tankRI.png')
                self.Image='tankRI.png'
                self.vector[0] = 1
                self.vector[1] = 0
            elif event.key == pygame.K_a:
                self.shift[0] = -1
                self.shift[1] = 0
                self.updateImage('tankLE.png')
                self.Image='tankLE.png'
                self.vector[0] = -1
                self.vector[1] = 0
            if event.key == pygame.K_SPACE:
                return self.Shoot()

        elif event.type == pygame.KEYUP:
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
# over=False
# def save():
#     f = open('save.txt', 'w+')
#     for i in walls + breakingWals + [player1] + [player2] + bullets:
#         f.writelines(str(i) + '\n')
#     f.close()
# while(not over):
#
#     black=(0,0,0)
#     pygame.init()
#     screen = pygame.display.set_mode(size, pygame.RESIZABLE)  # pygame.RESIZABLE - позволяет окну изменять размер
#
#     gameover = False
#     player1 = Player()
#     player2 = Player()
#     bullets=[]
#     text1=TextObject('You health:'+str(player1.health),20)
#     text2=TextObject('You health:'+str(player2.health),20,0,60)
#
#     tanks=[]
#     walls=[]
#     breakingWals=[]
#     try:
#         f=open('save.txt','r')
#         for i in f.readlines():
#             i=i.replace('\n','')
#             i=i.split('|')
#
#
#             if (i[0][0]=='W'):
#                 walls+=[i]
#             elif (i[0][0]=='B' and i[0][1]=='W'):
#                 breakingWals+=[i]
#             elif (i[0][0]=='t'):
#                 tanks+=[i]
#             elif (i[0][1]=='u'):
#                 bullets+=[i]
#         breakingWals1=breakingWals
#         breakingWals=[]
#         for i in breakingWals1:
#             a=BreakingWall()
#             a.load([i[1], i[2]])
#             breakingWals+=[a]
#
        # walls1=walls
        # walls=[]
        # for i in walls1:
        #     a=Wall()
        #     a.load([i[1], i[2]])
        #     walls+=[a]
#         bullets1=bullets
#         bullets=[]
#         for i in bullets1:
#             print((Bullet('bullet.png',[1,9],[1,1])).load([i[1],i[2]],[i[3],i[4]]))
#             a=Bullet('bullet.png', [1, 9], [1, 1])
#             a.load([i[1], i[2]], [i[3], i[4]])
#             bullets+=[a]
#         player1.load(tanks[0][0],[tanks[0][1],tanks[0][2]],[tanks[0][3],tanks[0][4]],tanks[0][5])
#         player2.load(tanks[1][0],[tanks[1][1],tanks[1][2]],[tanks[1][3],tanks[1][4]],tanks[1][5])
#         player1.death()
#         player2.death()
#
#     except:
#
#         for i in range(int(height / 19)):
#             for j in range(int(width / 32)):
#                 if (i == 0 or j == 0 or i == 20 or j == 24):
#                     walls += [Wall(j * 32, i * 19)]
#         collides = [0, 0]
#         for i in range(int(height / 19)):
#             for j in range(int(width / 32)):
#                 if (j % 4 == 3 and j < 20 and (i > 2 or i < 16)):
#                     breakingWals += [BreakingWall(j * 32, i * 19)]
#
#     menu = SpriteObject('menu.png')
#     menu.rect.x = 3
#     menu.rect.y = 40
#     while not over and not gameover:
#         for event in pygame.event.get():
#
#             if event.type == pygame.MOUSEBUTTONDOWN:
#                 if (menu.clicked()):
#                     Start = SpriteObject('start.png')
#                     Start.rect.x = int(width/2.1)
#                     Start.rect.y = int(width/10)
#                     Stats = SpriteObject('stats.png')
#                     Stats.rect.x = int(width/2.1)
#                     Stats.rect.y = int(width/4.43)
#                     start = False
#                     exit = SpriteObject('exit.png')
#                     exit.rect.x = int(width/2.1)
#                     exit.rect.y = int(width/2.85)
#                     start = False
#                     stats = False
#                     while not start:
#                         start = over
#                         Start.draw(screen)
#                         exit.draw(screen)
#                         Stats.draw(screen)
#                         for event in pygame.event.get():
#                             if event.type == pygame.QUIT:
#                                 print('This is the end of the game')
#                                 gameover = True
#                             if event.type == pygame.MOUSEBUTTONDOWN:
#                                 start = Start.clicked()
#                                 over = exit.clicked()
#                                 stats = Stats.clicked()
#                                 if (stats):
#                                     save()
#                         pygame.display.flip()
#                         pygame.time.wait(5)
#                         screen.fill((255, 255, 255))
#
#             if event.type == pygame.QUIT:
#                 print('This is the end of the game')
#                 gameover = True
#                 over = True
#             t=player1.process_event(event)
#             if t:
#                 bullets+=[t]
#             t1=player2.process_event(event)
#             if t1:
#                 bullets+=[t1]
#
#         for i in range(len(bullets)):
#             try:
#                 if (i<len(bullets)):
#                     if (bullets[i].dead!=True):
#
#                         bullets[i].death()
#                         bullets[i].move()
#                         bullets[i].draw(screen)
#                     else:
#                         del bullets[i]
#             except:
#                 krya=1
#         for i in range(len(walls)):
#             walls[i].draw(screen)
#         for i in range(len(breakingWals)):
#
#             if (i<len(breakingWals)):
#                 if (breakingWals[i].dead!=True):
#
#                     breakingWals[i].death()
#                     breakingWals[i].draw(screen)
#                 else:
#                     del breakingWals[i]
#
#         if ( not over and not gameover):
#             player1.Collide(walls+breakingWals,1)
#             player1.Collide(bullets,2)
#             player2.Collide(walls+breakingWals,1)
#             player2.Collide(bullets,2)
#             for i in range(len(breakingWals)):
#                 breakingWals[i].Collide(bullets)
#             for i in range(len(bullets)):
#                 bullets[i].Collide(walls)
#                 bullets[i].Collide(breakingWals)
#                 bullets[i].Collide([player1,player2])
#             menu.draw(screen)
#             text1.update_text('Player1 health:'+str(player1.health))
#             text2.update_text('Player2 health:'+str(player2.health))
#             text1.draw(screen)
#             text2.draw(screen)
#             player1.move()
#             player1.draw(screen)
#             player1.atack-=player1.atackspeed
#             player2.move()
#             player2.draw(screen)
#             player2.atack-=player2.atackspeed
#             pygame.display.flip()
#             pygame.time.wait(5)
#             screen.fill(black)