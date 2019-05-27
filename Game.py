import pygame
import sys
from Character import Boy
from Worlds import World

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
        self.worlds = [World(self.screen,self.player)]
        self.worlds_i=0
    def initOptions(self):
        #Variables
        self.speed = 6
        self.fps = 30
        self.bullet = False
        self.hit_flag=False
        self.player_delay = 0

        #Basics
        self.screen = pygame.display.set_mode((1600,900),pygame.FULLSCREEN)
        self.screen=pygame.display.set_mode()
        self.clk = pygame.time.Clock()
    def draw(self):
        #pygame.draw.rect(self.screen,(255,255,0),(self.screen.get_width()/3,self.screen.get_height()/2,200,100))
        self.worlds[self.worlds_i].place()
        if self.bullet == True:
            self.shoot()
        (self.movement_head, self.movement_torso, self.movement_legs, self.movement_weapon) = self.action[
                self.move_i]()
        self.screen.blit(self.movement_legs, self.player.Legs_block)
        self.screen.blit(self.movement_torso, self.player.Torso_block)
        self.screen.blit(self.movement_head,self.player.Head_block)
        self.screen.blit(self.movement_weapon, self.player.Weapon_block)
    def start(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)
            self.screen.fill((190,170,76))
            self.move()
            self.draw()
            #if self.bullet == True:
           #     self.shoot()
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
            if not pygame.key.get_pressed()[pygame.K_SPACE] or ~self.player.ARMED:
                if pygame.key.get_pressed()[pygame.K_d] or pygame.key.get_pressed()[pygame.K_RIGHT]:
                    self.move_i = 4
                    self.stay_i = 2
                    self.player.relocate(1,0);
                if pygame.key.get_pressed()[pygame.K_a] or pygame.key.get_pressed()[pygame.K_LEFT]:
                    self.move_i = 5
                    self.stay_i = 3
                    self.player.relocate(-1, 0);
                if pygame.key.get_pressed()[pygame.K_s] or pygame.key.get_pressed()[pygame.K_DOWN]:
                    self.move_i = 1
                    self.stay_i = 0
                    self.player.relocate(0, 1);
                if pygame.key.get_pressed()[pygame.K_w] or pygame.key.get_pressed()[pygame.K_UP]:
                    self.move_i = 7
                    self.stay_i = 6
                    self.player.relocate(0 , -1);
            if pygame.key.get_pressed()[pygame.K_SPACE] and self.player.ARMED:
                        self.hit_flag = True
                        if self.stay_i == 0:
                            self.move_i = 8
                        elif self.stay_i == 3:
                            self.move_i = 9
                        elif self.stay_i == 2 :
                            self.move_i = 10
                        elif self.stay_i == 6:
                            self.move_i = 11
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

