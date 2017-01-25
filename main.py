import os
import pygame
from pygame import *

pygame.init()

scr_size = (width,height) = (600,400)
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
        self.images,self.rect = load_sprite_sheet('davis_0.bmp',10,7,-1,-1,-1)
        self.image = self.images[0]
        self.index = 0

        self.isWalking = False
        self.walk_arr = [4,5,6,7,6,5]
        self.walk_arr_index = 0
        self.walk_blit_rate = 3
        self.walk_speed = 3
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

def main():
    gameOver = False

    davis = Davis(20,50)
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

        davis.update()

        screen.fill(red)

        davis.draw()

        #screen.blit(sprites[7],sprite_rect)

        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()
    quit()

main()
