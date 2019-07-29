import pygame
from os import listdir




class World:
    def __init__(self,screen,player):
        self.screen=screen
        self.player = player
        self.surface = pygame.Rect(0,self.screen.get_height()*1/5,screen.get_width(),self.screen.get_height()*4/5)
    def place(self):
        files = listdir("World")
        [self.bar, self.cactus1, self.cactus2, self.cactus3, self.cow1, self.cow2, self.sign] = [
            pygame.image.load("World/" + path) for path in files]
        self.screen.blit(self.bar,(self.screen.get_width()/4,0))
        self.screen.blit(self.cactus1,(self.screen.get_width()*4/5 + 50,self.screen.get_height()/5))
        self.screen.blit(self.cactus2, (self.screen.get_width() * 4/5 + self.cactus1.get_width()+57, self.screen.get_height() / 5 + self.cactus1.get_height()+8))
        self.screen.blit(self.cactus1, (self.screen.get_width() * 4.5 - 40 , self.screen.get_height() / 5 + 3))
        self.collision()
    def collision(self):
        pass
    def l_images(self,folder):
        files = listdir(folder)
        self.images = [pygame.image.load(folder + path) for path in files]

    def init_colors(self):
        self.black = 0
        self.white = (255,255,255)
        self.green = (0,255,0)
        self.red  = (255,0,0)
        self.blue = (0,0,255)
        self.yellow = (255,255,0)
        self.brown = (153,76,0)
        self.gray = (128,128,128)
        self.orange = (255,128,0)
        self.purple = (127,0,255)
        self.pink = (255,0,255)
        self.cyan = (0,255,255)

class City(World):
    def __init__(self,screen,player):
        self.map = pygame.image.load("World/city.jpg")
        self.screen = screen
        self.player = player
        self.surface = pygame.Rect(0,self.screen.get_height()/5,screen.get_width(),self.screen.get_height()*4/5)
        super().init_colors()

