from os import listdir
from random import Random
from pygame import Rect, time
from pygame import image
from pygame import mixer
from pygame.constants import USEREVENT


class Logic():
    def __init__(self,north):
        self.random_places = []
        self.north_block =  north
        self.init_places()
        self.init_NPCs()
        self.init_timer()
        self.timer_start = False
        self.rand = Random()
        self.fps = 0
        self.sprite = -1
        self.frames = 0
        self.level_finished = False
        self.finish = [image.load("GUI/flag/" + file).convert_alpha() for file in listdir("GUI/flag/")]
        self.deliver_sound = mixer.Sound('Soundtrack/deliver.ogg')
    def init_NPCs(self):
        self.armorer = [image.load("Destinations/armor/" + file).convert_alpha() for file in listdir("Destinations/armor/")]
        self.blacksmith = [image.load("Destinations/blacksmith/" + file).convert_alpha() for file in listdir("Destinations/blacksmith")]
        self.clown = [image.load("Destinations/clown/" + file).convert_alpha() for file in listdir("Destinations/clown")]
        self.lumber = [image.load("Destinations/lumber/" + file).convert_alpha() for file in listdir("Destinations/lumber")]
        self.oldman = [image.load("Destinations/oldman/" + file).convert_alpha() for file in listdir("Destinations/oldman")]
        self.priest = [image.load("Destinations/priest/" + file).convert_alpha() for file in listdir("Destinations/priest")]
        self.richman = [image.load("Destinations/rich/" + file).convert_alpha() for file in listdir("Destinations/rich")]
        self.NPCs_hash = {0:self.armorer,1:self.clown,2:self.lumber,3:self.priest,4:self.blacksmith,5:self.richman,6:self.oldman}
        self.sprite_list = [0,0,0,0,0,0,0]
    def animate_NPC(self):
        if self.sprite != -1:
            if self.fps >= 3:
                self.fps = 0
                self.sprite_list[self.sprite] += 1
                if self.sprite_list[self.sprite] >= 2:
                    self.sprite = -1
            self.fps += 1
    def get_salary(self,level):
        temp = 1
        salary = 80
        #every level the salary goes up by 30
        while temp <= level:
            salary += 40
            temp += 1
        return salary

    def get_pts_per_sec(self, level):
        temp = 1
        pts = 6
        while temp <= level:
            if temp % 2:
                pts += 3
            temp += 1
        return pts
        #initialize positions of locations to which the player needs to deliver package
    def init_places(self):
        self.armory = Rect(self.north_block.x + 761,self.north_block.y + 607,140,108)
        self.circus = Rect(self.north_block.x + 4767, self.north_block.y + 3965, 87 ,117)
        self.cabin = Rect(self.north_block.x + 697, self.north_block.y + 2395, 60,64)
        self.church = Rect(self.north_block.x + 3194,self.north_block.y + 2467,99,85)
        self.blacksmth = Rect(self.north_block.x + 4658, self.north_block.y + 498, 137, 86)
        self.villa = Rect(self.north_block.x + 2131, self.north_block.y + 2682, 52, 49 )
        self.square = Rect(self.north_block.x + 569, self.north_block.y + 4422, 132, 66)
        self.finish_block = Rect(self.north_block.x + 530, self.north_block.y + 4290, 200, 140)
        self.house = Rect(self.north_block.x + 4900, self.north_block.y + 600, 130, 70)
        self.places = [self.armory, self.circus, self.cabin, self.church, self.blacksmth, self.villa,self.house]
        self.random_places_save = []
        self.places_hash = {self.armory.width:0, self.circus.width:1, self.cabin.width:2, self.church.width:3, self.blacksmth.width:4, self.villa.width:5,self.house.width:6}

    #set/reset random_places list containing 3 places where the player currently needs to arrive to
    def set_random_places(self):
        places_list = [] #this list is used by Interface to set up correct images for Paper
        #self.reset_places()
        if len(self.random_places) == 3:
            self.random_places.clear()
        for i in range(0,3):
            random = self.rand.randint(0, len(self.places) - 1)
            while places_list.__contains__(random) == True:
                random = self.rand.randint(0,len(self.places) - 1)
            places_list.append(random)
            self.random_places.append(self.places[random])
        self.random_places_save = self.random_places.copy()
        return places_list


    #change positions of places accordingly to players speed
    def change_random_places_positions(self,x,y):
        self.finish_block = self.finish_block.move(x,y)
        for i in range(0,len(self.random_places)):
            self.random_places[i] = self.random_places[i].move(x,y)
        for i in range(0,len(self.random_places_save)):
            self.random_places_save[i] = self.random_places_save[i].move(x,y)


    #pop element from list of random_places if player delivered package
    def check_list(self, player):
        self.animate_NPC()
        if self.almost_finished():
            self.player_delivered(self.finish_block,player)
        else:
            for place in self.random_places:
                if self.player_delivered(place, player):
                    self.random_places.remove(place)

    def almost_finished(self): #if all packages been delivered
        if len(self.random_places) == 0:
            return True
        return False
    def set_random_places_manually(self,index1,index2,index3):
        self.random_places = [self.places[index1],self.places[index2],self.places[index3]]
        self.random_places_save = self.random_places.copy()
    #return True if PLayer delivered package to chosen destination
    def player_delivered(self, destination, player):
        if player.colliderect(destination):
            self.deliver_sound.play()

            if self.places_hash.get(destination.width) != None:
                self.sprite = self.places_hash.get(destination.width)
            else:
                self.sprite = -1
            if  self.almost_finished() == True:
                self.sprite_list = [0,0,0,0,0,0,0]
                self.level_finished = True
            return True
        return False
    def finish_anim(self): #display finish flag animation in front of post office
        if self.fps >= 3:
            self.fps = 0
            self.frames+=1
            if self.frames >= 7:
                self.frames = 0
        self.fps += 1
        return self.finish[self.frames]
    def set_timer(self,seconds):
        self.timer = seconds
        self.timer_start = True
    def stop_timer(self):
        time.set_timer(USEREVENT,6000)
    def resume_timer(self):
        time.set_timer(USEREVENT,1000)
    def init_timer(self):
         self.timer = 0
         time.set_timer(USEREVENT, 1000)


