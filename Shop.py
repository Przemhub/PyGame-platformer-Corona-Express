import time

import pygame
import sys
class Shop:
    def __init__(self,screen):
        self.money = 0
        self.screen = screen
        self.init_images()
        self.player_stack = StackGrid(650, 300)
        self.buff_stack = StackGrid(1100, 300)
        self.init_player_stack()
        self.init_buff_stack()
        self.first_time = True
        self.enter = False
        self.init_cursor()
        self.init_option_surface()
        self.cursor_sound = pygame.mixer.Sound('Soundtrack/cursor.ogg')
        self.load_sound = pygame.mixer.Sound('Soundtrack/load.ogg')
        self.caching = pygame.mixer.Sound('Soundtrack/buy.ogg')
        self.clk = pygame.time.Clock()
        self.delay = 0
        self.delay_const = 4

    def start(self,money,upgrade_dict):
        self.upgrade_dict = upgrade_dict
        self.old_dict = upgrade_dict.copy()
        self.money = money
        self.clear_cursor()
        self.setup_interface()
        pygame.mixer.music.load("Soundtrack/elevator_music.mp3")
        pygame.mixer.music.play()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)
            self.screen.fill((255, 255, 255))
            self.draw()
            self.move_cursor()
            pygame.display.flip()
            return_val = self.options_event()
            if len(return_val) > 2:
                pygame.mixer.music.stop()
                return return_val
            self.delay+=1
            self.clk.tick(30)

    def draw(self):
        i = 0
        self.screen.blit(self.background,(0,0))
        self.screen.blit(self.money_surf,(1430,790))
        self.screen.blit(self.font.render(str(self.money),True,(255,255,255)),(1450,800))
        self.screen.blit(self.option_surf,self.option_block)
        self.screen.blit(self.accept,self.option_block.move(20,30))
        self.screen.blit(self.cancel,self.option_block.move(40,120))
        self.screen.blit(self.font.render("Postac",True,(255,255,255)),self.player_stack.block.move(0,-110))
        self.screen.blit(self.player_surface,self.player_stack.block.move(-20,-20))
        for skill in self.player_stack:
            self.screen.blit(self.image_list[i], self.player_stack.block.move(0,i*120))
            self.screen.blit(skill[0],self.player_stack.block.move(80,i*120))
            for n_circles in range(0,skill[1]):
                if n_circles < skill[2]:
                    pygame.draw.circle(self.screen, (255, 255, 255),self.player_stack.block.move(100 + (n_circles * 40), i * 120 + 60).topleft, 10,7)
                else:
                    pygame.draw.circle(self.screen, (255, 255, 255),self.player_stack.block.move(100 + (n_circles * 40), i * 120 + 60).topleft, 10, 2)
            level = self.player_stack.get_level(i)
            if skill[2] < skill[1]:
                self.screen.blit(self.font2.render("$" + str(self.player_stack.get_prices(i, level)), True, (255, 255, 255)),
                                 self.player_stack.block.move(280 ,i * 120))
            else:
                self.screen.blit(self.font2.render("MAX", True, (255, 255, 255)),self.player_stack.block.move(280 ,i * 120))
            i += 1
        self.screen.blit(self.font.render("Znajdźki",True,(255,255,255)),self.buff_stack.block.move(0,-110))
        self.screen.blit(self.buff_surface, self.buff_stack.block.move(-20,-20))
        i = 0
        for buff in self.buff_stack:
            self.screen.blit(self.image_list[i + (len(self.player_stack))], self.buff_stack.block.move(0, i *120))
            self.screen.blit(buff[0], self.buff_stack.block.move(80, i * 120))
            for n_circles in range(0, buff[1]):
                if n_circles < buff[2]:
                    pygame.draw.circle(self.screen, (255, 255, 255),self.buff_stack.block.move(100 + (n_circles * 40), i* 120 + 60).topleft, 10, 7)
                else:
                    pygame.draw.circle(self.screen, (255, 255, 255),self.buff_stack.block.move(100 + (n_circles * 40), i * 120 + 60).topleft, 10, 2)
            level = self.buff_stack.get_level(i)
            if buff[2] < buff[1]:
                self.screen.blit(self.font2.render("$" + str(self.buff_stack.get_prices(i, level)), True, (255, 255, 255)),
                                 self.buff_stack.block.move(280, i * 120))
            else:
                self.screen.blit(self.font2.render("MAX", True, (255, 255, 255)),self.buff_stack.block.move(280 ,i * 120))
            i += 1
        self.screen.blit(self.cursor,self.cursor_block)

    def move_cursor(self):
        if (pygame.key.get_pressed()[pygame.K_s] or pygame.key.get_pressed()[pygame.K_DOWN]) and self.delay >= self.delay_const:
            self.delay = 0
            if self.choices[self.choices_i] < self.max_choices[self.choices_i]:
                self.choices[self.choices_i] += 1
                self.cursor_sound.play()
                if self.choices_i == 0:
                    self.cursor_block = self.cursor_block.move(0, 100)
                else:
                    self.cursor_block = self.cursor_block.move(0, 120)

        elif (pygame.key.get_pressed()[pygame.K_w] or pygame.key.get_pressed()[pygame.K_UP]) and self.delay >= self.delay_const:
            self.delay = 0
            if self.choices[self.choices_i] > 0:
                self.choices[self.choices_i] -= 1
                self.cursor_sound.play()
                if self.choices_i == 0:
                    self.cursor_block = self.cursor_block.move(0, -100)
                else:
                    self.cursor_block = self.cursor_block.move(0, -120)
        elif (pygame.key.get_pressed()[pygame.K_d] or pygame.key.get_pressed()[pygame.K_RIGHT]) and self.delay >= self.delay_const:
            self.delay = 0
            if self.choices_i < 2:
                self.choices_i += 1
                if self.choices_i == 1:
                    self.cursor_block = self.cursor_block.move(440,0)
                else:
                    self.cursor_block = self.cursor_block.move(450,0)
                if self.choices[self.choices_i - 1] > self.max_choices[self.choices_i]:
                    self.choices[self.choices_i] = self.max_choices[self.choices_i]
                else:
                    self.choices[self.choices_i] = self.choices[self.choices_i - 1]
                self.cursor_sound.play()
                if self.choices_i == 0:
                    self.cursor_block = pygame.Rect(self.cursor_block.x, 300 + (100 * self.choices[self.choices_i]), 438, 200)
                else:
                    self.cursor_block = pygame.Rect(self.cursor_block.x, 300 + (120 * self.choices[self.choices_i]), 438,
                                                    200)
        elif (pygame.key.get_pressed()[pygame.K_a] or pygame.key.get_pressed()[pygame.K_LEFT]) and self.delay >= self.delay_const:
            self.delay = 0
            if self.choices_i > 0:
                self.choices_i -= 1
                if self.choices_i == 0:
                    self.cursor_block = self.cursor_block.move(-440, 0)
                else:
                    self.cursor_block = self.cursor_block.move(-450, 0)
                if self.choices[self.choices_i + 1] > self.max_choices[self.choices_i]:
                    self.choices[self.choices_i] = self.max_choices[self.choices_i]
                else:
                    self.choices[self.choices_i] = self.choices[self.choices_i + 1]
                self.cursor_sound.play()
                if self.choices_i == 0:
                    self.cursor_block = pygame.Rect(self.cursor_block.x, 300 + (100 * self.choices[self.choices_i]),438, 200)
                else:
                    self.cursor_block = pygame.Rect(self.cursor_block.x, 300 + (120 * self.choices[self.choices_i]),438,200)
        elif pygame.key.get_pressed()[pygame.K_RETURN] == True and self.delay >= self.delay_const:
            self.delay = 0
            if self.choices_i == 0:
                self.enter = True
                return
            elif self.choices_i == 1:
                self.buy_skill()
            elif self.choices_i == 2:
                self.buy_buff()

    def buy_skill(self):
        level = self.player_stack.get_level(self.choices[self.choices_i])
        max_level = self.player_stack.get_max_level(self.choices[self.choices_i])
        if level < max_level:
            if self.money >= self.player_stack.get_prices(self.choices[self.choices_i],level):
                self.money -= self.player_stack.list[self.choices[self.choices_i]][3][level]
                self.player_stack.level_up(self.choices[self.choices_i])
                skill = self.player_stack.list[self.choices[self.choices_i]][4]
                if skill == "Untouchable":
                    self.upgrade_dict[skill] += 0.6
                else:
                    self.upgrade_dict[skill] += 1
                self.upgrade_dict["Money"] = self.money
                self.caching.play()

    def buy_buff(self):
        level = self.buff_stack.list[self.choices[self.choices_i]][2]
        max_level = self.buff_stack.get_max_level(self.choices[self.choices_i])
        if level < max_level:
            if self.money >= self.buff_stack.get_prices(self.choices[self.choices_i], level):
                self.money -= self.buff_stack.get_prices(self.choices[self.choices_i], level)
                self.buff_stack.level_up(self.choices[self.choices_i])
                buff = self.buff_stack.list[self.choices[self.choices_i]][4]
                self.upgrade_dict[buff] += 1
                self.upgrade_dict["Money"] = self.money
                self.caching.play()

    def options_event(self):
        if self.choices_i == 0 and self.enter == True:
            self.enter = False
            if self.choices[self.choices_i] == 0:
                return self.upgrade_dict
            elif self.choices[self.choices_i] == 1:
                self.upgrade_dict = self.old_dict
                self.backup_interface()
                return self.old_dict
        return {"None":None}
    def backup_interface(self):
        self.player_stack.clear()
        self.buff_stack.clear()
        self.init_player_stack()
        self.init_buff_stack()
        self.first_time = True


    #sets up whole graphic interface, but only once in a game (for loaded games)
    def setup_interface(self):
        if self.first_time == True:
            self.first_time = False
            if self.upgrade_dict["SpeedUp"] == 6:
                self.buff_stack.level_up(0)
            elif self.upgrade_dict["SpeedUp"] == 7:
                self.buff_stack.level_up(0)
                self.buff_stack.level_up(0)
            elif self.upgrade_dict["SpeedUp"] == 8:
                self.buff_stack.level_up(0)
                self.buff_stack.level_up(0)
                self.buff_stack.level_up(0)
            if self.upgrade_dict["Invincible"] == 6:
                self.buff_stack.level_up(1)
            elif self.upgrade_dict["Invincible"] == 7:
                self.buff_stack.level_up(1)
                self.buff_stack.level_up(1)
            elif self.upgrade_dict["Invincible"] == 8:
                self.buff_stack.level_up(1)
                self.buff_stack.level_up(1)
                self.buff_stack.level_up(1)
            if self.upgrade_dict["StopTime"] == 6:
                self.buff_stack.level_up(2)
            elif self.upgrade_dict["StopTime"] == 7:
                self.buff_stack.level_up(2)
                self.buff_stack.level_up(2)
            elif self.upgrade_dict["StopTime"] == 8:
                self.buff_stack.level_up(2)
                self.buff_stack.level_up(2)
                self.buff_stack.level_up(2)
            if self.upgrade_dict["Speed"] == 18: #0 Speed 1 Lives 2 Untouchable 3 Buffs
                self.player_stack.level_up(0)
            elif self.upgrade_dict["Speed"] == 19:
                self.player_stack.level_up(0)
                self.player_stack.level_up(0)
            elif self.upgrade_dict["Speed"] == 20:
                self.player_stack.level_up(0)
                self.player_stack.level_up(0)
                self.player_stack.level_up(0)
            if self.upgrade_dict["Lives"] == 4:
                self.player_stack.level_up(1)
            elif self.upgrade_dict["Lives"] == 5:
                self.player_stack.level_up(1)
                self.player_stack.level_up(1)
            if self.upgrade_dict["Untouchable"] == 3.1:
                self.player_stack.level_up(2)
            elif self.upgrade_dict["Untouchable"] == 3.7 :
                self.player_stack.level_up(2)
                self.player_stack.level_up(2)
            if self.upgrade_dict["Buffs"] == 4:
                self.player_stack.level_up(3)
            elif self.upgrade_dict["Buffs"] == 5:
                self.player_stack.level_up(3)
                self.player_stack.level_up(3)
            elif self.upgrade_dict["Buffs"] == 6:
                self.player_stack.level_up(3)
                self.player_stack.level_up(3)
                self.player_stack.level_up(3)

    def init_cursor(self):
        self.choices = [0,0,0]
        self.choices_i = 0
        self.max_choices = [1,len(self.player_stack) - 1,len(self.buff_stack) - 1]
        self.cursor = pygame.Surface((300,100))
        self.cursor.fill((255,255,255))
        self.cursor.set_alpha(100)
        self.cursor_block = pygame.Rect(190, 290, 438, 100)

    def init_images(self):
        self.background = pygame.image.load("GUI/background.png")
        self.speed = pygame.image.load("GUI/Shop/Speed.png").convert_alpha()
        self.untouchable = pygame.image.load("GUI/Shop/Invincible.png").convert_alpha()
        self.lives = pygame.image.load("GUI/Shop/Box.png")
        self.buffs = pygame.image.load("GUI/Shop/Buffs.png")
        self.invincibility = pygame.image.load("Buffs/Invincible.png")
        self.speedUp = pygame.image.load("Buffs/SpeedUp.png")
        self.stopTime = pygame.image.load("Buffs/StopTime.png")
        self.player_surface = pygame.Surface((390,460))
        self.player_surface.fill((0,0,0))
        self.player_surface.set_alpha(180)
        self.buff_surface = pygame.Surface((390, 400))
        self.buff_surface.fill((0, 0, 0))
        self.buff_surface.set_alpha(180)
        self.font2 = pygame.font.SysFont("Calibri",32,bold=True)
        self.money_surf = pygame.Surface((190,70))
        self.money_surf.fill((0,0,0))
        self.money_surf.set_alpha(160)
        self.image_list = []

    def init_option_surface(self):
        self.option_surf = pygame.Surface((300, 220))
        self.option_surf.set_alpha(180)
        self.option_surf.fill((0,0,0))
        self.font = pygame.font.SysFont("Calibri",64,bold=True)
        self.accept = self.font.render("Akceptuj",True,(255,255,255))
        self.cancel = self.font.render("Anuluj",True,(255,255,255))
        self.option_block = pygame.Rect(190,290,350,200)

    def init_buff_stack(self):
        self.buff_stack.add_ability("Buty Hermesa",3,(300,650,900),"SpeedUp")
        self.image_list.append(self.speedUp)
        self.buff_stack.add_ability("Maska Gazowa",3,(300,650,1000),"Invincible")
        self.image_list.append(self.invincibility)
        self.buff_stack.add_ability("Stop Czas",3,(400,800,1100),"StopTime")
        self.image_list.append(self.stopTime)

    def init_player_stack(self):
        self.player_stack.add_ability("Prędkość",3,(400,800,1000),"Speed")
        self.image_list.append(self.speed)
        self.player_stack.add_ability("Życia",2,(500,1400),"Lives")
        self.image_list.append(self.lives)
        self.player_stack.add_ability("Nietykalność",2,(450,1000),"Untouchable")
        self.image_list.append(self.untouchable)
        self.player_stack.add_ability("Znajdźki",3,(400,900,1300),"Buffs")
        self.image_list.append(self.buffs)
    def clear_cursor(self):
        self.choices_i = 0
        self.choices[0] = 0
        self.choices[1] = 0
        self.choices[2] = 0
        self.cursor_block = pygame.Rect(190, 290, 438, 100)
class StackGrid:
    def __init__(self,x,y):
        self.block = pygame.Rect(x,y,160,400)
        self.list= []
        self.font = pygame.font.SysFont("Calibri",32,True)
    def add_ability(self,text,levels,prices,name):
        self.list.append([self.font.render(text,True,(255,255,255)),levels,0,prices,name])
    def get_prices(self, index, level):
        return self.list[index][3][level]
    def get_max_level(self,index):
        return self.list[index][1]
    def get_text(self,index):
        return self.list[index][0]
    def get_name(self,index):
        return self.list[index][4]
    def pop_ability(self,index):
        self.list.remove(index)
    def level_up(self,index):
        self.list[index][2] += 1
    def get_level(self,index):
        return self.list[index][2]
    def clear(self):
        self.list.clear()
    def __iter__(self):
        return (val for val in self.list)
    def __len__(self):
        return len(self.list)
