import sys, pygame

size = width, height = 800, 400  # Размеры экрана
class SpriteObject():
    def __init__(self,image=''):
        self.image_filename='images/'+image
        self.image = pygame.image.load(self.image_filename)
        self.rect = self.image.get_rect()
    def set_center_position(self, x, y):
        self.rect.center = (x, y)
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
class Bullet(BreakingObject):
    def __init__(self,image,shift,rect):
        super().__init__(image)
        self.shift[0]=shift[0]*2
        self.shift[1]=shift[1]*2
        self.rect.x = rect.x
        self.rect.y = rect.y

        self.rect.x += shift[0] * 16

        self.rect.y += shift[1] * 16

    def check_edges(self):
        if self.rect.top <= 0 or self.rect.bottom >= height:
            self.dead=True
        if self.rect.left <= 0 or self.rect.right >= width:
            self.dead=True
class Tank(BreakingObject):
    def __init__(self,image):
        super().__init__(image)
        self.health=5
        self.atackspeed=1
        self.atack=0
        self.vector=[0,1]

    def process_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                self.shift[1] = -1
                self.vector[1]=-1
            elif event.key == pygame.K_s:
                self.shift[1] = 1
                self.vector[1] = 1
            if event.key == pygame.K_SPACE:
                return self.Shoot()
            if event.key == pygame.K_d:
                self.shift[0] = 1
                self.vector[0] = 1
            elif event.key == pygame.K_a:
                self.shift[0] = -1
                self.vector[0]= -1
        elif event.type == pygame.KEYUP:
            if (pygame.key.get_pressed()[pygame.K_s]):
                self.vector[1] = 1
            elif (pygame.key.get_pressed()[pygame.K_w]):
                self.vector[1] = -1
            if (pygame.key.get_pressed()[pygame.K_a]):
                self.vector[0] = -1
            if (pygame.key.get_pressed()[pygame.K_d]):
                self.vector[0] = 1
            if not (pygame.key.get_pressed()[pygame.K_w]) and not (pygame.key.get_pressed()[pygame.K_s]):

                if (self.vector[0] != 0):
                    self.vector[1] = 0
            if not pygame.key.get_pressed()[pygame.K_a] and not (pygame.key.get_pressed()[pygame.K_d]):
                if (self.vector[1] != 0):
                    self.vector[0] = 0

            if (pygame.key.get_pressed()[pygame.K_w] or pygame.key.get_pressed()[pygame.K_s]) and (pygame.key.get_pressed()[pygame.K_a] or pygame.key.get_pressed()[pygame.K_d]):
                if (self.vector[1] != 0):
                    self.vector[0] = 0
                if (self.vector[0] != 0):
                    self.vector[1] = 0
            if not(pygame.key.get_pressed()[pygame.K_w] and pygame.key.get_pressed()[pygame.K_s]) and(event.key == pygame.K_w or event.key == pygame.K_s):
                self.shift[1] = 0
            if not(pygame.key.get_pressed()[pygame.K_a] and pygame.key.get_pressed()[pygame.K_d]) and(event.key == pygame.K_a or event.key == pygame.K_d):
                self.shift[0] = 0
        return False
    def Shoot(self):
        if (self.atack<=0):
            self.atack=self.atackspeed
            return Bullet('bullet.png',self.vector,self.rect)
        else:
            return False
