from math import fabs

from pygame import font
from pygame import Rect
from pygame import Surface
from pygame import time
from pygame import QUIT
from pygame import display
import sys
from pygame import event as ev
class Intro:
    def __init__(self,player,maps_fun,NPC_fun,locations_fun,buff_fun,collider_fun):
        #setup arguments
        self.change_maps_positions = maps_fun
        self.move_all_NPC = NPC_fun
        self.change_random_places_position = locations_fun
        self.player = player
        self.update_maps = collider_fun
        self.move_buffs = buff_fun
        self.init_scenes()
        self.init_camera()
        self.clk = time.Clock()



    def init_camera(self):
        self.start_time = time.get_ticks()
        self.start_time2 = 0
        self.wait_time = 0
        # Camera movement stuff
        self.pathX_list = []
        self.pathY_list = []
        self.wait_list = []
        self.speed = 20
    def init_scenes(self):
        self.scene_semaphore = -1
        self.font = font.SysFont('Calibri', 34, bold=True)
        self.dialogue = Rect(50, 670, 1400, 200)
        self.window = Surface((1450, 240))
        self.window.fill((0, 0, 0))
        self.window.set_alpha(200)
        self.text_surface = Surface((400, 170))
        self.text_surface.fill((0, 0, 0))
        self.text = self.font.render(
            "Witaj dostawco! To twój pierwszy dzień pracy więc jest parę rzeczy które muszę Ci wyjaśnić", True,
            (255, 255, 255))
        self.text2 = self.font.render(
            "Sprawy trochę się zmieniły od kiedy ten cały koronawirus opanował nasze miasteczko. Tak wyszło,", True,
            (255, 255, 255))
        self.text3 = self.font.render(
            "że ludzie nie stosowali się do obostrzeń i zachorowalność w naszym miasteczku wynosi 99%. Jeżeli", True,
            (255, 255, 255))
        self.text4 = self.font.render(
            "nie chcesz do nich dołączyć, pod żadnym pozorem nie wchodź z nikim w kontakt! Rozumiemy się?", True,
            (255, 255, 255))
        self.scene1 = True
        self.scene2 = False
        self.scene3 = False
        self.alpha = 0
        self.text_flag = False
    def is_waiting2(self):
        now = time.get_ticks()
        time_passed = now - self.start_time2
        if time_passed > self.wait_time:
            self.wait_time = 0
            self.start_time2 = time.get_ticks()
            return False
        return True
    def init_scene3(self,set_timer):
        if self.scene3 == True:
            if self.is_waiting2() == False:
                self.scene_semaphore += 1
                if self.scene_semaphore == 0:
                    self.player.make_visible()
                    self.text_flag = True
                    self.text = self.font.render("Słuchaj. Sytuacja się trochę zmieniła. Nie wiem czy oglądałeś wczoraj wiadomości ale podobno", True,(255, 255, 255))
                    self.text2 = self.font.render("wykryto że wirus zmutował. Teraz nazywa się COVID-199 i jest znacznie potężniejszy od swojego ",True, (255, 255, 255))
                    self.text3 = self.font.render("poprzednika COVID-19. COVID-199 działa jak gaz trujący, atakuje płuca w przeciągu minut.", True, (255, 255, 255))
                    self.text4 = self.font.render(" ", True, (255, 255, 255))
                    self.wait_time = 16 * 1000
                elif self.scene_semaphore == 1:
                    self.text = self.font.render("Na szczęście Fundacja Zdrowie ufundowała nam mierniki które podobno liczą stężenie wirusa w ", True,(255, 255, 255))
                    self.text2 = self.font.render("otoczeniu, czy jakoś tak.. mniejsza o to. Najważniejsze że te cudeńka potrafią wyznaczyć czas po ", True,(255, 255, 255))
                    self.text3 = self.font.render("którym wirus dociera do płuc. Musisz teraz monitorować czas i wrócić przed jego końcem.", True,(255, 255, 255))
                    self.text4 = self.font.render("", True,(255, 255, 255))
                    set_timer(186)
                    self.wait_time = 14 * 1000
                elif self.scene_semaphore == 2:
                    self.text = self.font.render("Dla motywacji dodam że im szybciej skończysz zadanie tym większa czeka cię wypłata. ", True,(255, 255, 255))
                    self.text2 = self.font.render("Pomyśl o tym jak o bonusie za produktywną pracę", True,(255, 255, 255))
                    self.text3 = self.font.render("", True, (255, 255, 255))
                    self.text4 = self.font.render("", True,(255, 255, 255))
                    self.wait_time = 8 * 1000
                else:
                    self.scene3 = False
                    self.text_flag = False
                    self.scene_semaphore = -1
    def init_scene2(self,paper_fade,paper_is_hidden):
        if self.scene2 == True:
            if self.is_waiting2() == False:
                self.scene_semaphore += 1
                if self.scene_semaphore == 0:
                    self.speed = 40
                    if paper_is_hidden == True:
                        paper_fade()
                    self.player.make_invisible()
                    self.reset_camera()
                    self.wait_time = 1 * 1000
                elif self.scene_semaphore == 1:
                    self.reset_camera()
                    self.wait_time = 3.4 * 1000
                elif self.scene_semaphore == 2:
                    self.reset_camera()
                    self.wait_time = 2 * 1000
                elif self.scene_semaphore == 3:
                    self.reset_camera()
                    self.wait_time = 3 * 1000
                elif self.scene_semaphore == 4:
                    self.wait_time = 2 * 1000
                    self.reset_camera()
                elif self.scene_semaphore == 5:
                    self.wait_time = 3.2 * 1000
                    self.reset_camera()
                elif self.scene_semaphore == 6:
                    self.reset_camera()
                    self.wait_time = 2 * 1000
                elif self.scene_semaphore == 7:
                    self.wait_time = 3.8 * 1000
                    self.reset_camera()
                else:
                    self.scene2 = False
                    self.text_flag = False
                    self.player.make_visible()
                    self.scene_semaphore = -1
            else:
                if self.scene_semaphore == 0:
                    self.move_camera("Y-300W3")
                elif self.scene_semaphore == 1:
                    self.move_camera("X3700W0.5")
                elif self.scene_semaphore == 3:
                    self.move_camera("Y-3500W0.5")
                elif self.scene_semaphore == 5:
                    self.move_camera("X-3920W0.5")
                elif self.scene_semaphore == 7:
                    self.move_camera("Y3900W0.5")
    def init_scene1(self,paper_fade):
        if self.scene1 == True:
            if self.is_waiting2() == False: #sets up a scenario
                self.scene_semaphore += 1
                if self.scene_semaphore == 0:
                   self.wait_time = 4 * 1000
                   self.start_time2 = time.get_ticks()
                elif self.scene_semaphore == 1:
                    self.text_flag = True
                    self.wait_time = 19 * 1000
                    self.start_time2 = time.get_ticks()
                elif self.scene_semaphore == 2:
                    self.text = self.font.render("W notesie masz zaznaczone miejsca, gdzie nasi klienci oczekują paczek.Normalnie ",True, (255, 255, 255))
                    self.text2 = self.font.render("zapisujemy adresy mieszkań, ale słyszałem że jesteś nowy w okolicy i nie chciałem ryzykować.",True, (255, 255, 255))
                    self.text3 = self.font.render("",True, (255, 255, 255))
                    self.text4 = self.font.render("",True, (255, 255, 255))
                    self.wait_time = 11 * 1000
                    paper_fade()
                    self.start_time2 = time.get_ticks()
                elif self.scene_semaphore == 3:
                    self.text_flag = False
                    self.player.make_invisible()
                    self.wait_time = 4 * 1100
                elif self.scene_semaphore == 4:
                    self.reset_camera()
                    self.text = self.font.render("Na szczęście nasi klienci stosują się do zasad i noszą maseczki, dzięki czemu możesz ", True, (255, 255, 255))
                    self.text2 = self.font.render("ich rozróżnić od zakażeńców.", True, (255, 255, 255))
                    self.text3 = self.font.render("Starałem się rysować w taki sposób żebyś mógł łatwo skojarzyć miejsce z rysunkiem", True,(255, 255, 255))
                    self.text4 = self.font.render("Tak jak w przypadku tej chatki drwala, widać siekierę wbitą w pień jak byk", True,(255, 255, 255))
                    self.wait_time = 16 * 1000
                    self.text_flag = True
                elif self.scene_semaphore == 5:
                    self.text_flag = False
                    self.wait_time = 4 * 1000
                elif self.scene_semaphore == 6:
                    self.wait_time = 4* 1000
                elif self.scene_semaphore == 7:
                    self.reset_camera()
                    self.wait_time = 3 * 1000
                elif self.scene_semaphore == 8:
                    self.reset_camera()
                    self.wait_time = 2 * 1100
                elif self.scene_semaphore == 9:
                    self.wait_time = 3 * 1000
                elif self.scene_semaphore == 10:
                    self.text_flag = True
                    self.text = self.font.render("Kiedy dostarczysz wszystkie paczki, zamelduj się z powrotem na pocztę",True,(255,255,255))
                    self.text2 = self.font.render("",True,(255,255,255))
                    self.text3 = self.font.render("", True, (255, 255, 255))
                    self.text4 = self.font.render("", True, (255, 255, 255))
                    self.wait_time = 5 * 1000
                elif self.scene_semaphore == 11:
                    self.speed = 40
                    self.text_flag = False
                    self.reset_camera()
                    self.wait_time = 3 * 1000
                elif self.scene_semaphore == 12:
                    self.reset_camera()
                    self.wait_time = 3.05 * 1100
                elif self.scene_semaphore == 13:
                    self.text_flag = True
                    self.wait_time = 4 * 1000
                    self.text = self.font.render("To wszystko. Wracam do objadania się kawiorem i liczenia pieniążków.", True, (255, 255, 255))
                    self.text2 = self.font.render("Powodzenia! I do roboty.", True, (255, 255, 255))
                    self.text3 = self.font.render("", True, (255, 255, 255))
                    self.text4 = self.font.render("", True, (255, 255, 255))
                else:
                    self.player.make_visible()
                    self.scene_semaphore = -1
                    self.scene1 = False
                    self.text_flag = False

            else: #plays the scenario
                if self.scene_semaphore == 3:
                    self.move_camera("Y-2000W1")
                elif self.scene_semaphore == 5:
                    self.move_camera("X2400W1")
                elif self.scene_semaphore == 7:
                    self.move_camera("Y-2000W1")
                elif self.scene_semaphore == 8:
                    self.move_camera("X1000W0.1")
                elif self.scene_semaphore == 11:
                    self.move_camera("X-3360W1")
                elif self.scene_semaphore == 12:
                    self.move_camera("Y2700W0.1")

    def deactivate_scenes(self):
        self.scene3 = False
        self.scene2 = False
        self.scene1 = False

    def fade_cinematic(self,level,screen): #Creates fade out cinematic, then blits text on screen "Dzień x" x is day number
        self.window2 = Surface((1600, 900))
        self.window2.fill((0,0,0))
        self.text_surface = Surface((500, 140))
        self.font = font.SysFont('Calibri', 120, bold=True)
        self.text = self.font.render("Dzień " + str(level), True, (255, 255, 255))

        while True:
            for event in ev.get():
                if event.type == QUIT:
                    sys.exit(0)
            screen.fill((255, 255, 255))
            if self.is_waiting2():
                self.text_surface.set_alpha(self.alpha)
                self.alpha += 10 * (self.alpha < 255)

            else:
                if self.alpha < 255:
                    self.wait_time = 3 * 1000
                else:
                    self.font = font.SysFont('Calibri', 32, bold=True)
                    self.alpha = 0
                    break
            self.draw(screen)
            display.flip()
            self.clk.tick(30)
    def draw(self,screen):
        screen.blit(self.window2, (0, 0))
        screen.blit(self.text_surface, (580, 350))
        self.text_surface.blit(self.text, (70, 0))

    def reset_camera(self):
        self.pathY_list.clear()
        self.pathX_list.clear()
        self.wait_list.clear()
    def move_camera(self, command):
        # print("IN")
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
            self.change_maps_positions(-self.speed *sign, 0)
            self.change_random_places_position(-self.speed*sign, 0)
            self.move_all_NPC(-self.speed*sign,0)
            self.move_buffs(-self.speed*sign,0)
            self.update_maps(-self.speed*sign,0)

        elif y < x:
            coord = 'y'
            x = y
            if self.is_waiting(x):
                return
            # check if found number is negative and set flag sign = -1
            sign = self.check_sign(x, y)
            self.change_maps_positions(0,-self.speed * sign)
            self.change_random_places_position(0,-self.speed * sign)
            self.move_all_NPC(0,-self.speed * sign)
            self.move_buffs(0, -self.speed * sign)
            self.update_maps(0, -self.speed * sign)
        else:
            coord = 'xy'
            if x < len(self.pathX_list):
                if self.is_waiting(x):
                    return
                sign = self.check_sign(x, y)
                self.change_maps_positions(self.speed*sign,self.speed*sign)
                self.change_random_places_position(self.speed * sign,self.speed*sign)
                self.move_all_NPC(self.speed*sign, self.speed*sign)
                self.move_buffs(self.speed * sign, self.speed * sign)
                self.update_maps(self.speed * sign, self.speed*sign)
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
                self.start_time = time.get_ticks()
        elif coord == 'y':
            if self.pathY_list[y] == 0:
                self.start_time = time.get_ticks()
        elif coord == 'xy':
            if self.pathX_list[x] == 0 and self.pathY_list[y] == 0:
                self.start_time = time.get_ticks()

        self.pathX_list[x] = self.pathX_list[x] * sign
        self.pathY_list[y] = self.pathY_list[y] * sign

    def is_waiting(self, i):
        end_time = time.get_ticks()
        seconds_passed = (end_time - self.start_time) / 1000
        if seconds_passed > self.wait_list[i]:
            return False
        return True



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
