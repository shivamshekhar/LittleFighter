import os
import pygame
from pygame import *

pygame.init()

scr_size = (width,height) = (480,380)
FPS = 20
black = (0,0,0)
red = (255,0,0)

screen = pygame.display.set_mode(scr_size)
clock = pygame.time.Clock()

pygame.display.set_caption('Little Fighter')

def load_image(
    name,
    sizex=-1,
    sizey=-1,
    colorkey=None,
    ):

    fullname = os.path.join('sprites', name)
    image = pygame.image.load(fullname)
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, RLEACCEL)

    if sizex != -1 or sizey != -1:
        image = pygame.transform.scale(image, (sizex, sizey))

    return (image, image.get_rect())

def load_sprite_sheet(
        sheetname,
        nx,
        ny,
        scalex = -1,
        scaley = -1,
        colorkey = None,
        ):
    fullname = os.path.join('sprites',sheetname)
    sheet = pygame.image.load(fullname)
    sheet = sheet.convert()

    sheet_rect = sheet.get_rect()

    sprites = []

    sizex = sheet_rect.width/nx
    sizey = sheet_rect.height/ny

    for i in range(0,ny):
        for j in range(0,nx):
            rect = pygame.Rect((j*sizex,i*sizey,sizex,sizey))
            image = pygame.Surface(rect.size)
            image = image.convert()
            image.blit(sheet,(0,0),rect)

            if colorkey is not None:
                if colorkey is -1:
                    colorkey = image.get_at((0,0))
                image.set_colorkey(colorkey,RLEACCEL)

            if scalex != -1 or scaley != -1:
                image = pygame.transform.scale(image,(scalex,scaley))

            sprites.append(image)

    sprite_rect = sprites[0].get_rect()

    return sprites,sprite_rect

class Davis(pygame.sprite.Sprite):
    def __init__(self,x,y):
        self.images,self.rect = load_sprite_sheet('davis_0.bmp',10,7,70,70,-1)
        self.image = self.images[0]
        self.index = 0

        self.isWalking = False
        self.walk_arr = [4,5,6,7,6,5]
        self.walk_arr_index = 0
        self.walk_blit_rate = 3
        self.walk_speed = 5
        self.direction = 1

        self.stand_arr = [0,1,2,3,2,1]
        self.stand_arr_index = 0
        self.stand_blit_rate = 4

        self.movement = [0,0]

        self.rect.left = x
        self.rect.top = y

        self.counter = 0

    def draw(self):
        screen.blit(self.image,self.rect)

    def update(self):
        if self.isWalking:
            if self.counter%self.walk_blit_rate == 0:
                self.index = self.walk_arr[self.walk_arr_index]
                self.walk_arr_index = (self.walk_arr_index + 1)%6

            self.rect = self.rect.move(self.movement)

        else:
            if self.counter%self.stand_blit_rate == 0:
                self.index = self.stand_arr[self.stand_arr_index]
                self.stand_arr_index = (self.stand_arr_index + 1)%6

        self.image = self.images[self.index]
        if self.direction < 0:
            self.image = pygame.transform.flip(self.image,True,False)

        self.counter = (self.counter + 1)%10000000000


class Background(pygame.sprite.Sprite):
    def __init__(self,bgwidth,bgheight):
        pygame.sprite.Sprite.__init__(self)
        self.scroll = 0
        self.scrollspeed = [5,5]
        self.bgwidth = bgwidth
        self.bgheight = bgheight
        self.rightedge = width
        self.bottomedge = height
        self.fullterrain,self.fullterrainrect = load_image('bg1.jpg',int(bgwidth),int(bgheight))
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



def main():
    gameOver = False

    davis = Davis(20,50)
    bg = Background(725,380)
    #sprites,sprite_rect = load_sprite_sheet('davis_0.bmp',10,7,-1,-1,-1)

    while not gameOver:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    davis.movement[0] = -1*davis.walk_speed
                    davis.direction = -1
                    davis.isWalking = True

                if event.key == pygame.K_RIGHT:
                    davis.movement[0] = davis.walk_speed
                    davis.direction = 1
                    davis.isWalking = True

                if event.key == pygame.K_UP:
                    davis.movement[1] = -1*davis.walk_speed
                    davis.isWalking = True

                if event.key == pygame.K_DOWN:
                    davis.movement[1] = davis.walk_speed
                    davis.isWalking = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    davis.movement = [0,0]
                    davis.isWalking = False

        if davis.isWalking == True and davis.direction == 1 and davis.rect.right > width*9/10:
            bg.scroll = 1
        elif davis.isWalking == True and davis.direction == -1 and davis.rect.left < width*1/10:
            bg.scroll = -1
        else:
            bg.scroll = 0


        if bg.scroll != 0 and (bg.rightedge < bg.bgwidth - bg.scrollspeed[0] - 1 or bg.rightedge < width + 1):
            davis.movement[0] = 0


        bg.update()
        davis.update()

        screen.fill(red)
        bg.draw()
        davis.draw()

        #screen.blit(sprites[7],sprite_rect)
        #print (bg.bgwidth,bg.bgheight), bg.rightedge
        print bg.scroll,davis.movement
        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()
    quit()

main()
