import pygame

class SpriteCollider():
    def __init__(self,screen):
        self.screen = screen
        self.character = CharacterSprite(self.screen)
        self.south1 = South1Sprite(self.screen)
        self.center1 = Center1Sprite(self.screen)
        self.north1 = North1Sprite(self.screen)
        self.middle_road1 = MiddleRoad1Sprite(self.screen)
        self.middle_road2 = MiddleRoad2Sprite(self.screen)
        self.north2 = North2Sprite(self.screen)
        self.center2 = Center2Sprite(self.screen)
        self.south2 = South2Sprite(self.screen)
        # self.sprite_group = pygame.sprite.Group(self.south1,self.south2,self.center1,self.center2,self.north1,self.north2,self.middle_road1,self.middle_road2)
        self.sprite_south1 = pygame.sprite.Group(self.south1)
        self.sprite_south2 = pygame.sprite.Group(self.south2)
        self.sprite_north1 = pygame.sprite.Group(self.north1)
        self.sprite_north2 = pygame.sprite.Group(self.north2)
        self.sprite_center1 = pygame.sprite.Group(self.center1)
        self.sprite_center2 = pygame.sprite.Group(self.center2)
        self.sprite_middle1 = pygame.sprite.Group(self.middle_road1)
        self.sprite_middle2 = pygame.sprite.Group(self.middle_road2)

    def character_collided(self,map_sprite):
        if self.character.collide(map_sprite):
            return True
        return False

    def update_maps(self,x,y):
        self.south1.update(x,y)
        self.south2.update(x,y)
        self.center1.update(x,y)
        self.center2.update(x,y)
        self.middle_road2.update(x,y)
        self.middle_road1.update(x,y)
        self.north1.update(x,y)
        self.north2.update(x,y)

    def update_character(self,x,y,speed):
        self.character.update(x * speed,y * speed)


class CharacterSprite(pygame.sprite.Sprite):
    def __init__(self,screen):
        super().__init__()
        self.screen = screen
        self.image = pygame.image.load("Collisions/Character.jpg")
        self.mask = pygame.mask.from_threshold(self.image,(0,0,0,255),(255,255,255,255))
        self.rect = pygame.Rect(self.screen.get_width() / 3 + 15, self.screen.get_height() / 2 - 45, 40, 140)

    def update(self,x,y):
        self.rect = self.rect.move(x,y)

    def collide(self,spriteGroup):
        if pygame.sprite.spritecollide(self,spriteGroup,False,pygame.sprite.collide_mask):
            return True
        return False

class South1Sprite(pygame.sprite.Sprite):
    def __init__(self,screen):
        super().__init__()
        self.screen = screen
        self.image = pygame.image.load("Collisions/south1.jpg")
        self.mask = pygame.mask.from_threshold(self.image,(0,0,0,255),(255,255,255,255))
        self.rect = pygame.Rect(0, -500 , self.image.get_width(), self.image.get_height())
    def update(self,x,y):
        self.rect = self.rect.move(x, y)

class Center1Sprite(pygame.sprite.Sprite):
    def __init__(self,screen):
        super().__init__()
        self.screen = screen
        self.image = pygame.image.load("Collisions/center1.jpg")
        self.mask = pygame.mask.from_threshold(self.image,(0,0,0,255),(255,255,255,255))
        self.rect = pygame.Rect(0, -2240, self.image.get_width(),self.image.get_height())

    def update(self,x,y):
        self.rect = self.rect.move(x, y)

class North1Sprite(pygame.sprite.Sprite):
    def __init__(self,screen):
        super().__init__()
        self.screen = screen
        self.image = pygame.image.load("Collisions/north1.jpg")
        self.mask = pygame.mask.from_threshold(self.image,(0,0,0,255),(255,255,255,255))
        self.rect = pygame.Rect(0, -3894 , self.image.get_width(), self.image.get_height())
    def update(self,x,y):
        self.rect = self.rect.move(x, y)

class MiddleRoad1Sprite(pygame.sprite.Sprite):
    def __init__(self,screen):
        super().__init__()
        self.screen = screen
        self.image = pygame.image.load("Collisions/middle1.jpg")
        self.mask = pygame.mask.from_threshold(self.image,(0,0,0,255),(255,255,255,255))
        self.rect = pygame.Rect(2057, -3894 , self.image.get_width(), self.image.get_height())
    def update(self,x,y):
        self.rect = self.rect.move(x, y)

class MiddleRoad2Sprite(pygame.sprite.Sprite):
    def __init__(self,screen):
        super().__init__()
        self.screen = screen
        self.image = pygame.image.load("Collisions/middle2.jpg")
        self.mask = pygame.mask.from_threshold(self.image,(0,0,0,255),(255,255,255,255))
        self.rect = pygame.Rect(2060, -734 , self.image.get_width(), self.image.get_height())
    def update(self,x,y):
        self.rect = self.rect.move(x, y)

class North2Sprite(pygame.sprite.Sprite):
    def __init__(self,screen):
        super().__init__()
        self.screen = screen
        self.image = pygame.image.load("Collisions/north2.jpg")
        self.mask = pygame.mask.from_threshold(self.image,(0,0,0,255),(255,255,255,255))
        self.rect = pygame.Rect(3310, -3894 , self.image.get_width(), self.image.get_height())
    def update(self,x,y):
        self.rect = self.rect.move(x, y)

class Center2Sprite(pygame.sprite.Sprite):
    def __init__(self,screen):
        super().__init__()
        self.screen = screen
        self.image = pygame.image.load("Collisions/center2.jpg")
        self.mask = pygame.mask.from_threshold(self.image,(0,0,0,255),(255,255,255,255))
        self.rect = pygame.Rect(3290, -2240, self.image.get_width(),self.image.get_height())

    def update(self,x,y):
        self.rect = self.rect.move(x, y)

class South2Sprite(pygame.sprite.Sprite):
    def __init__(self,screen):
        super().__init__()
        self.screen = screen
        self.image = pygame.image.load("Collisions/south2.jpg")
        self.mask = pygame.mask.from_threshold(self.image,(0,0,0,255),(255,255,255,255))
        self.rect = pygame.Rect(3320, -500 , self.image.get_width(), self.image.get_height())
    def update(self,x,y):
        self.rect = self.rect.move(x, y)
