import math, os, random, pygame, constants
from pygame import mixer

pygame.init()
pygame.display.set_caption('Carcassone')


running = True
mode = "menu"
screen = pygame.display.set_mode((constants.SCREEN_SIZE_BASE*constants.TABLE_SIZE_X, constants.SCREEN_SIZE_BASE*constants.TABLE_SIZE_Y)) # Card sized screen
# screen = pygame.display.set_mode((1600, 900)) # Fix sized screen
# screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN) # Full screen mode

if screen.get_width()/constants.TABLE_SIZE_X > screen.get_height()/constants.TABLE_SIZE_Y:
    image_size = [screen.get_height()/constants.TABLE_SIZE_Y,screen.get_height()/constants.TABLE_SIZE_Y]
else:
    image_size = [screen.get_width()/constants.TABLE_SIZE_X, screen.get_width()/constants.TABLE_SIZE_X]

path = "../Images/Tiles"

def ImageLoader(file_name):
    return pygame.transform.scale(pygame.image.load(f"{path}/{file_name}.png").convert_alpha(), image_size)

Tiles = {
    "varos1": ImageLoader("varos1"),
    "varos2": ImageLoader("varos2"),
    "varos3": ImageLoader("varos3"),
    "varos4": ImageLoader("varos4"),
    "varos5": ImageLoader("varos5"),
    "varos6": ImageLoader("varos6"),
    "varos7": ImageLoader("varos7"),
    "varos8": ImageLoader("varos8"),
    "varos9": ImageLoader("varos9"),
    "varos10": ImageLoader("varos10"),
    "varos11": ImageLoader("varos11"),
    "varos12": ImageLoader("varos12"),
    "keresztezodes3": ImageLoader("keresztezodes3"),
    "keresztezodes4": ImageLoader("keresztezodes4"),
    "keresztezodes32": ImageLoader("keresztezodes32"),
    "kolostor1": ImageLoader("kolostor1"),
    "kolostor2": ImageLoader("kolostor2"),
    "ut1": ImageLoader("ut1"),
    "ut2": ImageLoader("ut2"),
    "ut3": ImageLoader("ut3"),
    "ut4": ImageLoader("ut4"),
    "ut5": ImageLoader("ut5"),
    "ut6": ImageLoader("ut6"),
    "ut7": ImageLoader("ut7"),
}
Backgrounds = {
    "bg_wide": pygame.transform.scale(pygame.image.load(f"{path}/../Backgrounds/carcassonneBG1.jfif").convert_alpha(), (screen.get_width(), screen.get_height())),
    "bg_tall": pygame.transform.scale(pygame.image.load(f"{path}/../Backgrounds/carcassonneBG2.webp").convert_alpha(), (screen.get_width(), screen.get_height())),
    "bg_square": pygame.transform.scale(pygame.image.load(f"{path}/../Backgrounds/carcassonneBG3.jpg").convert_alpha(), (screen.get_width(), screen.get_height())),
    "bg_game": pygame.transform.scale(pygame.image.load(f"{path}/../Backgrounds/gameBG.jpg").convert_alpha(), (screen.get_height() if screen.get_height() > screen.get_width() else screen.get_width(), screen.get_height() if screen.get_height() > screen.get_width() else screen.get_width())),
}

menu_background = Backgrounds["bg_tall"]

if abs(screen.get_width()-screen.get_height()<30):
    menu_background = Backgrounds["bg_square"]
elif screen.get_width() > screen.get_height():
    menu_background = Backgrounds["bg_wide"]

class Card:
    def __init__(self, image, x, y):
        self.image = image
        self.pos = self.pos_x, self.pos_y = x, y

    def draw(self):
        screen.blit(self.image, (self.pos_x*image_size[0], self.pos_y*image_size[1]))


class ImageButton:
    def __init__(self, image, pos_x, pos_y):
        self.image = image
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.mode = "image"

    def draw(self):
        screen.blit(self.image, (self.pos_x, self.pos_y))

class RectButton:
    def __init__(self, width, height, pos_x, pos_y, color, functions, is_start):
        self.width = width
        self.height = height
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.color = color
        self.functions = functions
        self.is_start_button = is_start
        self.to_game = False

    def draw(self):
        pygame.draw.rect(screen, self.color, (self.pos_x, self.pos_y, self.width, self.height))

    def click(self, event):
        mouse_pos = mouse_pos_x, mouse_pos_y = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN and self.pos_x < mouse_pos_x < self.pos_x + self.width and self.pos_y < mouse_pos_y < self.pos_y + self.height:
            if not self.is_start_button:
                for index in range(len(self.functions)):
                    self.functions[index]()
            else:
                self.to_game = True

class CircleButton:
    def __init__(self, pos_x, pos_y, radius, color, is_start):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.radius = radius
        self.color = color
        self.is_start_button = is_start
        self.to_game = False
    def draw(self):
        pygame.draw.circle(screen, self.color, (self.pos_x, self.pos_y), self.radius)
    def click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = mouse_pos_x, mouse_pos_y = pygame.mouse.get_pos()
            distance = abs(math.sqrt((mouse_pos_x-self.pos_x)**2 + (mouse_pos_y-self.pos_y)**2))
            if distance < self.radius:
                print('O')



cards = []
buttons = [CircleButton(60,50, 40, (10,50,200), False), RectButton(150,50, 300, 200, (200,200,40), [], True)]
choosen_card = random.choice(list(Tiles.values()))

transparent_square = pygame.Surface(image_size)
transparent_square.set_alpha(128)
transparent_square.fill((0,0,0,128))

while running:
    if mode == "game":
        bg_rect = Backgrounds["bg_game"].get_rect()
        bg_rect.center = (screen.get_width()/2,screen.get_height()/2)
        screen.blit(Backgrounds["bg_game"], bg_rect)

        for card in cards:
            card.draw()

        if len(cards) == constants.TABLE_SIZE_X * constants.TABLE_SIZE_Y:
            running = False



        for event in pygame.event.get():




            if event.type == pygame.QUIT:
                running = False
                exit()


            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                is_duplicate = False

                for card in cards:
                    if card.pos_x == grid_x and card.pos_y == grid_y:
                        is_duplicate = True


                if grid_x + 1 <= constants.TABLE_SIZE_X and grid_y + 1 <= constants.TABLE_SIZE_Y and not is_duplicate:
                    cards.append(Card(choosen_card, grid_x, grid_y))
                    choosen_card = random.choice(list(Tiles.values()))

            elif event.type == pygame.MOUSEWHEEL:
                if event.y == 1:
                  choosen_card = pygame.transform.rotate(choosen_card, 90)
                elif event.y == -1:
                    choosen_card = pygame.transform.rotate(choosen_card, -90)

        pos = pygame.mouse.get_pos()
        grid = grid_x, grid_y = pos[0] // image_size[0], pos[1] // image_size[0]
        screen.blit(choosen_card, (grid_x*image_size[0],grid_y*image_size[1]))
        screen.blit(transparent_square, (grid_x*image_size[0],grid_y*image_size[1]))






    elif mode == "menu":
        screen.blit(menu_background, (0,0))

        for button in buttons:
            button.draw()

        for event in pygame.event.get():

            for button in buttons:
                button.click(event)
                if button.is_start_button and button.to_game:
                    mode = "game"
                    button.to_game = False

            if event.type == pygame.QUIT:
                running = False
                exit()


    pygame.display.update()
