import pygame
from os import listdir


class Boy:

    def __init__(self,screen):
        #Statistics
        self.init_stats()
        #Misc
        H_files = listdir("Hero/Head")
        T_files = listdir("Hero/Torso")
        L_files = listdir("Hero/Legs")
        W_files = listdir("Hero/Weaps")
        self.label_items()
        self.init_countable()
        self.screen = screen
        #Images and Objects
        self.head = [pygame.image.load("Hero/Head/" + path) for path in H_files]
        self.torso = [pygame.image.load("Hero/Torso/" + path) for path in T_files]
        self.legs = [pygame.image.load("Hero/Legs/" + path) for path in L_files]

        self.weapon = [pygame.image.load("Hero/Weaps/" + path) for path in W_files]
        self.Head_block = pygame.Rect(self.screen.get_width() / 2, self.screen.get_height()/2-20, 42, 57)
        self.Torso_block = pygame.Rect(self.screen.get_width() / 2-6, self.screen.get_height()/2+23, 53, 78)
        self.Legs_block = pygame.Rect(self.screen.get_width() / 2+4, self.screen.get_height() / 2 +87,
                                      35, 44)
        self.Weapon_block = pygame.Rect(self.screen.get_width() / 2 + 10, self.screen.get_height() / 2 +90,
                                      42,30)
        self.block = pygame.Rect(self.screen.get_width() / 2 + 100, self.screen.get_height() / 2 + 1230,
                                        42, 57)

    def change_head(self, head):
        self.head_count = head

    def change_torso(self, torso):
        self.torso_count = torso

    def change_legs(self, legs):
        self.legs_count = legs

    def change_weapon(self, weapon):
        self.weapon = weapon
    def relocate(self,x,y):
        self.Head_block = self.Head_block.move(self.player_speed*x, self.player_speed*y)
        self.Torso_block = self.Torso_block.move(self.player_speed*x, self.player_speed*y)
        self.Legs_block = self.Legs_block.move(self.player_speed*x, self.player_speed*y)
        self.Weapon_block = self.Weapon_block.move(self.player_speed*x, self.player_speed*y)
    def walk_front(self):
        if (self.fps == self.delay):
            self.fps = 0
            self.frames += 1
        self.fps += 1
        self.frames = self.frames % 4
        return (self.head[self.head_count + self.frames], self.torso[self.torso_count + self.frames], \
                self.legs[self.legs_count + self.frames], self.weapon[self.weapon_count + self.frames])

    def walk_right(self):
        if (self.fps == self.delay):
            self.fps = 0
            self.frames += 1
        self.fps += 1
        self.frames = self.frames % 4
        return (self.head[self.right_offset + self.head_count + self.frames],
                self.torso[self.right_offset + self.torso_count + self.frames], \
                self.legs[self.right_offset + self.legs_count + self.frames],
                self.weapon[self.right_offset + self.weapon_count + self.frames])

    def walk_left(self):
        if (self.fps == self.delay):
            self.fps = 0
            self.frames += 1
        self.fps += 1
        self.frames = self.frames % 4
        return (self.head[self.left_offset + self.head_count + self.frames],
                self.torso[self.left_offset + self.torso_count + self.frames], \
                self.legs[self.left_offset + self.legs_count + self.frames],
                self.weapon[self.left_offset + self.weapon_count + self.frames])

    def walk_back(self):
        if self.fps == self.delay:
            self.fps = 0
            self.frames += 1
        self.fps += 1
        self.frames = self.frames % 4
        return (self.head[self.back_offset + self.head_count + self.frames], self.torso[
            self.back_offset + self.torso_count + self.frames], \
                self.legs[self.back_offset + self.legs_count + self.frames],
                self.weapon[self.back_offset + self.weapon_count + self.frames])

    def stay_front(self):
        return (self.head[self.head_count], self.torso[
            self.torso_count], \
            self.legs[self.legs_count], self.weapon[self.weapon_count])

    def stay_right(self):
        return (self.head[self.right_offset + self.head_count], self.torso[
            self.right_offset + self.torso_count], \
                self.legs[self.right_offset + self.legs_count], self.weapon[self.right_offset + self.weapon_count])

    def stay_left(self):
        return (self.head[self.left_offset + self.head_count], self.torso[
            self.left_offset + self.torso_count], \
                self.legs[self.left_offset + self.legs_count], self.weapon[self.left_offset + self.weapon_count])

    def stay_back(self):
        return (self.head[self.back_offset + self.head_count], self.torso[
            self.back_offset + self.torso_count], \
                self.legs[self.back_offset + self.legs_count], self.weapon[self.back_offset + self.weapon_count])

    def hit_left(self):
        if (self.fps == self.delay):
            self.fps = 0
            self.frames += 1
        self.fps += 1
        self.frames = self.frames % 2
        return (self.head[self.head_count + self.frames + self.hit_offsetL],
                self.torso[self.torso_count + self.frames + self.hit_offsetL], \
                self.legs[self.legs_count + self.frames + self.hit_offsetL],
                self.weapon[self.weapon_count + self.frames + self.hit_offsetL])

    def hit_right(self):
        if (self.fps == self.delay):
            self.fps = 0
            self.frames += 1
        self.fps += 1
        self.frames = self.frames % 2
        return (self.head[self.head_count + self.frames + self.hit_offsetR],
                self.torso[self.torso_count + self.frames + self.hit_offsetR], \
                self.legs[self.legs_count + self.frames + self.hit_offsetR],
                self.weapon[self.weapon_count + self.frames + self.hit_offsetR])

    def hit_front(self):
        if (self.fps == self.delay):
            self.fps = 0
            self.frames += 1
        self.fps += 1
        self.frames = self.frames % 2
        return (self.head[self.head_count + self.frames + self.hit_offset], self.torso[self.torso_count + self.frames + self.hit_offset], \
                self.legs[self.legs_count + self.frames + self.hit_offset], self.weapon[self.weapon_count + self.frames + self.hit_offset])
    def hit_back(self):
        if (self.fps == self.delay):
            self.fps = 0
            self.frames += 1
        self.fps += 1
        self.frames = self.frames % 2
        return (self.head[self.head_count + self.frames + self.hit_offsetB], self.torso[self.torso_count + self.frames + self.hit_offsetB], \
                self.legs[self.legs_count + self.frames + self.hit_offsetB], self.weapon[self.weapon_count + self.frames + self.hit_offsetB])
    def label_items(self):  # names of items in game
        self.HELMET1 = 0
        self.TORSO1 = 0
        self.LEGS1 = 0
        self.WEAPON1 = 0

    def init_countable(self):  # number of an image loaded at a time
        self.head_count = 0
        self.torso_count = 0
        self.legs_count = 0
        self.straight_count = 0
        self.profile_count = 0
        self.weapon_count = 0
        self.frames = 0
        self.fps = 0
        self.delay = 4;
        self.player_speed = 5
        # Positioning Offsets [front,left,right,back]
        self.left_offset = 4
        self.right_offset = 8
        self.back_offset = 12
        self.hit_offset = 16
        self.hit_offsetL = 18
        self.hit_offsetR = 20
        self.hit_offsetB = 22
    def init_stats(self):
        self.HP = 100
        self.EXP = 0
        self.DMG = 10
        self.HEAD = 0
        self.TORSO = 0
        self.LEGS = 0
        self.ARMED = False