import os
import random
from pygame import mixer
import pygame

pygame.init()
pygame.display.set_caption('A játék elkezdődött')
size = 40
image_size = [50,50]
screen = pygame.display.set_mode((16*size, 9*size))

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


running = True
while running:

    screen.blit(Tiles["ut2"], (0,0,0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            exit()


    pygame.display.update()