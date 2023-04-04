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


def Placeable(selected_card, location, placed_cards):  # selected_card egy card class, a location egy számpár [2, 3], a placed_cards pedig egy lista a lerakott kártya classekkel
    location = [int(location[1]-1), int(location[0]-1)]
    matrix = []
    temp_row = []
    is_connected = False

    for x in range(8):
        for y in range(5):
            temp_row.append(" ")
        matrix.append(temp_row)
        temp_row = []

    if len(placed_cards) > 0:
        for card in placed_cards:
            matrix[int(card.pos_y)][int(card.pos_x)] = card

        #megvizsgálja, hogy csatlakozik-e
        if (location[0] - 1 >= 0 and matrix[location[0] - 1][location[1]] != " ") or \
                (location[1] + 1 <= 4 and matrix[location[0]][location[1] + 1] != " ") or \
                (location[0] + 1 <= 7 and matrix[location[0] + 1][location[1]] != " ") or \
                (location[1] - 1 >= 0 and matrix[location[0]][location[1] - 1] != " "):

            #megvizsgálja mind a 4 oldalát a selected_cardnak
            if (location[0] - 1 < 0 or matrix[location[0] - 1][location[1]] == " " or selected_card.sides[0] == matrix[location[0] - 1][location[1]].sides[2]) and \
                    (location[1] + 1 > 4 or matrix[location[0]][location[1] + 1] == " " or selected_card.sides[1] == matrix[location[0]][location[1] + 1].sides[3]) and \
                    (location[0] + 1 > 7 or matrix[location[0] + 1][location[1]] == " " or selected_card.sides[2] == matrix[location[0] + 1][location[1]].sides[0]) and \
                    (location[1] - 1 < 0 or matrix[location[0]][location[1] - 1] == " " or selected_card.sides[3] == matrix[location[0]][location[1] - 1].sides[1]):
                return True
            else:
                return False
        else:
            return False
    else:
        return True





Tiles = ["varos1", "varos2", "varos3", "varos4", "varos5", "varos6", "varos7", "varos8", "varos9", "varos10", "varos11", "varos12", "keresztezodes3", "keresztezodes4", "keresztezodes32", "kolostor1", "kolostor2", "ut1", "ut2", "ut3", "ut4", "ut5", "ut6", "ut7"]
Backgrounds = {
    "bg_wide": pygame.transform.scale(pygame.image.load(f"{path}/../Backgrounds/carcassonneBG1.jfif").convert_alpha(), (screen.get_width(), screen.get_height())),
    "bg_tall": pygame.transform.scale(pygame.image.load(f"{path}/../Backgrounds/carcassonneBG2.webp").convert_alpha(), (screen.get_width(), screen.get_height())),
    "bg_square": pygame.transform.scale(pygame.image.load(f"{path}/../Backgrounds/carcassonneBG3.jpg").convert_alpha(), (screen.get_width(), screen.get_height())),
    "bg_game": pygame.transform.scale(pygame.image.load(f"{path}/../Backgrounds/gameBG.jpg").convert_alpha(), (screen.get_height() if screen.get_height() > screen.get_width() else screen.get_width(), screen.get_height() if screen.get_height() > screen.get_width() else screen.get_width())),
    "icon": pygame.image.load('../Images/Backgrounds/Logo.webp'),
    "title": pygame.transform.scale(pygame.image.load('../Images/Backgrounds/Title.png'), (screen.get_width()/1.2, screen.get_width()/1.2/4)),
}

title_rect = Backgrounds['title'].get_rect(midtop=(screen.get_width()/2, 20))

pygame.display.set_icon(Backgrounds['icon'])

menu_background = Backgrounds["bg_tall"]

if abs(screen.get_width()-screen.get_height()<30):
    menu_background = Backgrounds["bg_square"]
elif screen.get_width() > screen.get_height():
    menu_background = Backgrounds["bg_wide"]

class Card:
    def __init__(self, image, x, y):
        self.image = image
        self.pos = self.pos_x, self.pos_y = x, y
        self.sides = 'vmvmm'

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

class CenterRectButton:
    def __init__(self, width, height, pos_y, color=(100,100,100), functions=[], is_start=False, text="Start", text_size=36):
        self.width = width
        self.act_width = screen.get_width()*self.width/100
        self.height = height
        self.act_height = screen.get_height()*self.height/100
        self.pos_y = pos_y
        self.color = color
        self.functions = functions
        self.is_start_button = is_start
        self.to_game = False
        self.font = pygame.font.Font('freesansbold.ttf', text_size)
        self.text = self.font.render(text.upper(), True, (255, 255, 255))
        self.textRect = self.text.get_rect(center=(self.act_width,self.pos_y+self.act_height/2))

    def draw(self):
        pygame.draw.rect(screen, self.color, (self.act_width/2, self.pos_y, self.act_width, self.act_height), 0, 50)
        screen.blit(self.text, self.textRect)

    def click(self, event):
        mouse_pos = mouse_pos_x, mouse_pos_y = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN and self.act_width/2 < mouse_pos_x < self.act_width/2+self.act_width and self.pos_y < mouse_pos_y < self.pos_y + self.act_height:
            if not self.is_start_button:
                for index in range(len(self.functions)):
                    self.functions[index]()
            else:
                self.to_game = True


cards = []
buttons = [CenterRectButton(50, 10, 350, (100,0,200), [], True, "START"), CenterRectButton(50, 10, 450, (0,100,0), [], False, "SETTINGS"), CenterRectButton(50, 10, 550, (200,0,100), [], False, "EXIT")]
choosen_card = ImageLoader(random.choice(Tiles))

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

                if grid_x + 1 <= constants.TABLE_SIZE_X and grid_y + 1 <= constants.TABLE_SIZE_Y and not is_duplicate and Placeable(Card(choosen_card, grid_x, grid_y), [grid_x + 1, grid_y + 1], cards):
                    cards.append(Card(choosen_card, grid_x, grid_y))
                    choosen_card = ImageLoader(random.choice(Tiles))

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
        pygame.draw.rect(screen, (0,50,150) ,(0,0,screen.get_width(),screen.get_height()))
        screen.blit(Backgrounds["title"], title_rect)

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
