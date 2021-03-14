from math import fabs

import pygame
from os import listdir


class Deliverer():

    def __init__(self,screen,):
        #Misc
        H_files = listdir("Hero/")
        # pygame.sprite.Sprite.__init__()

        self.init_countable()
        self.screen = screen

        #Images and Objects
        self.human = [pygame.transform.scale(pygame.image.load("Hero/" + path).convert_alpha(),(84, 161) ) for path in H_files]
        self.visible = [pygame.transform.scale(pygame.image.load("Hero/" + path).convert_alpha(),(84, 161) ) for path in H_files]
        self.invisible = [pygame.image.load("Hero/a996.png").convert_alpha() for i in range(0,len(self.human))]
        self.block = pygame.Rect(self.screen.get_width() / 3 + 30, self.screen.get_height() / 2 - 40,
                                 40, 140)
        self.image = pygame.transform.scale(pygame.image.load("Hero/a.png").convert_alpha(),(84, 161) )

        self.start_time = -4 * 1000
        self.make_me_visible = False

    def is_invincable(self):
        self.make_me_visible = False
        end_time = pygame.time.get_ticks()
        seconds_passed = (end_time - self.start_time) / 1000
        #print(i)
        #print(seconds_passed,"  ",self.wait_list[i])

        if seconds_passed > self.invincible_time:
            return False
        # print(seconds_passed)
        if seconds_passed > (self.invincible_time - 0.06):
            self.make_me_visible = True
        return True
    def hit_animation(self):
        #print(self.start_time)
        if self.make_me_visible == True:
            self.human = self.visible
        else:
            if self.fps2 == self.delay:
                self.fps2 = 0
                if self.peekaboo == False:
                    self.human = self.invisible
                    self.peekaboo = True
                else:
                    self.human = self.visible
                    self.peekaboo = False
            self.fps2 += 1

    def relocate(self,x,y):
        self.block = self.block.move(self.player_speed * x, self.player_speed * y)

    def walk_front(self):
        if (self.fps == self.delay):
            self.fps = 0
            self.frames += 1
        self.fps += 1
        self.frames = self.frames % 4
        return self.human[self.frames + 1]

    def walk_right(self):
        if (self.fps == self.delay):
            self.fps = 0
            self.frames += 1
        self.fps += 1
        self.frames = self.frames % 6
        return self.human[self.right_offset + self.frames + 1]

    def walk_left(self):
        if (self.fps == self.delay):
            self.fps = 0
            self.frames += 1
        self.fps += 1
        self.frames = self.frames % 6
        return self.human[self.left_offset+ self.frames + 1]

    def walk_back(self):
        if self.fps == self.delay:
            self.fps = 0
            self.frames += 1
        self.fps += 1
        self.frames = self.frames % 4
        return self.human[self.back_offset + self.frames + 1]



    def stay_front(self):
        return self.human[0]

    def stay_right(self):
        return self.human[self.right_offset]

    def stay_left(self):
        return self.human[self.left_offset]

    def stay_back(self):
        return self.human[self.back_offset]

    def set_lives(self,lives):
        self.lives = lives

    def take_life(self):
        if self.lives == 0:
            self.lives = 4
        self.lives -= 1

    def init_countable(self):  # number of an image loaded at a time
        self.peekaboo = False
        self.invincible_time = 2.5
        self.straight_count = 0
        self.profile_count = 0
        self.frames = 0
        self.fps = 0
        self.fps2=  0
        self.delay = 4;
        #player_stats
        self.player_speed = 17
        self.lives = 3
        self.const_lives = 3
        self.ammo = 0
        self.points = 0
        self.money = 0
        # Positioning Offsets [front,left,right,back]
        self.left_offset = 5
        self.right_offset = 12
        self.back_offset = 19

    def make_invisible(self):
        self.human = self.invisible

    def make_visible(self):
        self.human = self.visible




