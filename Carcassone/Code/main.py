import os
import random
from pygame import mixer
import pygame
import constants

pygame.init()
pygame.display.set_caption('Carcassone')

screen = pygame.display.set_mode((constants.SCREEN_SIZE_BASE*constants.TABLE_SIZE_X, constants.SCREEN_SIZE_BASE*constants.TABLE_SIZE_Y)) # Card sized screen
# screen = pygame.display.set_mode((1600, 900)) # Fix sized screen
# screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN) # Full screen mode

if screen.get_width()/constants.TABLE_SIZE_X > screen.get_height()/constants.TABLE_SIZE_Y:
    image_size = [screen.get_height()/constants.TABLE_SIZE_Y,screen.get_height()/constants.TABLE_SIZE_Y]
else:
    image_size = [screen.get_width()/constants.TABLE_SIZE_X, screen.get_width()/constants.TABLE_SIZE_X]

path = "../Images/Tiles"
Tiles = {
    "varos1": pygame.transform.scale(pygame.image.load(f"{path}/varos1.png").convert_alpha(), image_size),
    "varos2": pygame.transform.scale(pygame.image.load(f"{path}/varos2.png").convert_alpha(), image_size),
    "varos3": pygame.transform.scale(pygame.image.load(f"{path}/varos3.png").convert_alpha(), image_size),
    "varos4": pygame.transform.scale(pygame.image.load(f"{path}/varos4.png").convert_alpha(), image_size),
    "varos5": pygame.transform.scale(pygame.image.load(f"{path}/varos5.png").convert_alpha(), image_size),
    "varos6": pygame.transform.scale(pygame.image.load(f"{path}/varos6.png").convert_alpha(), image_size),
    "varos7": pygame.transform.scale(pygame.image.load(f"{path}/varos7.png").convert_alpha(), image_size),
    "varos8": pygame.transform.scale(pygame.image.load(f"{path}/varos8.png").convert_alpha(), image_size),
    "varos9": pygame.transform.scale(pygame.image.load(f"{path}/varos9.png").convert_alpha(), image_size),
    "varos10": pygame.transform.scale(pygame.image.load(f"{path}/varos10.png").convert_alpha(), image_size),
    "varos11": pygame.transform.scale(pygame.image.load(f"{path}/varos11.png").convert_alpha(), image_size),
    "varos12": pygame.transform.scale(pygame.image.load(f"{path}/varos12.png").convert_alpha(), image_size),
    "keresztezodes3": pygame.transform.scale(pygame.image.load(f"{path}/keresztezodes3.png").convert_alpha(), image_size),
    "keresztezodes4": pygame.transform.scale(pygame.image.load(f"{path}/keresztezodes4.png").convert_alpha(), image_size),
    "keresztezodes32": pygame.transform.scale(pygame.image.load(f"{path}/keresztezodes32.png").convert_alpha(), image_size),
    "kolostor1": pygame.transform.scale(pygame.image.load(f"{path}/kolostor1.png").convert_alpha(), image_size),
    "kolostor2": pygame.transform.scale(pygame.image.load(f"{path}/kolostor2.png").convert_alpha(), image_size),
    "ut1": pygame.transform.scale(pygame.image.load(f"{path}/ut1.png").convert_alpha(), image_size),
    "ut2": pygame.transform.scale(pygame.image.load(f"{path}/ut2.png").convert_alpha(), image_size),
    "ut3": pygame.transform.scale(pygame.image.load(f"{path}/ut3.png").convert_alpha(), image_size),
    "ut4": pygame.transform.scale(pygame.image.load(f"{path}/ut4.png").convert_alpha(), image_size),
    "ut5": pygame.transform.scale(pygame.image.load(f"{path}/ut5.png").convert_alpha(), image_size),
    "ut6": pygame.transform.scale(pygame.image.load(f"{path}/ut6.png").convert_alpha(), image_size),
    "ut7": pygame.transform.scale(pygame.image.load(f"{path}/ut7.png").convert_alpha(), image_size),
}

class Card:
    def __init__(self, image, x, y):
        self.image = image
        self.pos = self.pos_x, self.pos_y = x, y

    def draw(self):
        screen.blit(self.image, (self.pos_x*image_size[0], self.pos_y*image_size[0]))



cards = []


running = True
while running:

    if len(cards) == constants.TABLE_SIZE_X * constants.TABLE_SIZE_Y:
        running = False

    for event in pygame.event.get():

        for card in cards:
            card.draw()

        if event.type == pygame.QUIT:
            running = False
            exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            grid = grid_x, grid_y = pos[0]//image_size[0], pos[1]//image_size[0]

            is_duplicate = False

            for card in cards:
                if card.pos_x == grid_x and card.pos_y == grid_y:
                    is_duplicate = True


            if grid_x + 1 <= constants.TABLE_SIZE_X and grid_y + 1 <= constants.TABLE_SIZE_Y and not is_duplicate:
                cards.append(Card(random.choice(list(Tiles.values())), grid_x, grid_y))



    pygame.display.update()
