import pygame
import sys
from Character import Boy
import Worlds


class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        pygame.display.init()
        self.initOptions()
        self.initObjects()
        self.start()

    def initObjects(self):
        #Player and player animation
        self.player = Boy(self.screen)
        self.action = [self.player.stay_front, self.player.walk_front, self.player.stay_right,
                          self.player.stay_left,self.player.walk_right, self.player.walk_left,\
                          self.player.stay_back, self.player.walk_back,self.player.hit_front,\
                          self.player.hit_left,self.player.hit_right,self.player.hit_back]

        self.move_i = 0
        self.stay_i=0
        #Equipment
        self.Bullet_x = self.player.block.x + 45
        self.Bullet_y = self.player.block.y + 30
        #Worlds
        self.worlds = [Worlds.World(self.screen, self.player, self.map_x, self.map_y), Worlds.City(self.screen, self.player, self.map_x, self.map_y)]
        self.worlds_i = 1
    def static_anim(self):
        #try:
        self.screen.blit(self.worlds[self.worlds_i].anim_fountain(),self.worlds[self.worlds_i].fount_block) 
      #  except AttributeError:
       #     print("nwm nwm")
    def initOptions(self):
        #Variables
        self.speed = 6
        self.fps = 30
        self.bullet = False
        self.hit_flag=False
        self.player_delay = 0
        self.map_x = 1
        self.map_y = 1
        #Basics
        self.screen = pygame.display.set_mode((1600,900),pygame.FULLSCREEN)
        self.screen=pygame.display.set_mode()
        self.clk = pygame.time.Clock()
    def draw(self):
        #moving every part of character to a certain position set in move()
        (self.movement_head, self.movement_torso, self.movement_legs, self.movement_weapon) = self.action[
                self.move_i]()
        self.screen.blit(self.worlds[self.worlds_i].map, (self.map_x, self.map_y))
        self.screen.blit(self.movement_legs, self.player.Legs_block)
        self.screen.blit(self.movement_torso, self.player.Torso_block)
        self.screen.blit(self.movement_head,self.player.Head_block)
        self.screen.blit(self.movement_weapon, self.player.Weapon_block)
        self.static_anim()

    def start(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)
            self.screen.fill((190,170,76))
            self.move()
            self.draw()
            #if self.bullet == True:
            #    self.shoot()
            pygame.display.flip()
            self.clk.tick(self.fps)

    def move(self):
        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            sys.exit(0)
        self.player.player_speed = 5
        if pygame.key.get_pressed()[pygame.K_LSHIFT]:
            self.player.player_speed = 10
        if self.is_hitting():
            self.player_delay+=1
        else:
            self.move_i=self.stay_i
            self.player_delay = 0
            self.hit_flag=False
            if (not pygame.key.get_pressed()[pygame.K_SPACE] or ~self.player.ARMED):
                if pygame.key.get_pressed()[pygame.K_d] or pygame.key.get_pressed()[pygame.K_RIGHT]:
                    self.move_i = 4
                    self.stay_i = 2
                    if self.can_move_frame("right"):
                        self.map_x -= self.player.player_speed
                    else:
                        self.player.relocate(1,0);
                if pygame.key.get_pressed()[pygame.K_a] or pygame.key.get_pressed()[pygame.K_LEFT]:      
                    self.move_i = 5
                    self.stay_i = 3
                    if self.can_move_frame("left"):
                        self.map_x += self.player.player_speed
                    else:
                        self.player.relocate(-1, 0);
                if pygame.key.get_pressed()[pygame.K_s] or pygame.key.get_pressed()[pygame.K_DOWN]:
                    self.move_i = 1
                    self.stay_i = 0
                    if self.can_move_frame("down"):
                        self.map_y -= self.player.player_speed
                    else:
                        self.player.relocate(0, 1);
                if pygame.key.get_pressed()[pygame.K_w] or pygame.key.get_pressed()[pygame.K_UP]:
                    self.move_i = 7
                    self.stay_i = 6
                    if self.can_move_frame("up"):
                        self.map_y += self.player.player_speed
                    else:
                        self.player.relocate(0 , -1);
            if pygame.key.get_pressed()[pygame.K_SPACE] and self.player.ARMED:
                        self.hit_flag = True
                        if self.stay_i == 0:
                            self.move_i = 8
                        elif self.stay_i == 3:
                            self.move_i = 9
                        elif self.stay_i == 2:
                            self.move_i = 10
                        elif self.stay_i == 6:
                            self.move_i = 11
            if self.player_out_of_range():
                if self.move_i == 4:
                    self.player.relocate(-1,0)
                if self.move_i == 5:
                    self.player.relocate(1,0)
                if self.move_i == 1:
                    self.player.relocate(0,-1)
                if self.move_i == 7:
                    self.player.relocate(0,1)
   
    def can_move_frame(self, axis):
        if axis == "up":
            if self.player.Torso_block.y <= self.screen.get_height()*2/5 and self.map_y < 0:
                return True
        if axis == "down":
            if self.player.Torso_block.y >= self.screen.get_height()*3/5 and self.worlds[self.worlds_i].map.get_height() + self.map_y > self.screen.get_height():
                return True
        if axis == "right":
            if self.player.Torso_block.x >= self.screen.get_width()*3/5 and self.worlds[self.worlds_i].map.get_width() + self.map_x > self.screen.get_width():
                return True
        if axis == "left":
            if self.player.Torso_block.x <= self.screen.get_width()*2/5 and self.map_x < 0:
                return True
        return False

    def player_out_of_range(self):
        if self.player.Torso_block.left <= self.map_x:
            return True
        if self.player.Torso_block.right >= self.worlds[self.worlds_i].map.get_width()+self.map_x:
            return True
        if self.player.Legs_block.bottom >= self.worlds[self.worlds_i].map.get_height()+self.map_y:
            return True
        if self.player.Head_block.top <= self.map_y:
            return True
        return False

    def is_hitting(self): #if the animation of hitting is still active
        return (self.hit_flag and self.player_delay<5)

    def shoot(self):
        self.Bullet = pygame.Rect(self.Bullet_x, self.Bullet_y, 5, 5)
        if self.move_i == 4 or self.stay_i == 2:
            self.Bullet_x += 50
        elif self.move_i == 5 or self.stay_i == 3:
            self.Bullet_x -= 50
        elif self.move_i == 7 or self.stay_i == 6:
            self.Bullet_y -= 50
        elif self.move_i == 1 or self.stay_i == 0:
            self.Bullet_y += 50
        pygame.draw.rect(self.screen, 0, self.Bullet)
        if self.Bullet.x >= self.screen.get_width() or self.Bullet.x <= 0 or self.Bullet.y >= self.screen.get_height() or self.Bullet.y <= 0:
            del self.Bullet
            self.Bullet_x = self.player.block.x + 25
            self.Bullet_y =  self.player.block.y + 30
            self.bullet = False


def main():
    Game()
if __name__=="__main__":
    main()

