from pygame import image as im
from pygame import Rect
from pygame import time
from random import Random as rand
class BuffContainer:
    def __init__(self,north):
        #lists of areas coliding with roads on map
        self.north = north
        self.buff_count = 3
        self.width_list = [(800,1000),(500,2000),(2500,2900),(2500,2900),(375,4900),(3300,4500)]
        self.height_list = [(1650,3400),(4560,4790),(2700,5000),(1000,2200),(580,900),(4360,4620)]
        self.buffs = [SpeedUp,StopTime,BoxGun,Invincible,HealthUp]
        self.buff_names = ["SpeedUp","StopTime","BoxGun","Invincible","HealthUp"]
        self.buff_to_time = {"SpeedUp" : 5, "Invincible" : 5, "StopTime" : 5,
                             "BoxGun" : None, "HealthUp" : None}
        self.buff_list = []
        self.init_buff_list()

    def add_buff(self,buff):
        self.buff_list.append(buff)

    def pop_buff(self,buff):
        self.buff_list.remove(buff)

    def move_buffs(self,x,y):
        for buff in self.buff_list:
            buff.block = buff.block.move(x,y)

    def deactivate_buffs(self):
        for buff in self.buff_list:
            if buff.is_working():
                buff.deactivate()

    def clear_list(self):
        self.buff_list.clear()

    def init_buff_list(self):
        self.buff_list.clear()

        for i in range(0,self.buff_count):
            list_index = rand().randint(0,len(self.width_list) - 1)
            width = self.width_list[list_index][1] - self.width_list[list_index][0]
            height = self.height_list[list_index][1] - self.height_list[list_index][0]

            area = Rect(self.width_list[list_index][0],self.height_list[list_index][0],width,height)
            buffx = rand().randint(area.left,area.right)
            buffy = rand().randint(area.top,area.bottom)
            index = rand().randint(0,len(self.buffs) - 1)
            self.buff_list.append(self.buffs[index](self.north,buffx,buffy,self.buff_to_time[self.buff_names[index]]))

    def upgrade_buff_time(self,buff_name, time):
        self.buff_to_time[buff_name] += time
    def set_buff_time(self,buff_name,time):
        self.buff_to_time[buff_name] = time
class SpeedUp:
    def __init__(self,north, x, y,time):
        self.north = north
        self.block = Rect(self.north.x + x, self.north.y + y, 70,70)
        self.image = im.load("Buffs/SpeedUp.png")

        self.time = time
        self.picked = False
        self.start_time = 0
        self.name = "SpeedUp"

    def activate(self):
        self.start_time = time.get_ticks()
    def deactivate(self):
        self.start_time = time.get_ticks() - 6000
    def is_working(self):
        end_time = time.get_ticks()
        seconds_passed = (end_time - self.start_time) / 1000
        if seconds_passed > self.time:
            return False
        return True

class StopTime:
    def __init__(self, north, x, y,time):
        self.north = north
        self.block = Rect(self.north.x + x, self.north.y + y, 70, 70)
        self.image = im.load("Buffs/StopTime.png")
        self.picked = False
        self.time = time
        self.start_time = 0
        self.name = "StopTime"
    def activate(self):
        self.start_time = time.get_ticks()
    def deactivate(self):
        self.start_time = time.get_ticks() - 6000
    def is_working(self):
        end_time = time.get_ticks()
        seconds_passed = (end_time - self.start_time) / 1000
        if seconds_passed > self.time:
            return False
        return True

class BoxGun:
    def __init__(self, north, x, y,time = None):
        self.north = north
        self.block = Rect(self.north.x + x, self.north.y + y, 70, 70)
        self.image = im.load("Buffs/BoxGun.png")
        self.picked = False
        self.bullet = 0
        self.name = "BoxGun"
    def activate(self):
        self.bullet += 1
    def deactivate(self):
        self.bullet -= 1
    def is_working(self):
        if self.bullet != 0:
            return True
        return False

class Invincible:
    def __init__(self, north, x, y, time):
        self.north = north
        self.block = Rect(self.north.x + x, self.north.y + y, 70, 70)
        self.image = im.load("Buffs/Invincible.png")
        self.picked = False
        self.time = time
        self.start_time = 0
        self.name = "Invincible"
    def activate(self):
        self.start_time = time.get_ticks()
    def deactivate(self):
        self.start_time = time.get_ticks() - 6000
    def is_working(self):
        end_time = time.get_ticks()
        seconds_passed = (end_time - self.start_time) / 1000
        if seconds_passed > self.time:
            return False
        return True

class HealthUp:
    def __init__(self, north, x, y, time = None):
        self.north = north
        self.block = Rect(self.north.x + x, self.north.y + y, 70, 70)
        self.image = im.load("Buffs/HealthUp.png")
        self.picked = False
        self.health = 0
        self.name = "HealthUp"
    def activate(self):
        self.health += 1
    def deactivate(self):
        self.health -= 1
    def is_working(self):
        if self.health != 0:
            return True
        return False