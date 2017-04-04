import pygame
from ..constants import *
from pygame import *
from ..functions import *

class Davis(pygame.sprite.Sprite):
    def __init__(self,x,y):
        self.images,self.rect = load_sprite_sheet('davis_0.bmp',10,7,70,70,-1)
        self.images1,self.rect = load_sprite_sheet('davis_1.bmp',10,7,70,70,-1)
        self.images2,self.rect = load_sprite_sheet('davis_2.bmp',10,7,70,70,-1)
        self.image = self.images[0]
        self.index = 0

        self.isWalking = False
        self.walk_arr = [4,5,6,7,6,5]
        self.walk_arr_index = 0
        self.walk_blit_rate = 3
        self.walk_speed = 7
        self.direction = 1

        self.stand_arr = [0,1,2,3,2,1]
        self.stand_arr_index = 0
        self.stand_blit_rate = 4

        self.isPunching = False
        self.punch_arr = [10,11,12,13,14,15,16,17]
        self.punch_arr_index = 0
        self.punch_blit_rate = 2

        self.isFiringBlast = False
        self.firingBlast_arr = [0,1,2,3,4,5,6,7,8,9]
        self.firingBlast_arr_index = 0
        self.firingBlast_blit_rate = 2
        self.mana = 100

        self.isBlocking = False
        self.block_arr = [56,57]
        self.block_arr_index = 0
        self.block_resist = 2

        self.isJumping = False
        self.jump_arr = [62]
        self.jump_arr_index = 0
        #self.jumpHeight = self.rect.height/2
        self.jumpSpeed = 10
        self.temp_jump_base = 0

        self.movement = [0,0]

        self.rect.left = x
        self.rect.top = y

        self.sheet_number = 0
        self.health = 100
        self.counter = 0

    def draw(self):
        screen.blit(self.image,self.rect)

    def update(self):
        """------------------------Checking player status--------------------------------"""
        if self.isWalking:
            if self.counter%self.walk_blit_rate == 0:
                self.index = self.walk_arr[self.walk_arr_index]
                self.walk_arr_index = (self.walk_arr_index + 1)%len(self.walk_arr)

            self.rect = self.rect.move(self.movement)
            self.sheet_number = 0


        elif self.isPunching:
            if self.counter%self.punch_blit_rate == 0:
                self.index = self.punch_arr[self.punch_arr_index]
                self.punch_arr_index = (self.punch_arr_index + 1)%len(self.punch_arr)
            self.sheet_number = 0

        elif self.isBlocking:
            self.index = self.block_arr[self.block_arr_index]
            self.sheet_number = 0

        elif self.isJumping:
            self.index = self.jump_arr[self.jump_arr_index]
            self.sheet_number = 0
            self.movement[1] = self.movement[1] + gravity
            self.rect = self.rect.move(self.movement)

        elif self.isFiringBlast and self.mana > 0:
            if self.counter%self.firingBlast_blit_rate == 0:
                self.index = self.firingBlast_arr[self.firingBlast_arr_index]
                self.firingBlast_arr_index = (self.firingBlast_arr_index + 1)%len(self.firingBlast_arr)

                if self.index == 3:
                    DavisBall(self.rect.centerx + self.direction*(self.rect.width/2), self.rect.centery + 5, self.direction)
                    self.mana -= 5
                elif self.index == 8:
                    DavisBall(self.rect.centerx + self.direction*(self.rect.width/2), self.rect.centery, self.direction)
                    self.mana -= 5

            self.sheet_number = 2

        else:
            if self.counter%self.stand_blit_rate == 0:
                self.index = self.stand_arr[self.stand_arr_index]
                self.stand_arr_index = (self.stand_arr_index + 1)%len(self.stand_arr)
            self.sheet_number = 0

        """------------------------Selecting sheet number--------------------------------"""

        if self.sheet_number == 0:
            self.image = self.images[self.index]
        elif self.sheet_number == 1:
            self.image = self.images1[self.index]
        elif self.sheet_number == 2:
            self.image = self.images2[self.index]

        """-------------------------------Other updates----------------------------------"""

        if self.direction < 0:
            self.image = pygame.transform.flip(self.image,True,False)

        if self.mana < 0:
            self.mana = 0

        if self.isFiringBlast == False and self.mana < 100 and self.counter%4 == 0:
            self.mana += 1

        self.counter = (self.counter + 1)%10000000000
        self.checkbounds()

    def checkbounds(self):
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > width:
            self.rect.right = width
        if self.rect.top < int(height*0.25):
            self.rect.top = int(height*0.25)
        if self.rect.bottom > height:
            self.rect.bottom = height

        if self.rect.bottom > self.temp_jump_base and self.isJumping == True:
            self.rect.bottom = self.temp_jump_base
            self.isJumping = False
            self.movement = [0,0]

class DavisBall(pygame.sprite.Sprite):
    def __init__(self,x,y,direction=1):
        pygame.sprite.Sprite.__init__(self,self.containers)
        self.images,self.rect = load_sprite_sheet('davis_ball.bmp',4,3,69,40,-1)
        self.image = self.images[0]
        self.index = 3
        self.direction = direction

        self.movement = [direction*10,0]
        self.rect.centerx = x
        self.rect.centery = y

        self.counter = 0

    def draw(self):
        screen.blit(self.image,self.rect)

    def update(self):
        self.image = self.images[self.index]
        if self.direction == -1:
            self.image = pygame.transform.flip(self.image, True, False)

        if self.rect.left > width:
            self.kill()
        self.rect = self.rect.move(self.movement)
        self.counter = (self.counter + 1)%10000000000
