import pygame
from os import listdir


class City():
    def __init__(self,screen,player):
        self.static_anim_id = 0; #id of a static animation, used in func anim_static,  decides which static animation is played in frame
        self.screen = screen
        self.player = player
        self.init_countable()
        self.init_maps()
        self.init_maps_blocks()
       # self.init_collisions()
        self.init_anim()
        self.surface = pygame.Rect(0, self.screen.get_height()/5,screen.get_width(), self.screen.get_height()*4/5)

    def init_maps(self):
        #Maps
        self.north1 = pygame.image.load("World/maps/north1.png").convert_alpha()
        self.north2 = pygame.image.load("World/maps/north2.png").convert_alpha()
        self.center1 = pygame.image.load("World/maps/center1.png").convert_alpha()
        self.center2 = pygame.image.load("World/maps/center2.png").convert_alpha()
        self.south1 = pygame.image.load("World/maps/south1.png").convert_alpha()
        self.south2 = pygame.image.load("World/maps/south2.png").convert_alpha()
        self.middle_road1 = pygame.image.load("World/maps/middle1.png").convert_alpha()
        self.middle_road2 = pygame.image.load("World/maps/middle2.png").convert_alpha()

        #Objects
        self.north1_objects = pygame.image.load("World/objects/north1.png").convert_alpha()
        self.middle_road1_objects = pygame.image.load("World/objects/middle1.png").convert_alpha()
        self.middle_road2_objects = pygame.image.load("World/objects/middle2.png").convert_alpha()
        self.north2_objects = pygame.image.load("World/objects/north2.png").convert_alpha()
        self.center1_objects = pygame.image.load("World/objects/center1.png").convert_alpha()
        self.center2_objects = pygame.image.load("World/objects/center2.png").convert_alpha()
        self.south1_objects = pygame.image.load("World/objects/south1.png").convert_alpha()
        self.south2_objects = pygame.image.load("World/objects/south2.png").convert_alpha()


        #Collisions
        self.north1_collisions = pygame.image.load("World/collisions/north1.jpg").convert_alpha()
        self.middle_road1_collisions = pygame.image.load("World/collisions/middle1.jpg").convert_alpha()
        self.middle_road2_collisions = pygame.image.load("World/collisions/middle2.jpg").convert_alpha()
        self.north2_collisions = pygame.image.load("World/collisions/north2.jpg").convert_alpha()
        self.center1_collisions = pygame.image.load("World/collisions/center1.jpg").convert_alpha()
        self.center2_collisions = pygame.image.load("World/collisions/center2.jpg").convert_alpha()
        self.south1_collisions = pygame.image.load("World/collisions/south1.jpg").convert_alpha()
        self.south2_collisions = pygame.image.load("World/collisions/south2.jpg").convert_alpha()

    def init_maps_blocks(self):
        self.south1_block = pygame.Rect(0, -500 , self.south1.get_width(), self.south1.get_height())
        self.center1_block = pygame.Rect(self.south1_block.x, self.south1_block.y - self.center1.get_height(), self.center1.get_width(),self.center1.get_height())
        self.north1_block = pygame.Rect(self.center1_block.x, self.center1_block.y - self.north1.get_height(),self.north1.get_width(), self.north1.get_height())
        self.middle_road1_block = pygame.Rect(self.north1_block.x + self.north1_block.width - 3, self.north1_block.y, self.middle_road1.get_width(), self.middle_road1.get_height())
        self.middle_road2_block = pygame.Rect(self.middle_road1_block.x , self.middle_road1_block.y + self.middle_road1.get_height() - 20, self.middle_road2.get_width(), self.middle_road2.get_height())
        self.north2_block = pygame.Rect(self.middle_road1_block.x + self.middle_road1.get_width() - 10, self.north1_block.y, self.north2.get_width(), self.north2.get_height())
        self.center2_block = pygame.Rect(self.north2_block.x - 10, self.center1_block.y, self.center2.get_width(), self.center2.get_height())
        self.south2_block = pygame.Rect(self.center2_block.x, self.center2_block.y + self.center2.get_height(), self.south2.get_width(), self.south2.get_height())

    def change_maps_positions(self,x,y):
        self.middle_road1_block = self.middle_road1_block.move(x,y)
        self.north1_block = self.north1_block.move(x,y)
        self.north2_block = self.north2_block.move(x,y)
        self.middle_road2_block = self.middle_road2_block.move(x,y)
        self.center1_block = self.center1_block.move(x,y)
        self.center2_block = self.center2_block.move(x,y)
        self.south1_block = self.south1_block.move(x,y)
        self.south2_block = self.south2_block.move(x,y)
        self.fount_block = self.fount_block.move(x,y)
        self.caruzel_block = self.caruzel_block.move(x,y)

    def init_countable(self):
        self.fps = 0
        self.delay = 4
        self.frames = 0
        self.d_fountain = 9
        self.d_caruzel = 6

    def l_images(self,folder):
        files = listdir(folder)
        self.images = [pygame.image.load(folder + path) for path in files]
    # returns different images from image object obj after a certain delay defined in self.delay
    def anim_object(self, img_amount, obj):
        if (self.fps == self.delay):
            self.fps = 0
            self.frames += 1
        self.fps += 1
        self.frames = self.frames % img_amount
        return obj[self.frames]

    def anim_static(self):
        if self.player.block.colliderect(self.middle_road1_block.move(250,0)):
            self.static_anim_id = 0
        elif self.player.block.colliderect(self.south2_block.move(-100,0)):
            self.static_anim_id = 1
        if self.static_anim_id == 0:
            return self.anim_fountain()
        elif self.static_anim_id == 1:
            return self.anim_caruzel()

    def anim_fountain(self): #map coordinates are used for static anim to move simultaneusly with map
        return self.anim_object(self.d_fountain, self.fountain)
    def anim_caruzel(self):
        return self.anim_object(self.d_caruzel,self.caruzel)
    def init_anim(self):
        fountain_fList = listdir("World/fountain")
        caruzel_fList = listdir("World/caruzel")

        self.fountain = [pygame.transform.scale(pygame.image.load("World/fountain/" + path), (355, 341)) for path in
                         fountain_fList]

        self.fount_block = pygame.Rect(self.middle_road1_block.x + self.middle_road1.get_width() / 3 + 55,
                                       self.middle_road1_block.y + self.middle_road1.get_height() * 7 / 10 - 30,
                                       self.fountain[0].get_width(), self.fountain[ 0].get_height())  # place fountain in the middle of the middle_road location
        self.caruzel = [pygame.image.load("World/caruzel/" + path) for path in caruzel_fList]

        self.caruzel_block = pygame.Rect(self.south2_block.x + 1300, self.south2_block.y + 600,self.caruzel[0].get_width(),self.caruzel[0].get_height())
   #equivalent to str(Object), will be used for locations_NPC dictionary
    def get_string(self,location_blk):
        if location_blk.height == self.south1_block.height:
            return "south1"
        elif location_blk.height == self.south2_block.height:
            return "south2"
        elif location_blk.height == self.middle_road1_block.height:
            return "middle_road1"
        elif location_blk.height == self.middle_road2_block.height:
            return "middle_road2"
        elif location_blk.height == self.center1_block.height:
            return "center1"
        elif location_blk.height == self.center2_block.height:
            return "center2"
        elif location_blk.height == self.north1_block.height:
            return "north1"
        elif location_blk.height == self.north2_block.height:
            return "north2"
