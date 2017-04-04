import pygame
from ..constants import *
from pygame import *
from ..functions import *

class Bandit(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self,self.containers)
        self.images,self.rect = load_sprite_sheet('bandit_0.bmp',10,7,70,70,-1)
        self.image = self.images[0]
        self.index = 0

        self.isWalking = True
        self.walk_arr = [4,5,6,7,6,5]
        self.walk_arr_index = 0
        self.walk_blit_rate = 3
        self.walk_speed = 3
        self.direction = -1

        self.stand_arr = [0,1,2,3,2,1]
        self.stand_arr_index = 0
        self.stand_blit_rate = 4

        self.isPunching = False
        self.punch_arr = [10,11,12,13,14,15,16,17]
        self.punch_arr_index = 0
        self.punch_blit_rate = 3

        self.movement = [0,0]

        self.rect.left = x
        self.rect.top = y

        self.health = 10
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

        else:
            if self.counter%self.stand_blit_rate == 0:
                self.index = self.stand_arr[self.stand_arr_index]
                self.stand_arr_index = (self.stand_arr_index + 1)%len(self.stand_arr)
            self.sheet_number = 0

        """-------------------------------Other updates----------------------------------"""
        self.image = self.images[self.index]

        if self.direction < 0:
            self.image = pygame.transform.flip(self.image,True,False)

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
