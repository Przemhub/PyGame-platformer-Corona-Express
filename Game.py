import json
from os import listdir
from random import Random

import pygame
import sys


from CollisionSprites import SpriteCollider
from Box import Box
from Buffs import BuffContainer
from Character import Deliverer
import Worlds
from Animal import Animal
from Menu import Menu
from Logic import Logic
from NPC import NPC
from NPCGroups import Groups
from Interface import Interface
import Cinematic
from Shop import Shop


class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        pygame.display.init()
        self.initOptions()
        pygame.mixer.music.load('Soundtrack/menu.mp3')
        pygame.mixer.music.play(True)
        self.menu = Menu(self.screen)
        self.menu.start()
        self.initObjects()
        pygame.mixer.music.load('Soundtrack/in-game.mp3')
        pygame.mixer.music.play(True)
        if self.menu.load_bool == True:
            self.init_level(new=True)
            self.load_game()
            self.shuffle_NPCs(self.menu.NPCset_path)
            self.intro.scene1 = False
            self.intro.scene_semaphore = -1
        else:
            self.init_level(new=True)
            self.load_game(new = True)
            self.shuffle_NPCs(fName='map1.json')
        self.start()

    def initObjects(self):

        # Player and player animation
        self.player = Deliverer(self.screen)
        self.action = [self.player.stay_front, self.player.walk_front, self.player.stay_right,
                          self.player.stay_left,self.player.walk_right, self.player.walk_left,\
                          self.player.stay_back, self.player.walk_back]

        self.move_i = 0
        self.stay_i=0
        # Worlds
        self.world = Worlds.City(self.screen, self.player)
        #self.locations = [self.world.north1,self.world.north2, self.world.center1,self.world.center2,self.world.south1,self.world.south2,self.world.middle_road1, self.world.middle_road2]
        self.locations_blocks = [self.world.north1_block,self.world.north2_block,self.world.center1_block,self.world.center2_block,
                                 self.world.south1_block ,self.world.south2_block,self.world.middle_road1_block, self.world.middle_road2_block]
        #self.locations_collisions = [self.world.south1_collisions ,self.world.middle_road1_collisions, self.world.middle_road2_collisions, self.world.north1_collisions,self.world.north2_collisions,self.world.center1_collisions,self.world.center2_collisions,self.world.south2_collisions]
        # NPCs
        self.NPC_group = Groups(self.world.north1_block)
        self.location_NPC = {"north1":self.NPC_group.NPC_groupE, "north2":self.NPC_group.NPC_groupF, "south1":self.NPC_group.NPC_groupG,
                             "south2":self.NPC_group.NPC_groupH,"center1":self.NPC_group.NPC_groupK,"center2":self.NPC_group.NPC_groupJ}

        # Collision Sprites
        self.collider = SpriteCollider(self.screen)

        # Logic
        self.logic = Logic(self.world.north1_block)

        # Interface
        self.interface = Interface()

        # Shop
        self.shop = Shop(self.screen)

        # Buffs
        self.buff_container = BuffContainer(self.world.north1_block)

        # Bullet
        self.bullet = Box(self.world.north1_block)

        # Cinematics
        self.intro = Cinematic.Intro(self.player,self.world.change_maps_positions,self.NPC_group.move_all,self.logic.change_random_places_positions,self.buff_container.move_buffs,self.collider.update_maps)

        #upgrade dictionary
        self.upgrades = {"SpeedUp": self.buff_container.buff_to_time["SpeedUp"],
                         "Invincible": self.buff_container.buff_to_time["Invincible"],
                         "StopTime": self.buff_container.buff_to_time["StopTime"], "Untouchable": 2.5, "Speed": 17,
                         "Lives": 3, "Money": 0, "Buffs": 3}

        # Sounds
        self.hit_sound = pygame.mixer.Sound('Soundtrack/blow.ogg')
        self.paper_sound = pygame.mixer.Sound("Soundtrack/paper.ogg")
        self.menu_sound = pygame.mixer.Sound('Soundtrack/load.ogg')
        self.speedUp_sound = pygame.mixer.Sound('Soundtrack/speedUp.ogg')
        self.boxGun_sound = pygame.mixer.Sound('Soundtrack/boxGun.ogg')
        self.healthUp_sound = pygame.mixer.Sound('Soundtrack/healthUp.ogg')
        self.stopTime_sound = pygame.mixer.Sound('Soundtrack/stopTime.ogg')
        self.invincible_sound = pygame.mixer.Sound('Soundtrack/invincible.ogg')
        self.throw_sound = pygame.mixer.Sound('Soundtrack/throw.ogg')
        self.score_sound = pygame.mixer.Sound('Soundtrack/score.ogg')
        self.caching_sound = pygame.mixer.Sound('Soundtrack/caching.ogg')
        self.applause_sound = pygame.mixer.Sound('Soundtrack/applause.ogg')
        self.tadaa_sound = pygame.mixer.Sound('Soundtrack/tadaa.ogg')

    def static_anim(self):
        if self.world.static_anim_id == 0:
            self.screen.blit(self.world.anim_static(), self.world.fount_block)
        else:
            self.screen.blit(self.world.anim_static(), self.world.caruzel_block)

    def initOptions(self):
        #Variables
        self.player_blocked = False
        self.clicked = False
        self.fps = 30
        self.screen = pygame.display.set_mode((1600,900),pygame.FULLSCREEN)
        self.clk = pygame.time.Clock()
        self.level = 1
        self.timer_save = 0
        self.stop_NPCs = False
        self.display_options = False

    def draw(self):
        #Setting character movement animation based on previous character position
        self.movement = self.action[
                self.move_i]()
        #if self.player.block.colliderect(self.):
         #S   pass

        #Basics
        #Layer1
        self.screen.blit(self.world.north1,self.world.north1_block)
        self.screen.blit(self.world.north2, self.world.north2_block)
        self.screen.blit(self.world.center1,self.world.center1_block)
        self.screen.blit(self.world.center2,self.world.center2_block)
        self.screen.blit(self.world.middle_road1, self.world.middle_road1_block)
        self.screen.blit(self.world.middle_road2,self.world.middle_road2_block)
        self.screen.blit(self.world.south1,self.world.south1_block)
        self.screen.blit(self.world.south2,self.world.south2_block)
        for place in self.logic.random_places_save:
            index = self.logic.places_hash.get(place.width)
            self.screen.blit(self.logic.NPCs_hash.get(index)[self.logic.sprite_list[index]], place)

        #Buffs
        for buff in self.buff_container.buff_list:
            self.screen.blit(buff.image,buff.block)
        #Player
        self.screen.blit(self.movement, (self.player.block.x - 15, self.player.block.y - 10))


        # NPCs and Animals
        for npc in self.NPC_group.NPC_list:
            self.screen.blit(npc.movement,pygame.Rect(npc.block.x-17,npc.block.y-5,npc.block.width,npc.block.height))
            npc.movement = npc.action[npc.move_i]()
        #Layer2
        self.screen.blit(self.world.north1_objects, self.world.north1_block)
        self.screen.blit(self.world.north2_objects, self.world.north2_block)
        self.screen.blit(self.world.center1_objects, self.world.center1_block)
        self.screen.blit(self.world.center2_objects, self.world.center2_block)
        self.screen.blit(self.world.middle_road1_objects, self.world.middle_road1_block)
        self.screen.blit(self.world.middle_road2_objects, self.world.middle_road2_block)
        self.screen.blit(self.world.south1_objects, self.world.south1_block)
        self.screen.blit(self.world.south2_objects, self.world.south2_block)

        #Static anim
        self.static_anim()
        if self.bullet.is_active() == True:
            self.screen.blit(self.bullet.image,self.bullet.block)
        #Finish flag
        if self.logic.almost_finished():
            self.screen.blit(self.logic.finish_anim(),self.logic.finish_block)
        #Interface
        ##Lives
        for i in range(0,self.player.lives):
            self.screen.blit(self.interface.Life,pygame.Rect(self.interface.Life_block.x + i * 100,self.interface.Life_block.y,self.interface.Life.get_width(),self.interface.Life.get_height()))
        ##Paper
        self.screen.blit(self.interface.Paper,self.interface.Paper_block)
        if self.logic.almost_finished(): #display post office on Paper
            self.screen.blit(self.interface.location_list[7],pygame.Rect(self.interface.locations_block.x - 10,self.interface.locations_block.y + 50,1,1))
        else:
            for i in range(0,len(self.interface.chosen_list)): #On the paper surface draws locations also crosses out with red line locations already delivered
                if i % 2 == 0:
                    self.screen.blit(self.interface.chosen_list[i],pygame.Rect(self.interface.locations_block.x,self.interface.locations_block.y + i * 90,10,10))
                    cross_out = True
                    for rand_place in self.logic.random_places:#search through list of delivery locations and check which ones are removed, then draw red line  on their paper objects representations
                        if self.logic.places_hash.get(rand_place.width) == self.interface.locations_hash.get(self.interface.chosen_list[i].get_height()):
                            cross_out = False
                    if cross_out == True:
                        pygame.draw.line(self.screen, (255, 0, 0), \
                                         (self.interface.locations_block.x, self.interface.locations_block.y + i * 90), \
                                         (self.interface.locations_block.x + self.interface.chosen_list[i].get_width(),
                                          self.interface.locations_block.y + self.interface.chosen_list[
                                              i].get_height() + i * 90), 3)

                else:
                    self.screen.blit(self.interface.chosen_list[i], pygame.Rect(self.interface.locations_block.x + 90,self.interface.locations_block.y + i * 90,10,10))
                    cross_out = True
                    for rand_place in self.logic.random_places:
                        if self.logic.places_hash.get(rand_place.width) == self.interface.locations_hash.get(self.interface.chosen_list[i].get_height()):
                            cross_out = False
                    if cross_out == True:
                        pygame.draw.line(self.screen, (255, 0, 0), \
                                         (self.interface.locations_block.x + 90, self.interface.locations_block.y + i * 90), \
                                         (self.interface.locations_block.x + self.interface.chosen_list[i].get_width() + 90,
                                          self.interface.locations_block.y + self.interface.chosen_list[i].get_height() + i * 90),3)
        #Timer
        if self.logic.timer_start == True:
            self.screen.blit(self.interface.timer_background,pygame.Rect(685,55,10,10))
            self.screen.blit(self.interface.timer_text,pygame.Rect(700,60,10,10))
        #Text blocks
        if self.intro.text_flag == True:
            self.screen.blit(self.intro.window, (30, 640))
            self.screen.blit(self.intro.text,self.intro.dialogue)
            self.intro.dialogue = self.intro.dialogue.move(0,50)
            self.screen.blit(self.intro.text2,self.intro.dialogue)
            self.intro.dialogue = self.intro.dialogue.move(0,50)
            self.screen.blit(self.intro.text3,self.intro.dialogue)
            self.intro.dialogue = self.intro.dialogue.move(0,50)
            self.screen.blit(self.intro.text4,self.intro.dialogue)
            self.intro.dialogue = self.intro.dialogue.move(0,-150)
        #Cinematics - draws circles around paper objects and position on map
        if self.intro.scene1 == True:
            if self.intro.scene_semaphore == 4:
                pygame.draw.circle(self.screen,(255,0,0,),(self.interface.locations_block.x + 30,self.interface.locations_block.y + 30),30,4)
                pygame.draw.circle(self.screen, (255, 0, 0,),(708,380), 60, 4)
            elif self.intro.scene_semaphore == 6:
                pygame.draw.circle(self.screen, (255, 0, 0,),(self.interface.locations_block.x + 30, self.interface.locations_block.y + 250), 50,4)
                pygame.draw.circle(self.screen, (255, 0, 0,), (1070, 200), 150, 6)
            elif self.intro.scene_semaphore == 9:
                pygame.draw.circle(self.screen, (255, 0, 0,), (self.interface.locations_block.x + 120, self.interface.locations_block.y + 120), 40, 4)
                pygame.draw.circle(self.screen, (255, 0, 0,), (950, 140), 100, 4)
        elif self.intro.scene2 == True:
            if self.intro.scene_semaphore == 2:
                pygame.draw.circle(self.screen, (255, 0, 0,),(self.interface.locations_block.x + 30, self.interface.locations_block.y + 40), 50, 4)
            elif self.intro.scene_semaphore == 4:
                pygame.draw.circle(self.screen, (255, 0, 0,),(self.interface.locations_block.x + 120, self.interface.locations_block.y + 120), 50,4)

            elif self.intro.scene_semaphore == 6:
                pygame.draw.circle(self.screen, (255, 0, 0,), (self.interface.locations_block.x + 30, self.interface.locations_block.y + 230), 40, 4)
                pygame.draw.circle(self.screen, (255, 0, 0,), (610, 250), 60, 6)

    def draw_finish(self):
        self.screen.blit(self.interface.Paper_finish,self.interface.Paper_finish_block)
        self.screen.blit(self.interface.congratz_text,self.interface.congratz_block)
        self.screen.blit(self.interface.points_text,self.interface.points_block)
        self.screen.blit(self.interface.money_text,self.interface.money_block)
        if self.display_options == True:
            self.interface.Options.blit(self.interface.continue_text,self.interface.continue_block)
            self.interface.Options.blit(self.interface.shop_text,self.interface.shop_block)
            self.screen.blit(self.interface.Options,self.interface.Options_block)
            self.screen.blit(self.interface.cursor,self.interface.cursor_block)

    def start(self):
        while True:

            for event in pygame.event.get():
                if event.type == pygame.USEREVENT:
                    if self.logic.timer_start == True:
                        self.logic.timer -= 1
                        self.interface.set_timer_text(self.logic.timer)
                if event.type == pygame.QUIT:
                    sys.exit(0)

            self.screen.fill((85,159,53))

            #Movement and animation
            if self.stop_NPCs == False:
                self.NPC_group.commands()
            self.interface.animate_paper()
            if self.intro.scene_semaphore == -1:
                self.move()

            #Logic stuff
            if self.level == 1:
                self.intro.init_scene1(self.interface.fade_paper)
            elif self.level == 2:
                paper_hidden = False
                if self.interface.Paper_block.x > 1600:
                    paper_hidden = True
                self.intro.init_scene2(self.interface.fade_paper,paper_hidden)
            elif self.level == 3:
                self.intro.init_scene3(self.logic.set_timer)
            if self.logic.level_finished:
                if self.level % 2 == 0 and self.level > 3 and self.level < 12:
                    self.timer_save -= 10
                elif self.level >=10 and self.level % 2 == 0:
                    self.timer_save -= 20
                self.player.money += self.logic.get_salary(self.level)
                self.interface.update_texts(self.player.points,self.player.money)
                pygame.mixer.music.pause()
                pygame.time.delay(1000)
                self.finish_event()
                self.level += 1
                pygame.mixer.music.load('Soundtrack/victory.mp3')
                pygame.mixer.music.play(False)
                self.intro.fade_cinematic(self.level,self.screen)
                pygame.mixer.music.pause()
                self.init_level()
                self.shuffle_NPCs()
                pygame.mixer.music.load('Soundtrack/in-game.mp3')
                pygame.mixer.music.play(True)
                self.logic.level_finished = False
            if self.player.lives == 0 or (self.logic.timer <= 0 and self.logic.timer_start == True):                  #game over
                pygame.mixer.music.load('Soundtrack/game-over.mp3')
                pygame.mixer.music.play(True)
                self.game_over()
            if self.intro.scene_semaphore == -1:
                self.logic.check_list(self.player.block) #check on evey destination whether player delivered package
                self.player_collided_buff()
                self.play_buff_effect()

            #Drawing
            self.draw()
            pygame.display.flip()
            self.clk.tick(self.fps)

    def finish_event(self):
        pts = self.logic.get_pts_per_sec(self.level)
        n = 0
        m = 0
        option = 0
        delay = 0
        self.paper_sound.play()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.K_KP_ENTER:
                    pass
                if event.type == pygame.QUIT:
                    sys.exit(0)
            self.screen.fill((255,255,255))
            if self.display_options == True:
                self.draw()
                self.draw_finish()
                event = pygame.key.get_pressed()
                if event[pygame.K_s] or event[pygame.K_DOWN]:
                    if option == 0:
                        self.menu.cursor_sound.play()
                        self.interface.cursor_block = self.interface.cursor_block.move(0,60)
                        option = 1
                elif event[pygame.K_w] or event[pygame.K_UP]:
                    if option == 1:
                        self.menu.cursor_sound.play()
                        self.interface.cursor_block = self.interface.cursor_block.move(0,-60)
                        option = 0
                elif event[pygame.K_RETURN]:
                    if option == 0:
                        self.display_options = False
                        break
                    else:
                        pygame.mixer.music.stop()
                        self.interface.cursor_block = self.interface.cursor_block.move(0,-60)
                        option = 0
                        self.upgrades["Money"] = self.player.money
                        self.upgrades = self.shop.start(self.player.money,self.upgrades)
                        pygame.time.delay(100)
                        self.asign_upgrades(self.upgrades)
                        pygame.mixer.music.load("Soundtrack/in-game.mp3")
                        pygame.mixer.music.play()

                pygame.display.flip()
                self.clk.tick(self.fps)
                continue
            if self.logic.timer > 0:
                self.logic.timer -= 1
                self.player.points += pts
                m += pts
                pygame.time.delay(50)
                if n % 10 == 0:
                    self.player.points += 50
                    m+= 50
                if m > 200:
                    self.player.money += 20
                    self.caching_sound.play()
                    m-= 200
                self.interface.set_timer_text(self.logic.timer)
                self.interface.update_texts(self.player.points,self.player.money)
            self.draw()
            self.draw_finish()
            n += 1
            pygame.display.flip()
            if self.logic.timer <= 0:
                self.score_sound.stop()
                self.tadaa_sound.play()
                pygame.time.delay(2500)
                self.display_options = True
                self.menu.cursor_sound.play()
            if n == 1 and self.display_options == False:
                pygame.time.delay(1200)
                self.score_sound.play(loops=True)
            self.clk.tick(self.fps)
    def asign_upgrades(self,upgrades):
        self.player.money = upgrades["Money"]
        self.player.player_speed = upgrades["Speed"]
        self.player.invincible_time = upgrades["Untouchable"]
        self.player.const_lives = upgrades["Lives"]
        self.buff_container.buff_count = upgrades["Buffs"]
        self.buff_container.set_buff_time("SpeedUp",upgrades["SpeedUp"])
        self.buff_container.set_buff_time("Invincible", upgrades["Invincible"])
        self.buff_container.set_buff_time("StopTime", upgrades["StopTime"])

        # initialize whole level: set destination locations, switch locations, change NPC_groups, reset Timer,setup interface
    def init_level(self,new = False):

        if new == True:
            places_list = [2,4,3]
            self.logic.set_random_places_manually(2,4,3)
        else:
            # In case buff still plays when player finishes game, deactivate all buffs
            self.buff_container.deactivate_buffs()
            self.play_buff_effect()
            self.buff_container.clear_list()
            self.buff_container.init_buff_list()
            self.world = Worlds.City(self.screen, self.player)
            self.collider = SpriteCollider(self.screen)
            self.player.block = pygame.Rect(self.screen.get_width() / 3 + 30, self.screen.get_height() / 2 - 40, 40,140)
            self.collider.character.rect = pygame.Rect(self.screen.get_width() / 3 + 15, self.screen.get_height() / 2 - 45, 40, 140)
            self.player.lives = self.player.const_lives
            self.NPC_group = Groups(self.world.north1_block)
            self.location_NPC = {"north1": self.NPC_group.NPC_groupE, "north2": self.NPC_group.NPC_groupF,
                                 "south1": self.NPC_group.NPC_groupG,
                                 "south2": self.NPC_group.NPC_groupH, "center1": self.NPC_group.NPC_groupK,
                                 "center2": self.NPC_group.NPC_groupJ}
            self.logic = Logic(self.world.north1_block)
            places_list = self.logic.set_random_places()
            #reset methods in Cinematic for move_camera
            self.intro.change_maps_positions = self.world.change_maps_positions
            self.intro.change_random_places_position = self.logic.change_random_places_positions
            self.intro.move_all_NPC = self.NPC_group.move_all
            self.intro.update_maps = self.collider.update_maps
            if self.level == 2:
                places_list = [1,6,0]
                self.logic.set_random_places_manually(1, 6, 0)
                self.intro.scene2 = True
            if self.level >= 3:
                if self.level == 3:
                    self.timer_save = 180
                    self.intro.scene3 = True
                self.logic.set_timer(self.timer_save)
        self.player.lives = self.player.const_lives
        self.player.ammo = 0
        self.interface.set_Paper(places_list)



    def move(self):
        #SECTION 0 in_game menu event handling
        if pygame.key.get_pressed()[pygame.K_ESCAPE]:       #open In game MENU
            self.menu_sound.play()
            pygame.mixer.music.pause()
            self.menu.end_loop = False
            dest = [self.logic.places_hash.get(self.logic.random_places_save[0].width),
                    self.logic.places_hash.get(self.logic.random_places_save[1].width),
                    self.logic.places_hash.get(self.logic.random_places_save[2].width)]
            self.menu.start(in_game=True,level=self.level,dest=dest,timer=self.logic.timer,money=self.player.money,points=self.player.points,upgrades=self.upgrades)
            if self.menu.load_bool == True:             #If user loaded save in LOAD MENU
                self.intro.scene_semaphore = -1
                self.player.block.x = self.screen.get_width() / 3 + 30
                self.player.block.y = self.screen.get_height() / 2 - 40
                self.init_level()
                self.load_game()
                self.shuffle_NPCs(self.menu.NPCset_path)
                self.intro.scene1 = False
                self.menu.load_bool = False
            pygame.mixer.music.play(True)
        #SECTION 1 Character stand position
        self.move_i = self.stay_i

        #SECTION 2 Character/world positioning
        if pygame.key.get_pressed()[pygame.K_d]:
            self.move_i = 4
            self.stay_i = 2
            if self.can_move_frame("right"):
                self.world.change_maps_positions(-self.player.player_speed,0)
                self.logic.change_random_places_positions(-self.player.player_speed,0)
                self.NPC_group.move_all(-self.player.player_speed, 0)
                self.buff_container.move_buffs(-self.player.player_speed, 0)
                self.collider.update_maps(-self.player.player_speed,0)
            else:
                self.player.relocate(1,0)
                self.collider.update_character(1,0,self.player.player_speed)
        elif pygame.key.get_pressed()[pygame.K_a]:
            self.move_i = 5
            self.stay_i = 3
            if self.can_move_frame("left"):
                self.world.change_maps_positions(self.player.player_speed, 0)
                self.logic.change_random_places_positions(self.player.player_speed, 0)
                self.NPC_group.move_all(self.player.player_speed, 0)
                self.buff_container.move_buffs(self.player.player_speed, 0)
                self.collider.update_maps(self.player.player_speed,0)
            else:
                self.player.relocate(-1, 0)
                self.collider.update_character(-1,0,self.player.player_speed)
        elif pygame.key.get_pressed()[pygame.K_s]:
            self.move_i = 1
            self.stay_i = 0
            if self.can_move_frame("down"):
                self.world.change_maps_positions(0, -self.player.player_speed)
                self.logic.change_random_places_positions(0, -self.player.player_speed)
                self.NPC_group.move_all(0,-self.player.player_speed)
                self.buff_container.move_buffs(0, -self.player.player_speed)
                self.collider.update_maps(0,-self.player.player_speed)
            else:
                self.player.relocate(0, 1)
                self.collider.update_character(0,1,self.player.player_speed)
        elif pygame.key.get_pressed()[pygame.K_w]:
            self.move_i = 7
            self.stay_i = 6
            if self.can_move_frame("up"):
                self.world.change_maps_positions(0, self.player.player_speed)
                self.logic.change_random_places_positions(0, self.player.player_speed)
                self.NPC_group.move_all(0, self.player.player_speed)
                self.buff_container.move_buffs(0, self.player.player_speed)
                self.collider.update_maps(0,self.player.player_speed)
            else:
                self.player.relocate(0 , -1)
                self.collider.update_character(0,-1,self.player.player_speed)
        elif pygame.key.get_pressed()[pygame.K_TAB]:
            self.paper_sound.play()
            self.interface.fade_paper()

        #SECTION 3 player collisions
        if (self.player_out_of_range() or self.player_collided()):
            if self.move_i == 4:
                self.player.relocate(-1,0)
                self.collider.update_character(-1,0, self.player.player_speed)
            elif self.move_i == 5:
                self.player.relocate(1,0)
                self.collider.update_character(1,0, self.player.player_speed)
            elif self.move_i == 1:
                self.player.relocate(0,-1)
                self.collider.update_character(0, -1, self.player.player_speed)
            elif self.move_i == 7:
                self.player.relocate(0,1)
                self.collider.update_character(0, 1, self.player.player_speed)
        if self.player.is_invincable() == False:
            if self.player_collided_NPC():
                self.player.take_life()
                self.hit_sound.play()
                self.player.start_time = pygame.time.get_ticks()
        else:
            self.player.hit_animation()
        #SECTION 4 shooting BoxGun
        if pygame.key.get_pressed()[pygame.K_SPACE]:
            if self.bullet.is_active() == False:
                self.bullet.reset()
                if self.player.ammo > 0:
                    self.throw_sound.play()
                    self.bullet.block = pygame.Rect(self.player.block)
                    self.player.ammo -= 1
                    self.bullet.make_wait()
                    if self.move_i == 4 or self.move_i == 2:
                        self.bullet.direction = 2
                    elif self.move_i == 5 or self.move_i == 3:
                        self.bullet.direction = 0
                    elif self.move_i == 1 or self.move_i == 0:
                        self.bullet.direction = 3
                    elif self.move_i == 7 or self.move_i == 6:
                        self.bullet.direction = 1

        if self.bullet.is_active() == True:
            dir = self.bullet.get_direction()
            self.bullet.shoot(dir)
            if self.bullet_collided_NPC() == True:
                self.hit_sound.play()
                self.bullet.reset()



    def can_move_frame(self, axis):
        if axis == "up":
            if self.player.block.y <= self.screen.get_height()/2 - 80and self.world.north1_block.y < 0:
                return True
        if axis == "down":
            if self.player.block.y >= self.screen.get_height()/2  and self.world.south1_block.y + self.world.south1.get_height() > self.screen.get_height():
                return True
        if axis == "right":
            if self.player.block.x >= self.screen.get_width()/2 + 60 and self.world.north2_block.x + self.world.north2.get_width() > self.screen.get_width():
                return True
        if axis == "left":
            if self.player.block.x <= self.screen.get_width()/2 - 60 and self.world.north1_block.x < 0:
                return True
        return False

    def player_out_of_range(self):
        if self.player.block.left <=  self.world.north1_block.x:
            return True
        if self.player.block.right >= self.world.north2_block.x + self.world.north2.get_width():
            return True
        if self.player.block.bottom >= self.world.south1_block.y + self.world.south1.get_height():
            return True
        if self.player.block.top <= self.world.north1_block.y :
            return True
        return False

    def bullet_collided_NPC(self):
        self.locations_blocks = [self.world.north1_block, self.world.north2_block, self.world.center1_block,
                                 self.world.center2_block,
                                 self.world.south1_block, self.world.south2_block, self.world.middle_road1_block,
                                 self.world.middle_road2_block]
        for block in self.locations_blocks:  # seaches through location list
            if self.player.block.colliderect(block):
                npc_group = self.location_NPC.get(self.world.get_string(
                    block))  # searches through dict for an NPC group equivalent of character's current location
                if npc_group == None:  # 1 item doesnt appear in list, it is middle_road1(has 4 npc_groups)
                    for npc in self.NPC_group.NPC_groupA:  # search every npc from npc_group
                        if self.bullet.block.colliderect(npc.block):
                            npc.block  = npc.block.move(-6000,0)
                            self.NPC_group.NPC_list.remove(npc)
                            return True
                    for npc in self.NPC_group.NPC_groupB:
                        if self.bullet.block.colliderect(npc.block):
                            npc.block = npc.block.move(-6000, 0)
                            self.NPC_group.NPC_list.remove(npc)
                            return True
                    for npc in self.NPC_group.NPC_groupC:
                        if self.bullet.block.colliderect(npc.block):
                            npc.block = npc.block.move(-6000, 0)
                            self.NPC_group.NPC_list.remove(npc)
                            return True
                    for npc in self.NPC_group.NPC_groupD:  # search every npc from npc_group
                        if self.bullet.block.colliderect(npc.block):
                            npc.block = npc.block.move(-6000, 0)
                            self.NPC_group.NPC_list.remove(npc)
                            return True
                    for npc in self.NPC_group.NPC_groupI:
                        if self.bullet.block.colliderect(npc.block):
                            npc.block = npc.block.move(-6000, 0)
                            self.NPC_group.NPC_list.remove(npc)
                            return True
                else:
                    for npc in npc_group:
                        if self.bullet.block.colliderect(npc.block):
                            npc.block = npc.block.move(-6000, 0)
                            self.NPC_group.NPC_list.remove(npc)
                            return True
        return False

    def player_collided_buff(self):
        for buff in self.buff_container.buff_list:
            if buff.picked == False: #Checks if player hasnt already picked that buff
                if self.player.block.colliderect(buff.block):
                    buff.block = buff.block.move(-6000,0)
                    buff.picked = True
                    buff.activate()
                    if buff.name == "SpeedUp":
                        self.player.player_speed += 5
                        self.speedUp_sound.play()
                    elif buff.name == "Invincible":
                        self.player.start_time = pygame.time.get_ticks()
                        self.invincible_sound.play()
                    elif buff.name == "StopTime":
                        self.stop_NPCs = True
                        self.logic.stop_timer()
                        self.stopTime_sound.play()
                    elif buff.name == "HealthUp":
                        self.player.lives += 1
                        self.healthUp_sound.play()
                    elif buff.name == "BoxGun":
                        self.player.ammo += 1
                        self.boxGun_sound.play()


    def player_collided_NPC(self):
        self.locations_blocks = [self.world.north1_block, self.world.north2_block, self.world.center1_block,self.world.center2_block,
                                 self.world.south1_block, self.world.south2_block, self.world.middle_road1_block,self.world.middle_road2_block]
        for block in self.locations_blocks:                                     #seaches through location list
            if self.player.block.colliderect(block):
                npc_group = self.location_NPC.get(self.world.get_string(block)) #searches through dict for an NPC group equivalent of character's current location
                if npc_group == None:                                           #1 item doesnt appear in list, it is middle_road1(has 4 npc_groups)
                    for npc in self.NPC_group.NPC_groupA:                       #search every npc from npc_group
                        if self.player.block.colliderect(npc.block):
                            return True
                    for npc in self.NPC_group.NPC_groupB:
                        if self.player.block.colliderect(npc.block):
                            return True
                    for npc in self.NPC_group.NPC_groupC:
                        if self.player.block.colliderect(npc.block):
                            return True
                    for npc in self.NPC_group.NPC_groupD:                       #search every npc from npc_group
                        if self.player.block.colliderect(npc.block):
                            return True
                    for npc in self.NPC_group.NPC_groupI:
                        if self.player.block.colliderect(npc.block):
                            return True
                else:
                    for npc in npc_group:
                        if self.player.block.colliderect(npc.block):
                            return True
        return False
    def play_buff_effect(self):
        for buff in self.buff_container.buff_list:
            if buff.picked == True:
                if buff.name == "Invincible":
                    if buff.is_working() == True:
                        self.player.hit_animation()
                        self.player.start_time = pygame.time.get_ticks()
                    else:
                        self.player.start_time = pygame.time.get_ticks() - ((self.player.invincible_time + 1) * 1000)
                        self.player.make_visible()
                        self.buff_container.buff_list.remove(buff)
                elif buff.name == "SpeedUp":
                    if buff.is_working() == False:
                        self.player.player_speed -= 5
                        self.buff_container.buff_list.remove(buff)
                elif buff.name == "StopTime":
                    if buff.is_working() == True:
                        self.logic.stop_timer()
                        self.stop_NPCs = True
                    if buff.is_working() == False:
                        self.logic.resume_timer()
                        self.stop_NPCs = False
                        self.buff_container.buff_list.remove(buff)


    def game_over(self):
        self.draw()
        self.screen.blit(self.interface.Skull,pygame.Rect(self.screen.get_width()/2 - 200,self.screen.get_height()- 660,1,1))
        pygame.display.flip()
        self.player.block.x = self.screen.get_width() / 3 + 30
        self.player.block.y = self.screen.get_height() / 2 - 40
        dest = [self.logic.places_hash.get(self.logic.random_places_save[0].width),
                self.logic.places_hash.get(self.logic.random_places_save[1].width),
                self.logic.places_hash.get(self.logic.random_places_save[2].width)]
        self.menu.save_game(self.level,dest,self.timer_save,self.player.money,self.player.points,self.upgrades,local=True)
        self.menu.path = "Local/autosave.json"
        self.init_level()
        self.load_game()
        self.intro.deactivate_scenes()
        self.shuffle_NPCs(self.menu.NPCset_path)
        pygame.mixer.music.load('Soundtrack/in-game.mp3')
        pygame.mixer.music.play(True)
    def shuffle_NPCs(self,fName = 'None'):
        files = listdir("NPC_sets/")
        rand = Random()
        randd = rand.randint(1,len(files)-1)
        if fName == 'None':
            self.menu.NPCset_path = files[randd]
            json_file = open("NPC_sets/" + files[randd],'r',encoding="utf-8")
        else:
            self.menu.NPCset_path = fName
            json_file = open("NPC_sets/" + fName, 'r', encoding="utf-8")
        data1 = json.load(json_file)
        json_file.close()
        NPC_groups = data1["NPC_groups"]
        commands = data1["Commands"]
        self.NPC_group.command_hash.clear()

        self.NPC_group.NPC_groupA.clear()
        self.NPC_group.NPC_groupB.clear()
        self.NPC_group.NPC_groupC.clear()
        self.NPC_group.NPC_groupD.clear()
        self.NPC_group.NPC_groupE.clear()
        self.NPC_group.NPC_groupF.clear()
        self.NPC_group.NPC_groupG.clear()
        self.NPC_group.NPC_groupH.clear()
        self.NPC_group.NPC_groupI.clear()
        self.NPC_group.NPC_groupJ.clear()
        self.NPC_group.NPC_groupK.clear()

        for npc in NPC_groups["NPC_groupA"]:
            if npc["type"] == "NPC":
                self.NPC_group.NPC_groupA.append(NPC(self.world.north1_block, npc["x"], npc["y"], npc["speed"]))
            elif npc["type"] == "Animal":
                self.NPC_group.NPC_groupA.append(Animal(self.world.north1_block, npc["x"], npc["y"], npc["speed"]))
            cmd_key = '(' + str(npc["x"]) + ', ' + str(npc['y']) + ')'
            try:
                temp = commands["NPC_groupA"][cmd_key]
                self.NPC_group.command_hash.update({cmd_key: commands["NPC_groupA"][cmd_key]})
            except KeyError:
                pass
        for npc in NPC_groups["NPC_groupB"]:
            if npc["type"] == "NPC":
                self.NPC_group.NPC_groupB.append(NPC(self.world.north1_block, npc["x"], npc["y"], npc["speed"]))
            elif npc["type"] == "Animal":
                self.NPC_group.NPC_groupB.append(Animal(self.world.north1_block, npc["x"], npc["y"], npc["speed"]))
            cmd_key = '(' + str(npc["x"]) + ', ' + str(npc['y']) + ')'
            try:
                temp = commands["NPC_groupB"][cmd_key]
                self.NPC_group.command_hash.update({cmd_key:commands["NPC_groupB"][cmd_key]})
            except KeyError:
                pass
        for npc in NPC_groups["NPC_groupC"]:
            if npc["type"] == "NPC":
                self.NPC_group.NPC_groupC.append(NPC(self.world.north1_block, npc["x"], npc["y"], npc["speed"]))
            elif npc["type"] == "Animal":
                self.NPC_group.NPC_groupC.append(Animal(self.world.north1_block, npc["x"], npc["y"], npc["speed"]))
            cmd_key = '(' + str(npc["x"]) + ', ' + str(npc['y']) + ')'
            try:
                temp = commands["NPC_groupC"][cmd_key]
                self.NPC_group.command_hash.update({cmd_key: commands["NPC_groupC"][cmd_key]})
            except KeyError:
                pass
        for npc in NPC_groups["NPC_groupD"]:
            if npc["type"] == "NPC":
                self.NPC_group.NPC_groupD.append(NPC(self.world.north1_block, npc["x"], npc["y"], npc["speed"]))
            elif npc["type"] == "Animal":
                self.NPC_group.NPC_groupD.append(Animal(self.world.north1_block, npc["x"], npc["y"], npc["speed"]))
            cmd_key = '(' + str(npc["x"]) + ', ' + str(npc['y']) + ')'
            try:
                temp = commands["NPC_groupD"][cmd_key]
                self.NPC_group.command_hash.update({cmd_key: commands["NPC_groupD"][cmd_key]})
            except KeyError:
                pass
        for npc in NPC_groups["NPC_groupE"]:
            if npc["type"] == "NPC":
                self.NPC_group.NPC_groupE.append(NPC(self.world.north1_block, npc["x"], npc["y"], npc["speed"]))
            elif npc["type"] == "Animal":
                self.NPC_group.NPC_groupE.append(Animal(self.world.north1_block, npc["x"], npc["y"], npc["speed"]))
            cmd_key = '(' + str(npc["x"]) + ', ' + str(npc['y']) + ')'
            try:
                temp = commands["NPC_groupE"][cmd_key]
                self.NPC_group.command_hash.update({cmd_key: commands["NPC_groupE"][cmd_key]})
            except KeyError:
                pass
        for npc in NPC_groups["NPC_groupF"]:
            if npc["type"] == "NPC":
                self.NPC_group.NPC_groupF.append(NPC(self.world.north1_block, npc["x"], npc["y"], npc["speed"]))
            elif npc["type"] == "Animal":
                self.NPC_group.NPC_groupF.append(Animal(self.world.north1_block, npc["x"], npc["y"], npc["speed"]))
            cmd_key = '(' + str(npc["x"]) + ', ' + str(npc['y']) + ')'
            try:
                temp = commands["NPC_groupF"][cmd_key]
                self.NPC_group.command_hash.update({cmd_key: commands["NPC_groupF"][cmd_key]})
            except KeyError:
                pass
        for npc in NPC_groups["NPC_groupG"]:
            if npc["type"] == "NPC":
                self.NPC_group.NPC_groupG.append(NPC(self.world.north1_block, npc["x"], npc["y"], npc["speed"]))
            elif npc["type"] == "Animal":
                self.NPC_group.NPC_groupG.append(Animal(self.world.north1_block, npc["x"], npc["y"], npc["speed"]))
            cmd_key = '(' + str(npc["x"]) + ', ' + str(npc['y']) + ')'
            try:
                temp = commands["NPC_groupG"][cmd_key]
                self.NPC_group.command_hash.update({cmd_key: commands["NPC_groupG"][cmd_key]})
            except KeyError:
                pass
        for npc in NPC_groups["NPC_groupH"]:
            if npc["type"] == "NPC":
                self.NPC_group.NPC_groupH.append(NPC(self.world.north1_block, npc["x"], npc["y"], npc["speed"]))
            elif npc["type"] == "Animal":
                self.NPC_group.NPC_groupH.append(Animal(self.world.north1_block, npc["x"], npc["y"], npc["speed"]))
            cmd_key = '(' + str(npc["x"]) + ', ' + str(npc['y']) + ')'
            try:
                temp = commands["NPC_groupH"][cmd_key]
                self.NPC_group.command_hash.update({cmd_key: commands["NPC_groupH"][cmd_key]})
            except KeyError:
                pass
        for npc in NPC_groups["NPC_groupI"]:
            if npc["type"] == "NPC":
                self.NPC_group.NPC_groupI.append(NPC(self.world.north1_block, npc["x"], npc["y"], npc["speed"]))
            elif npc["type"] == "Animal":
                self.NPC_group.NPC_groupI.append(Animal(self.world.north1_block, npc["x"], npc["y"], npc["speed"]))

            cmd_key = '(' + str(npc["x"]) + ', ' + str(npc['y']) + ')'
            try:
                temp = commands["NPC_groupI"][cmd_key]

                self.NPC_group.command_hash.update({cmd_key: commands["NPC_groupI"][cmd_key]})
            except KeyError:
                pass
        for npc in NPC_groups["NPC_groupJ"]:
            if npc["type"] == "NPC":
                self.NPC_group.NPC_groupJ.append(NPC(self.world.north1_block, npc["x"], npc["y"], npc["speed"]))
            elif npc["type"] == "Animal":
                self.NPC_group.NPC_groupJ.append(Animal(self.world.north1_block, npc["x"], npc["y"], npc["speed"]))
            cmd_key = '(' + str(npc["x"]) + ', ' + str(npc['y']) + ')'
            try:
                temp = commands["NPC_groupJ"][cmd_key]
                self.NPC_group.command_hash.update({cmd_key: commands["NPC_groupJ"][cmd_key]})
            except KeyError:
                pass
        for npc in NPC_groups["NPC_groupK"]:
            if npc["type"] == "NPC":
                self.NPC_group.NPC_groupK.append(NPC(self.world.north1_block, npc["x"], npc["y"], npc["speed"]))
            elif npc["type"] == "Animal":
                self.NPC_group.NPC_groupK.append(Animal(self.world.north1_block, npc["x"], npc["y"], npc["speed"]))
            cmd_key = '(' + str(npc["x"]) + ', ' + str(npc['y']) + ')'
            try:
                temp = commands["NPC_groupK"][cmd_key]
                self.NPC_group.command_hash.update({cmd_key: commands["NPC_groupK"][cmd_key]})
            except KeyError:
                pass
        self.NPC_group.NPC_list = self.NPC_group.NPC_groupA + self.NPC_group.NPC_groupB + self.NPC_group.NPC_groupC + self.NPC_group.NPC_groupD + \
                        self.NPC_group.NPC_groupE + self.NPC_group.NPC_groupF + self.NPC_group.NPC_groupG + self.NPC_group.NPC_groupH + self.NPC_group.NPC_groupI + \
                        self.NPC_group.NPC_groupK + self.NPC_group.NPC_groupJ

    def load_game(self,new = False):
        if new == True:
            self.menu.path = 'Local/firstMap.json'
        json_file = open(self.menu.path,'r',encoding='utf-8')
        data = json.load(json_file)
        json_file.close()
        self.level = data["Level"]
        self.menu.NPCset_path = data["NPC_set"]
        self.player.money = data["Money"]
        places = data["Destinations"]
        self.upgrades = data["Skills"]
        self.asign_upgrades(self.upgrades)
        self.player.lives = self.player.const_lives
        self.timer_save = data["Timer"]
        if self.timer_save > 0:
            self.logic.set_timer(self.timer_save)
        places_list = [places[0],places[1],places[2]]
        self.logic.set_random_places_manually(places[0],places[1],places[2])
        self.interface.set_Paper(places_list)


    def player_collided(self):
        if self.player.block.colliderect(self.world.south1_block):
            if self.collider.character_collided(self.collider.sprite_south1):
                return True
        elif self.player.block.colliderect(self.world.middle_road2_block):
            if self.collider.character_collided(self.collider.sprite_middle2):
                return True
        elif self.player.block.colliderect(self.world.middle_road1_block):
            if self.collider.character_collided(self.collider.sprite_middle1):
                return True
        elif self.player.block.colliderect(self.world.center1_block):
            if self.collider.character_collided(self.collider.sprite_center1):
                return True
        elif self.player.block.colliderect(self.world.north1_block):
            if self.collider.character_collided(self.collider.sprite_north1):
                return True
        elif self.player.block.colliderect(self.world.south2_block):
            if self.collider.character_collided(self.collider.sprite_south2):
                return True
        elif self.player.block.colliderect(self.world.north2_block):
            if self.collider.character_collided(self.collider.sprite_north2):
                return True
        elif self.player.block.colliderect(self.world.center2_block):
            if self.collider.character_collided(self.collider.sprite_center2):
                return True
        return False

def main():
    Game()
if __name__=="__main__":
    main()

