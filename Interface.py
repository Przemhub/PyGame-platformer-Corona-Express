from math import fabs
from pygame import image as im
import pygame
class Interface():
    def __init__(self):
        self.init_objects()
        self.speed = 20
        self.seconds = 0
        self.start_time = pygame.time.get_ticks()
        self.paper_transition = False
        self.pathX_list = []
        self.pathY_list = []
        self.wait_list = []
        self.init_locations()
        self.chosen_list = []
    def set_Paper(self,places_list):
        self.chosen_list.clear()
        for place in places_list:
            self.chosen_list.append(self.location_list[place])
    def set_timer_text(self,seconds):
        self.seconds = seconds
        min = int(seconds/60)
        sec = seconds % 60
        if sec < 10:
            self.timer_text = self.timer_font.render(str(min) + ":0" + str(sec), True, (255, 255, 255))
        else:
            self.timer_text = self.timer_font.render(str(min) + ":" + str(sec),True,(255,255,255))

    def init_locations(self):
        self.location_list = [im.load("GUI/armory.png"), im.load("GUI/joker.png"), im.load("GUI/hunt.png"),
                              im.load("GUI/church.png"), \
                              im.load("GUI/weaponry.png"), im.load("GUI/villa.png"), im.load("GUI/house.png"),
                              im.load("GUI/post.png")]
        self.locations_hash = {im.load("GUI/armory.png").get_height(): 0, im.load("GUI/joker.png").get_height(): 1,
                               im.load("GUI/hunt.png").get_height(): 2, im.load("GUI/church.png").get_height(): 3, \
                               im.load("GUI/weaponry.png").get_height(): 4, im.load("GUI/villa.png").get_height(): 5,
                               im.load("GUI/house.png").get_height(): 6, im.load("GUI/post.png").get_height(): 7}
        self.locations_block = pygame.Rect(1700, 350, 10, 10)


    def init_objects(self):
        self.Life = im.load("GUI/box.png").convert_alpha()
        self.Paper = im.load("GUI/paper.png").convert_alpha()
        self.Skull = im.load("GUI/death.png").convert_alpha()
        self.cursor = pygame.transform.scale(pygame.image.load("GUI/Menu/Cursor.png"),(360,70))
        self.Paper_finish = im.load("GUI/paper2.png").convert_alpha()
        self.Options = pygame.Surface((200, 110))
        self.Options.fill((0,0,0))
        self.Options.set_alpha(180)




        self.Life_block = pygame.Rect(62, 42, self.Life.get_width(), self.Life.get_height())
        self.Paper_block = pygame.Rect(1640, 310, self.Paper.get_width(), self.Paper.get_height())
        self.Paper_finish_block = pygame.Rect(550,200, 450,500)
        self.cursor_block = pygame.Rect(630, 330, 438, 100)
        self.Options_block = pygame.Rect(self.Paper_finish_block.x + 160,self.Paper_finish_block.y + 140,200,100)

        self.timer_font = pygame.font.SysFont("Calibri", 54, bold=True)
        self.timer_text = self.timer_font.render("", True, (255, 255, 255))
        self.timer_background = pygame.Surface((125, 56))
        self.timer_background.fill((0, 0, 0))
        self.timer_background.set_alpha(180)

        self.congratz_font = pygame.font.SysFont('Gabriola',74)
        self.points_font = pygame.font.SysFont('Calibri', 40, bold=True, italic=True)
        self.congratz_text = self.congratz_font.render("Gratulacje!", True,(0,0,0))
        self.points_text = self.points_font.render("Punkty: ",True,(0,0,0))
        self.money_text = self.points_font.render("Budżet: ",True,(0,0,0))
        self.continue_text = self.points_font.render("Kontynuuj", True, (255,255,255))
        self.shop_text = self.points_font.render("Sklep",True,(255,255,255))
        paperx = self.Paper_finish_block.x
        papery = self.Paper_finish_block.y
        self.congratz_block = pygame.Rect(paperx + 140, papery + 70,200,50)
        self.points_block = pygame.Rect(paperx + 130, papery + 255,200,50)
        self.money_block = pygame.Rect(paperx + 130, papery + 385,200,50)
        self.continue_block = pygame.Rect(10, 10,100,40)
        self.shop_block = pygame.Rect( 40, 60,100,40)

    def update_texts(self,points,money):
        self.points_text = self.points_font.render("Punkty: "+str(points),True,(0,0,0))
        self.money_text = self.points_font.render("Budżet: $" + str(money),True,(0,0,0))


    def is_waiting(self, i):
        end_time = pygame.time.get_ticks()
        seconds_passed = (end_time - self.start_time) / 1000
        if seconds_passed > self.wait_list[i]:
            return False
        return True
    def fade_paper(self):
        self.paper_transition = True
    def animate_paper(self):
        if self.paper_transition == True:
            self.stop_waiting()
            self.paper_transition = False
        self.move("X-290W10000,X290W10000")
    def stop_waiting(self):
        self.start_time = -10000 * 1000
    def move(self, command):
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
                return
            # check if found number is negative and set flag sign = -1
            sign = self.check_sign(x, y)
            self.Paper_block = self.Paper_block.move(self.speed * sign, 0)
            self.locations_block = self.locations_block.move(self.speed * sign, 0)

        elif y < x:
            coord = 'y'
            x = y
            if self.is_waiting(x):
                return
            # check if found number is negative and set flag sign = -1
            sign = self.check_sign(x, y)
            self.Paper_block = self.Paper_block.move(0, self.speed * sign)
            self.locations_block = self.locations_block.move(0, self.speed * sign)
        else:
            coord = 'xy'
            if x < len(self.pathX_list):
                if self.is_waiting(x):
                    return
                sign = self.check_sign(x, y)
                self.Paper_block = self.Paper_block.move(self.speed * sign, self.speed * sign)
                self.locations_block = self.locations_block.move(self.speed * sign, self.speed * sign)
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
        for cmd in command.split(','):
            # pick out coord value and write to dist
            for char in list(cmd):
                if char.isdigit() or char == '-':
                    dist = float(cmd[cmd.index(char):cmd.index('W')])
                    break
            # pick Waiting time from command
            wait = float(cmd[(cmd.index('W') + 1):])
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