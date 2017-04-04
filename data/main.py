import pygame
from pygame import *
from constants import *
from davis import *
from functions import *
from background import *
from energybar import *


def main():
    gameOver = False

    davis = Davis(width/2,height/2)
    bg = Background(2900,380,'bg2.png')
    EB = EnergyBar(width/48,height/38,davis.mana,width/48)

    #sprites,sprite_rect = load_sprite_sheet('davis_0.bmp',10,7,-1,-1,-1)
    fireBlast = pygame.sprite.Group()

    DavisBall.containers = fireBlast

    while not gameOver:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameOver = True

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

                if event.key == pygame.K_a:
                    davis.isPunching = True

                if event.key == pygame.K_s:
                    davis.isFiringBlast = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    davis.movement = [0,0]
                    davis.isWalking = False

                if event.key == pygame.K_a:
                    davis.isPunching = False
                    davis.punch_arr_index = 1

                if event.key == pygame.K_s:
                    davis.isFiringBlast = False
                    davis.firingBlast_arr_index = 3

        if davis.isWalking == True and davis.direction == 1 and davis.rect.right > width*9/10:
            bg.scroll = 1
        elif davis.isWalking == True and davis.direction == -1 and davis.rect.left < width*1/10:
            bg.scroll = -1
        else:
            bg.scroll = 0


        if bg.scroll != 0 and ((bg.rightedge < bg.bgwidth - bg.scrollspeed[0] and davis.direction == 1) or (bg.rightedge > width + bg.scrollspeed[0] and davis.direction == -1)):
            davis.movement[0] = 0

        elif davis.isWalking == True and davis.movement == [0,0]:
            davis.movement[0] = davis.direction*davis.walk_speed


        bg.update()
        davis.update()
        fireBlast.update()
        EB.update(davis.mana)

        screen.fill(red)
        bg.draw()
        EB.draw()
        davis.draw()
        fireBlast.draw(screen)

        #screen.blit(sprites[7],sprite_rect)
        #print (bg.bgwidth,bg.bgheight), bg.rightedge
        print bg.scroll,davis.movement
        pygame.display.update()
        clock.tick(FPS)
