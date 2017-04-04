import pygame
from constants import *
from functions import *

class Background(pygame.sprite.Sprite):
    def __init__(self,bgwidth,bgheight,bgname):
        pygame.sprite.Sprite.__init__(self)
        self.scroll = 0
        self.scrollspeed = [5,5]
        self.bgwidth = bgwidth
        self.bgheight = bgheight
        self.rightedge = width
        self.bottomedge = height
        self.fullterrain,self.fullterrainrect = load_image(bgname,int(bgwidth),int(bgheight))
        self.fullterrainrect.left = 0
        self.fullterrainrect.top = 0
        self.fullterrainrect.width = width
        self.fullterrainrect.height = height
        self.image = pygame.Surface((width,height))
        self.rect = pygame.Rect((0, 0, width, height))

        self.image.blit(self.fullterrain,self.rect,self.fullterrainrect)
        #colorkey = self.image.get_at((0,0))
        #self.image.set_colorkey(colorkey,RLEACCEL)
        #self.image = self.image.convert_alpha()

    def update(self):
        if self.scroll == 1 and self.rightedge <= self.bgwidth - self.scrollspeed[0]:
            self.rightedge += self.scrollspeed[0]
            self.fullterrainrect.left += self.scrollspeed[0]

        elif self.scroll == -1 and self.rightedge >= width + self.scrollspeed[0]:
            self.rightedge -= self.scrollspeed[0]
            self.fullterrainrect.left -= self.scrollspeed[0]

        elif self.scroll == 2 and self.bottomedge <= self.bgheight - self.scrollspeed[1]:
            self.bottomedge += self.scrollspeed[1]
            self.fullterrainrect.top += self.scrollspeed[1]

        elif self.scroll == -2 and self.bottomedge >= height + self.scrollspeed[1]:
            self.bottomedge -= self.scrollspeed[1]
            self.fullterrainrect.top -= self.scrollspeed[1]

        self.image = pygame.Surface((width,height))
        self.rect = pygame.Rect((0, 0, width, height))
        self.image.blit(self.fullterrain,self.rect,self.fullterrainrect)
        #colorkey = self.image.get_at((0,0))
        #self.image.set_colorkey(colorkey,RLEACCEL)
        #self.image = self.image.convert_alpha()

    def draw(self):
        screen.blit(self.image,self.rect)
