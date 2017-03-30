import pygame
from constants import *

class EnergyBar():#pygame.sprite.Sprite):
    def __init__(self,posx,posy,width,height,orientation = "horizontal",color=(0,200,0)):
        #pygame.sprite.Sprite.__init__(self,self.containers)
        self.image = pygame.Surface((width,height))
        self.rect = self.image.get_rect()
        self.rect.left = posx
        self.rect.top = posy
        self.color = color
        self.width = width
        self.height = height
        self.posx = posx
        self.posy = posy
        self.orientation = orientation
        self.image.fill(color)

    def draw(self):
        screen.blit(self.image,self.rect)

    def update(self,update_quantity):
        if self.orientation == "horizontal":
            self.width = update_quantity
        else:
            self.height = update_quantity
        self.image = pygame.Surface((self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.left = self.posx
        self.rect.top = self.posy
        self.image.fill(self.color)

