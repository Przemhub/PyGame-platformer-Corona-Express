import sys
import pygame
from os import listdir
from os import path
import time
import json


class Menu:
    def __init__(self,screen):
        self.screen = screen
        self.init_options()
        self.init_objects()

    def init_options(self):
        self.clk = pygame.time.Clock()
        self.clicked = False
        self.end_loop = False
        self.load_bool = False
        self.load_gui = False
        self.save_gui = False
        self.save_socket= -1
        self.in_game = False
        self.NPCset_path = ""
        self.mouseRect = pygame.Rect(1, 1, 5, 5)
        self.fps = 30
        self.choice = 0
        self.delay = 10
        self.escape_wait = 0
        self.saves = listdir("Saves/")
        self.path = ""
    def init_objects(self):
        self.cursor_sound = pygame.mixer.Sound('Soundtrack/cursor.ogg')
        self.load_sound = pygame.mixer.Sound('Soundtrack/load.ogg')
        self.title = pygame.image.load("GUI/Menu/Title.png")
        self.title_block = pygame.Rect(427, 289, 714, 127)
        self.save = pygame.image.load("GUI/Menu/Save.png")
        self.save_block = pygame.Rect(610,650,438,100)
        self.cursor = pygame.image.load("GUI/Menu/Cursor.png")
        self.cursor_block = pygame.Rect(508,434,438,100)
        self.exit = pygame.image.load("GUI/Menu/Exit.png")
        self.exit_block = pygame.Rect(638,634,438,100)
        self.continu = pygame.image.load('GUI/Menu/Continue.png')
        self.continu_block = pygame.Rect(605,434,438,100)
        self.new_game = pygame.image.load("GUI/Menu/NowaGra.png")
        self.new_game_block = pygame.Rect(605,434,438,100)
        self.loading = pygame.image.load("GUI/Menu/Loading.png")
        self.loading_block = pygame.Rect(1100,700,2,2)
        self.load = pygame.image.load("GUI/Menu/Load.png")
        self.load_block = pygame.Rect(608, 548, 438, 100)
        self.background = pygame.image.load("GUI/background.png").convert_alpha()
        self.background_block = pygame.Rect(0, 0, 1600, 900)
        self.rectangle = pygame.Surface((300,440)).convert_alpha()
        self.rectangle.fill((0, 0, 0,180))
        self.rectangle_block = pygame.Rect(590,424,300,420)
        self.rectangle2 = pygame.Surface((760, 140)).convert_alpha()
        self.rectangle2.fill((0, 0, 0, 180))
        self.rectangle2_block = pygame.Rect(400,284,700,140)
        self.Font = pygame.font.SysFont("Calibri",36,bold = True,italic=True)
        self.Font2 = pygame.font.SysFont("Calibri",56,bold = True,italic=True)
        self.text_block = pygame.Rect(595,500,438,100)
    def move_cursor(self):
        if (pygame.key.get_pressed()[pygame.K_s] or pygame.key.get_pressed()[pygame.K_DOWN]) and self.delay >=5:
            if self.load_gui == True: #Operating on saves window
                if self.choice < len(self.saves):
                    self.cursor_sound.play()
                    self.choice += 1
                    self.cursor_block = self.cursor_block.move(0,100)
                    self.setup_delay()
            elif self.save_gui == True:
                if self.choice < 3:
                    self.cursor_sound.play()
                    self.choice += 1
                    self.cursor_block = self.cursor_block.move(0,100)
                    self.setup_delay()
            else:
                if self.choice < 2 or (self.choice < 3 and self.in_game == True): #  NOW we are on MAIN MENU
                    self.cursor_sound.play()
                    self.choice += 1
                    self.cursor_block = self.cursor_block.move(0,100)
                    self.setup_delay()
        elif (pygame.key.get_pressed()[pygame.K_w] or pygame.key.get_pressed()[pygame.K_UP]) and self.delay >= 5:
            if self.choice > 0:
                self.cursor_sound.play()
                self.choice -= 1
                self.cursor_block = self.cursor_block.move((0,-100))
                self.setup_delay()
        elif pygame.key.get_pressed()[pygame.K_RETURN] and self.delay >=5: #Pressing ENTER event
            if self.load_gui == True:           #inside load game event
                if self.choice == len(self.saves): #EXIT load window
                    self.cursor_block.y = 434
                    self.load_gui = False
                    self.setup_delay()
                else:                              #LOAD GAME
                    path = self.saves[self.choice]
                    self.load_sound.play()
                    self.load_bool = True
                    self.choice = 0
                    self.cursor_block.y = 434
                    self.path = "Saves/" + path
                    self.load_gui = False
                    self.end_loop = True
            elif self.save_gui == True:     #inside save game event
                if self.choice == 3:        #EXIT save window
                    self.cursor_block.y = 434
                    self.save_gui = False
                    self.setup_delay()
                elif self.delay >= 5:                              #SAVE GAME
                    #self.saves[self.choice]     #for save text modification
                    self.load_sound.play()
                    self.save_socket = self.choice
                    self.setup_delay()
            else:                                   #  NOW we are on MAIN MENU
                self.cursor_block.y = 434
                if self.choice == 2:                #EXIT or open SAVE GAME
                    if self.in_game == True:
                        self.save_gui = True
                        self.setup_delay()
                    else:
                       sys.exit(0)
                elif self.choice == 1 and self.saves != None: #OPEN load window
                    self.load_sound.play()
                    self.setup_delay()
                    self.cursor_block.y = 434
                    self.choice = 0
                    self.load_gui = True
                elif self.choice == 0:                          #NEW GAME
                    self.load_sound.play()
                    self.end_loop = True
                elif self.choice == 3:          #EXIT whilst in in_game mode
                    sys.exit(0)
            if self.save_socket == -1:
                self.choice = 0

        if self.delay < 5:               #DELAY clock
            self.delay+= 1
    def setup_delay(self):
        self.delay = 0
    def start(self,in_game=False,level=None,dest=None,timer=None,money=None,points=None,upgrades=None):
        self.in_game = in_game
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)
            if pygame.key.get_pressed()[pygame.K_ESCAPE]:
                if in_game == True:
                    self.escape_wait +=1
                    if self.escape_wait >= 6:
                        self.escape_wait = 0
                        break
                else:
                    sys.exit(0)
            self.screen.fill((0,0,0))
            self.move_cursor()
            if self.save_socket != -1:
                self.save_game(level,dest,timer,money,points,upgrades)
                self.draw()
                pygame.display.flip()
                self.saves = listdir("Saves/")
                self.save_socket = -1
            self.draw()
            pygame.display.flip()
            if self.end_loop == True:
                self.screen.fill((0,0,0))
                break
            self.clk.tick(self.fps)

    def draw(self):
        #init text for save and load mode
        text_list = []
        for i in range(0,len(self.saves)):
            local_time = time.ctime(path.getmtime("Saves/" + self.saves[i]))[:19]
            text_list.append(self.Font.render(local_time, True, (255, 255, 255)))
        text2 = self.Font.render('Puste miejsce',True,(255,255,255))

        if self.load_gui == True:
            self.screen.blit(self.background, self.background_block)
            self.screen.blit(self.rectangle, self.rectangle_block)
            self.screen.blit(self.rectangle2, self.rectangle2_block)
            self.screen.blit(self.cursor, self.cursor_block)
            for i in range(0, len(self.saves)):
                self.screen.blit(text_list[i],self.text_block)
                self.text_block = self.text_block.move(0, 100)
            self.screen.blit(self.title, self.title_block)
            self.screen.blit(self.Font2.render("Cofnij", True, (255, 255, 255)),
                             pygame.Rect(662, 464 + len(self.saves) * 100, 438, 100))
            self.text_block.y = 464
        elif self.save_gui == True:
            self.screen.blit(self.background, self.background_block)
            self.screen.blit(self.rectangle, self.rectangle_block)
            self.screen.blit(self.rectangle2, self.rectangle2_block)
            self.screen.blit(self.cursor, self.cursor_block)
            for i in range(0, 3):
                if i < len(self.saves):
                    self.screen.blit(text_list[i],self.text_block)
                else:
                    self.screen.blit(text2,self.text_block)
                self.screen.blit(self.Font2.render("Cofnij", True, (255, 255, 255)),pygame.Rect(662, 464 + 3 * 100, 438, 100))
                self.screen.blit(self.title, self.title_block)
                self.text_block = self.text_block.move(0, 100)
            self.text_block.y = 464
        elif self.end_loop:
            self.screen.blit(self.background, self.background_block)
            self.screen.blit(self.loading,self.loading_block)

        else:
            self.screen.blit(self.background,self.background_block)
            self.screen.blit(self.rectangle, self.rectangle_block)
            self.screen.blit(self.rectangle2, self.rectangle2_block)
            self.screen.blit(self.title,self.title_block)
            if self.in_game == False:
                self.screen.blit(self.new_game,self.new_game_block)
            else:
                self.screen.blit(self.continu,self.continu_block)
                self.screen.blit(self.save,self.save_block)
                self.exit_block.y = 734

            self.screen.blit(self.exit,self.exit_block)
            self.screen.blit(self.load, self.load_block)
            self.screen.blit(self.cursor,self.cursor_block)

    #NPC_groups contains a list of lists such as NPC_groupA,NPC_groupB...
    def save_game(self,lvl,dest,timer,money,points,upgrades,local=False):
        NPC_set = self.NPCset_path
        data = {"Level":lvl,"NPC_set":NPC_set,"Destinations":dest,"Timer":timer,"Money":money,"Points":points,"Skills":upgrades}
        if local == True:
            with open('Local/autosave.json', 'w') as outfile:
                json.dump(data, outfile)
        else:
            with open('Saves/save' + str(self.save_socket) + ".json", 'w') as outfile:
                json.dump(data, outfile)

        self.saves = listdir('Saves/')