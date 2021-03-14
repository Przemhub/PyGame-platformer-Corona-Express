from math import fabs
from os import listdir
from random import Random
import pygame

class Animal():
    def __init__(self,north, x, y, speed):
        self.x = x
        self.y = y
        self.start_time = pygame.time.get_ticks()
        self.speed = speed
        self.north = north
        self.move_i = 0
        self.stay_i = 0
        self.block = pygame.Rect(self.north.x + x, self.north.y + y, 110, 80)
        self.pathX_list = []
        self.pathY_list = []
        self.wait_list = []
        self.init_countable()
        rand = Random().randint(1, 2)

        NPC_files = listdir("Animals/" + str(rand))
        self.human = [
            pygame.transform.scale(pygame.image.load("Animals/" + str(rand) + "/" + path).convert_alpha(), (161, 100)) for
            path in
            NPC_files]
        self.action = [self.stay_front, self.walk_front, self.stay_right,
                       self.stay_left, self.walk_right, self.walk_left, \
                       self.stay_back, self.walk_back,self.invisible]
        self.movement = self.action[self.move_i]()

    # send string containing commands to move NPC to location, example: "X50W0,XY60W0,Y-10W0", are three moves
    # if you want to move 30 pixels to right and wait 2 seconds "X30W2"
    def is_waiting(self, i):
        end_time = pygame.time.get_ticks()
        seconds_passed = (end_time - self.start_time) / 1000

        if seconds_passed > self.wait_list[i]:
            return False
        return True
    def is_hiding(self, cmd):
        try:
            cmd.index("H")
        except Exception:
            return False
        return True

    def move(self, command):
        self.move_i = self.stay_i
        x = 0
        y = 0
        sign = 1  # in case of a negative number
        coord = 'z'
        # analyze command for the first time
        if len(self.pathX_list) == 0:
            self.analyze_cmd(command)
        # find values that are not zeros
        x = len(self.pathX_list)  # in case value has not been found, (important)
        y = len(self.pathY_list)
        for path in self.pathX_list:
            if path != 0:
                x = self.pathX_list.index(path)
                break
        for path in self.pathY_list:
            if path != 0:
                y = self.pathY_list.index(path)
                break
        if x < y:
            coord = 'x'
            y = x
            if self.is_waiting(x):
                if self.is_hiding(x) == True:
                    self.move_i = 8
                    self.stay_i = 8
                return


            # check if found number is negative and set flag sign = -1
            sign = self.check_sign(x, y)
            if sign == -1:
                self.stay_i = 3
                self.move_i = 5
            else:
                self.stay_i = 2
                self.move_i = 4
            self.block = self.block.move(self.speed * sign, 0)

        elif y < x:
            coord = 'y'
            x = y
            if self.is_waiting(x):
                if self.is_hiding(x) == True:
                    self.move_i = 8
                    self.stay_i = 8
                return

            # check if found number is negative and set flag sign = -1
            sign = self.check_sign(x, y)
            if sign == -1:
                self.stay_i = 6
                self.move_i = 7
            else:
                self.stay_i = 0
                self.move_i = 1
            self.block = self.block.move(0, self.speed * sign)
        else:
            coord = 'xy'
            if x < len(self.pathX_list):
                if self.is_waiting(x):
                    if self.is_hiding(x) == True:
                        self.move_i = 8
                        self.stay_i = 8
                    return
                sign = self.check_sign(x, y)
                if sign == -1:
                    self.stay_i = 3
                    self.move_i = 5
                else:
                    self.stay_i = 2
                    self.move_i = 4
                self.block = self.block.move(self.speed * sign, self.speed * sign)
        if x == len(self.pathX_list) and y == len(self.pathY_list):
            self.pathY_list.clear()
            self.pathX_list.clear()
            self.wait_list.clear()
            return
        self.pathX_list[x] -= (self.pathX_list[x] > 0) * self.speed
        self.pathY_list[y] -= (self.pathY_list[y] > 0) * self.speed

        if self.pathX_list[x] < 0:
            self.pathX_list[x] = 0
        if self.pathY_list[y] < 0:
            self.pathY_list[y] = 0
        # check if a command has been finished
        if coord == 'x':
            if self.pathX_list[x] == 0:
                self.start_time = pygame.time.get_ticks()
        elif coord == 'y':
            if self.pathY_list[y] == 0:
                self.start_time = pygame.time.get_ticks()
        elif coord == 'xy':
            if self.pathX_list[x] == 0 and self.pathY_list[y] == 0:
                self.start_time = pygame.time.get_ticks()

        self.pathX_list[x] = self.pathX_list[x] * sign
        self.pathY_list[y] = self.pathY_list[y] * sign

    def check_sign(self, x, y):
        if self.pathX_list[x] < 0 or self.pathY_list[y] < 0:
            self.pathY_list[y] = fabs(self.pathY_list[y])
            self.pathX_list[x] = fabs(self.pathX_list[x])
            return -1
        return 1

    # parses the command into pathX_list pathY_list and wait_list
    def analyze_cmd(self, command):
        dist = 0
        wait = 0
        hide = 0
        for cmd in command.split(','):
            # pick out coord value and write to dist
            for char in list(cmd):
                if char.isdigit() or char == '-':
                    try:
                        dist = float(cmd[cmd.index(char):cmd.index('W')])
                    except Exception:
                        dist = float(cmd[cmd.index(char):cmd.index('H')])
                    break
            # pick Waiting time from command
            try:
                wait = float(cmd[(cmd.index('W') + 1):])
            except Exception:
                wait = float(cmd[(cmd.index('H') + 1):])
            self.wait_list.append(wait)
            if cmd[0] == 'X' and cmd[1] == 'Y':
                self.pathX_list.append(dist)
                self.pathY_list.append(dist)
            elif cmd[0] == 'Y':
                self.pathY_list.append(dist)
                self.pathX_list.append(0)
            elif cmd[0] == 'X':
                self.pathX_list.append(dist)
                self.pathY_list.append(0)
            else:
                raise Exception("Incorrect command, example \"X50,XY60,Y-10\"")

    def walk_front(self):
        if (self.fps == self.delay):
            self.fps = 0
            self.frames += 1
        self.fps += 1
        self.frames = self.frames % 3
        return self.human[self.frames]

    def walk_right(self):
        if (self.fps == self.delay):
            self.fps = 0
            self.frames += 1
        self.fps += 1
        self.frames = self.frames % 3
        return self.human[self.right_offset + self.frames]

    def walk_left(self):
        if (self.fps == self.delay):
            self.fps = 0
            self.frames += 1
        self.fps += 1
        self.frames = self.frames % 3
        return self.human[self.left_offset + self.frames]

    def walk_back(self):
        if self.fps == self.delay:
            self.fps = 0
            self.frames += 1
        self.fps += 1
        self.frames = self.frames % 3
        return self.human[self.back_offset + self.frames]

    def stay_front(self):
        return self.human[0]

    def stay_right(self):
        return self.human[self.right_offset]

    def stay_left(self):
        return self.human[self.left_offset]

    def stay_back(self):
        return self.human[self.back_offset]
    def invisible(self):
        return self.human[8]
    def init_countable(self):  # number of an image loaded at a time

        self.straight_count = 0
        self.profile_count = 0
        self.frames = 0
        self.fps = 0
        self.delay = 4;
        # Positioning Offsets [front,left,right,back]
        self.left_offset = 0
        self.right_offset = 4
        self.back_offset = 0