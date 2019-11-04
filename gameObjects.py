import sys, pygame

size = width, height = 640, 480  # Размеры экрана
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
        if self.rect.left <= 0 or self.rect.right >= height:
            self.shift[0] = 0
    def move(self):
        self.rect.x += self.shift[0]
        self.rect.y += self.shift[1]
        self.check_edges()