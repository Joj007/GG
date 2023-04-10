import math, os, random, pygame, constants
import sys
import time
from pygame import mixer
import collections
import Score

pygame.init()
pygame.display.set_caption('Carcassone')


Sounds={
    "click": mixer.Sound('../Sounds/click.wav'),
    "wrong": mixer.Sound('../Sounds/wrong.wav')
}

theme = "Medieval"
music_path = f'../Music/{theme}/'
print()
Musics=[]
for music in os.listdir(music_path):
    Musics.append(mixer.Sound(f"{music_path}{music}"))


running = True
mode = "menu"
screen = pygame.display.set_mode((constants.SCREEN_SIZE_BASE*constants.TABLE_SIZE_X, constants.SCREEN_SIZE_BASE*constants.TABLE_SIZE_Y)) # Card sized screen
# screen = pygame.display.set_mode((1600, 900)) # Fix sized screen
# screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN) # Full screen mode

if screen.get_width()/constants.TABLE_SIZE_X > screen.get_height()/constants.TABLE_SIZE_Y:
    image_size = [screen.get_height()/constants.TABLE_SIZE_Y,screen.get_height()/constants.TABLE_SIZE_Y]
else:
    image_size = [screen.get_width()/constants.TABLE_SIZE_X, screen.get_width()/constants.TABLE_SIZE_X]

image_path = "../Images/Tiles"


def SaveCurrentCard():
    with open("../Save/CurrentCard", "w") as f:
        f.write(choosen_tile)

def SaveCurrentGame(placed_cards):
    EmptyFile("PrewGame")
    with open("../Save/PrewGame", "a") as f:
        for card in placed_cards:
            f.write(f"{card.sides};{str(card.pos_x)};{str(card.pos_y)};{card.rotation}\n")
    SavePack(Pack)
    SaveCurrentCard()

def SavePack(pack):
    EmptyFile("Pack")
    with open("../Save/Pack", "a") as f:
        for card in pack:
            f.write(f"{card}\n")



def ReadPrewGame():
    cards = []
    with open("../Save/PrewGame", "r") as f:
        for card in f.readlines():
            if card == "\n":
                continue
            card_list = card.split(";")
            card_list[-1] = int(card_list[-1].rstrip())
            if len(card_list[1]) > 2 and card_list[1][-2] == ".":
                card_list[1] = card_list[1][:-2]
                card_list[2] = card_list[2][:-2]
            rotation_copy = card_list[-1]
            image_name = card_list[0]
            if rotation_copy > 0:
                while rotation_copy != 0:
                    rotation_copy -= 90
                    image_name = f"{image_name[3]}{image_name[0]}{image_name[1]}{image_name[2]}{image_name[4]}"


            elif rotation_copy < 0:
                while rotation_copy != 0:
                    rotation_copy += 90
                    image_name = f"{image_name[1]}{image_name[2]}{image_name[3]}{image_name[0]}{image_name[4]}"


            cards.append(Card(pygame.transform.rotate(ImageLoader(image_name), card_list[-1]), int(card_list[1]), int(card_list[2]), card_list[0], card_list[3]))
    return cards

def ReadCurrentCard():
    with open("../Save/CurrentCard", "r") as f:
        card = f.read()
    return card

def ReadPack():
    pack = []
    with open("../Save/Pack", "r") as f:
        for card in f.readlines():
            pack.append(card.rstrip())
    return pack


def EmptyFile(file):
    with open(f"../Save/{file}", "w") as f:
        f.write("")

def ImageLoader(file_name):
    return pygame.transform.scale(pygame.image.load(f"{image_path}/{file_name}.png").convert_alpha(), image_size)

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

def Is_game_over(selected_card, placed_cards):
    if len(placed_cards)==constants.TABLE_SIZE_X*constants.TABLE_SIZE_Y:
        return True
    for x in range(constants.TABLE_SIZE_X):
        for y in range(constants.TABLE_SIZE_Y):
            if Placeable(Card(choosen_card, x, y, choosen_tile, 0), [x + 1, y + 1], cards) or Placeable(Card(choosen_card, x, y, f"{choosen_tile[1]}{choosen_tile[2]}{choosen_tile[3]}{choosen_tile[0]}{choosen_tile[4]}", 0), [x + 1, y + 1], cards)\
                    or Placeable(Card(choosen_card, x, y, f"{choosen_tile[2]}{choosen_tile[3]}{choosen_tile[0]}{choosen_tile[1]}{choosen_tile[4]}", 0), [x + 1, y + 1], cards) or Placeable(Card(choosen_card, x, y, f"{choosen_tile[3]}{choosen_tile[0]}{choosen_tile[1]}{choosen_tile[2]}{choosen_tile[4]}", 0), [x + 1, y + 1], cards):
                is_duplicate = False
                for card in cards:
                    if card.pos_x == x and card.pos_y == y:
                        is_duplicate = True
                if not is_duplicate:
                    return False
    return True

def WriteHighScore():
    with open("../Save/HighScores", "w") as f:
        f.write("")
    with open("../Save/HighScores", "a") as f:
        for score in Scores.items():
            f.write(f"{score[0][-3:]};{score[1]}\n")

def Create_pack():
    All_tiles = ["mmmmk", "mmumk", "mmuu_", "mumu_", "muuu_", "mvmvc", "mvmvv", "uuuu_", "vmmm_", "vmuu_", "vmvm_",
                 "vumu_", "vuum_", "vuuu_", "vvmm_", "vvmmc", "vvmmv", "vvmvc", "vvmvv", "vvuu_", "vvuuc", "vvuvc",
                 "vvuvv", "vvvvc", "mmmm_"]
    Road_tiles = ["mmumk", "mmuu_", "mumu_", "muuu_", "uuuu_", "vmuu_", "vumu_", "vuum_", "vuuu_", "vvuu_", "vvuuc",
                  "vvuvc", "vvuvv"]
    City_tiles = ["mvmvc", "mvmvv", "vmmm_", "vmuu_", "vmvm_", "vumu_", "vuum_", "vuuu_", "vvmm_", "vvmmc", "vvmmv",
                  "vvmvc", "vvmvv", "vvuu_", "vvuuc", "vvuvc", "vvuvv", "vvvvc"]
    Plain_tiles = ["mmmm_"]
    Monastery_tiles = ["mmmmk", "mmumk"]

    Pack = [random.choice(Plain_tiles), random.choice(Monastery_tiles)]
    for _ in range(4):
        selected_road_tile = random.choice(Road_tiles)
        Pack.append(selected_road_tile)
        Road_tiles.remove(selected_road_tile)

        selected_city_tile = random.choice(City_tiles)
        Pack.append(selected_city_tile)
        City_tiles.remove(selected_city_tile)

    for _ in range(70):
        Pack.append(random.choice(All_tiles))

    return Pack

def MusicKeyHandler(event, choosen_music):
    if event.key == pygame.K_KP_PLUS:
        choosen_music.set_volume(choosen_music.get_volume() + 0.1)
    elif event.key == pygame.K_KP_MINUS:
        choosen_music.set_volume(choosen_music.get_volume() - 0.1)
        if choosen_music.get_volume() < 0.11:
         choosen_music.set_volume(0)
    elif event.key == pygame.K_RETURN:
        choosen_music.stop()

if len(ReadPack()) == 0:
    Pack = Create_pack()
else:
    Pack = ReadPack()








Backgrounds = {
    "bg_wide": pygame.transform.scale(pygame.image.load(f"{image_path}/../Backgrounds/carcassonneBG1.jfif").convert_alpha(), (screen.get_width(), screen.get_height())),
    "bg_tall": pygame.transform.scale(pygame.image.load(f"{image_path}/../Backgrounds/carcassonneBG2.webp").convert_alpha(), (screen.get_width(), screen.get_height())),
    "bg_square": pygame.transform.scale(pygame.image.load(f"{image_path}/../Backgrounds/carcassonneBG3.jpg").convert_alpha(), (screen.get_width(), screen.get_height())),
    "bg_game": pygame.transform.scale(pygame.image.load(f"{image_path}/../Backgrounds/gameBG.jpg").convert_alpha(), (screen.get_height() if screen.get_height() > screen.get_width() else screen.get_width(), screen.get_height() if screen.get_height() > screen.get_width() else screen.get_width())),
    "icon": pygame.image.load('../Images/Backgrounds/Logo.webp'),
    "title": pygame.transform.scale(pygame.image.load('../Images/Backgrounds/Title.png'), (screen.get_width()/1.2, screen.get_width()/1.2/4)),
    "bg_menu": pygame.transform.scale(pygame.image.load(f"{image_path}/../Backgrounds/MenuHatter.png").convert_alpha(), (screen.get_height(), screen.get_height())),
}

title_rect = Backgrounds['title'].get_rect(midtop=(screen.get_width()/2, 20))

pygame.display.set_icon(Backgrounds['icon'])

menu_background = Backgrounds["bg_tall"]

if abs(screen.get_width()-screen.get_height()<30):
    menu_background = Backgrounds["bg_square"]
elif screen.get_width() > screen.get_height():
    menu_background = Backgrounds["bg_wide"]

class Card:
    def __init__(self, image, x, y, name, rotation):
        self.image = image
        self.pos = self.pos_x, self.pos_y = x, y
        self.sides = name
        self.rotation = rotation

    def draw(self):
        screen.blit(self.image, (self.pos_x*image_size[0], self.pos_y*image_size[1]))


class Key:
    new_name = "___"

    def __init__(self, letter, pos_x, pos_y, width, height):
        self.letter = letter
        self.pos = self.pos_x, self.pos_y = pos_x, pos_y
        self.width = width
        self.height = height
        self.font = pygame.font.Font('freesansbold.ttf', int(width/2))
        self.text = self.font.render(letter.upper(), True, (255, 255, 255))
        self.textRect = self.text.get_rect(center=(self.pos_x+self.width/2, self.pos_y+self.height/2))

    def draw(self):
        pygame.draw.rect(screen, (0,0,100), (self.pos_x, self.pos_y, self.width, self.height), 0, 50)
        screen.blit(self.text, self.textRect)

    def click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = mouse_pos_x, mouse_pos_y = pygame.mouse.get_pos()
            distance = abs(math.sqrt((mouse_pos_x-self.pos_x-self.width/2)**2 + (mouse_pos_y-self.pos_y-self.height/2)**2))
            if distance < self.width/2:
                Key.new_name += self.letter
                Sounds['click'].play()


Scores = dict()
with open("../Save/HighScores", "r") as f:
    for line in f:
        line = line.split("\n")
        for element in line:
            if element == "":
                continue
            Scores[element.split(";")[0]] = int(element.split(";")[1])


class CenterRectButton:
    def __init__(self, width, height, pos_y, color=(100,100,100), text="Start", text_size=36):
        self.width = width
        self.act_width = screen.get_width()*self.width/100
        self.height = height
        self.act_height = screen.get_height()*self.height/100
        self.pos_y = pos_y
        self.color = color
        self.to_game = False
        self.to_exit = False
        self.to_leaderboard = False
        self.font = pygame.font.Font('freesansbold.ttf', text_size)
        self.original_text = text
        self.text = self.font.render(text.upper(), True, (255, 255, 255))
        self.textRect = self.text.get_rect(center=(screen.get_width()/2,self.pos_y+self.act_height/2))

    def draw(self):
        pygame.draw.rect(screen, self.color, ((screen.get_width()-self.act_width)/2, self.pos_y, self.act_width, self.act_height), 0, 50)
        screen.blit(self.text, self.textRect)

    def click(self, event):
        mouse_pos = mouse_pos_x, mouse_pos_y = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN and (screen.get_width()-self.act_width)/2 < mouse_pos_x < (screen.get_width()-self.act_width)/2+self.act_width and self.pos_y < mouse_pos_y < self.pos_y + self.act_height:
            if self.original_text == "START":
                self.to_game = True
            elif self.original_text == "LEADERBOARD":
                self.to_leaderboard = True
            elif self.original_text == "EXIT":
                self.to_exit = True
            Sounds['click'].play()


cards = ReadPrewGame()


keys = []

letters = [["1","2","3","4","5","6","7","8","9","0"], ["q","w","e","r","t","y","u","i","o","p"], ["a","s","d","f","g","h","j","k","l","-"], ["z","x","c","v","b","n","m","_","@","."]]
eltolas_x = 10
eltolas_y = 10
hossz = screen.get_width()/len(letters[0]) - eltolas_x
magassag = hossz

for line, line_index in zip(letters, range(len(letters))):
    for letter, letter_index in zip(line, range(len(line))):
        keys.append(Key(letter, eltolas_x/2+letter_index*(hossz+eltolas_x), eltolas_y+line_index*(hossz+eltolas_y)+(screen.get_height()-len(letters)*(magassag+eltolas_y)-eltolas_y), hossz, magassag))


buttons = [CenterRectButton(70, 10, 350, (124, 101, 66), "START"), CenterRectButton(70, 10, 450, (124, 101, 66), "LEADERBOARD"), CenterRectButton(70, 10, 550, (124, 101, 66), "EXIT")]
if ReadCurrentCard() != "":
    choosen_tile = ReadCurrentCard()
else:
    choosen_tile = random.choice(Pack)
choosen_card = ImageLoader(choosen_tile)
Pack.remove(choosen_tile)

transparent_square = pygame.Surface(image_size)
transparent_square.set_alpha(128)
transparent_square.fill((0,0,0,128))

rotation = 0
random_music_number = random.randint(0, len(Musics) - 1)
choosen_music = Musics[random_music_number]
choosen_music.play()
choosen_music.set_volume(0.5)
while running:
    if not mixer.get_busy():
        random_music_number += 1
        if random_music_number == len(Musics):
            random_music_number = 0
        choosen_music = Musics[random_music_number]
        choosen_music.play()
    if mode == "game":
        bg_rect = Backgrounds["bg_game"].get_rect()
        bg_rect.center = (screen.get_width()/2,screen.get_height()/2)
        screen.blit(Backgrounds["bg_game"], bg_rect)

        for card in cards:
            card.draw()


        if len(cards) == constants.TABLE_SIZE_X * constants.TABLE_SIZE_Y:
            mode = "save"


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                exit()

            elif event.type == pygame.KEYDOWN:
                MusicKeyHandler(event, choosen_music)
                if event.key == pygame.K_ESCAPE:
                    mode = "menu"


            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                is_duplicate = False

                for card in cards:
                    if card.pos_x == grid_x and card.pos_y == grid_y:
                        is_duplicate = True

                if grid_x + 1 <= constants.TABLE_SIZE_X and grid_y + 1 <= constants.TABLE_SIZE_Y and not is_duplicate and Placeable(Card(choosen_card, grid_x, grid_y, choosen_tile, rotation), [grid_x + 1, grid_y + 1], cards):
                    cards.append(Card(choosen_card, grid_x, grid_y, choosen_tile, rotation))
                    rotation = 0
                    choosen_tile = random.choice(Pack)
                    choosen_card = ImageLoader(choosen_tile)
                    Pack.remove(choosen_tile)
                    if Is_game_over(Card(choosen_card, grid_x, grid_y, choosen_tile, rotation), cards):
                        mode = "save"
                        Pack = Create_pack()
                        EmptyFile("Pack")
                        EmptyFile("PrewGame")
                        EmptyFile("CurrentCard")
                    SaveCurrentGame(cards)
                    Sounds['click'].play()
                else:
                    Sounds['wrong'].play()

            elif event.type == pygame.MOUSEWHEEL:
                if event.y == 1:
                    choosen_card = pygame.transform.rotate(choosen_card, 90)
                    choosen_tile = f"{choosen_tile[1]}{choosen_tile[2]}{choosen_tile[3]}{choosen_tile[0]}{choosen_tile[4]}"
                    rotation += 90
                elif event.y == -1:
                    choosen_card = pygame.transform.rotate(choosen_card, -90)
                    choosen_tile = f"{choosen_tile[3]}{choosen_tile[0]}{choosen_tile[1]}{choosen_tile[2]}{choosen_tile[4]}"
                    rotation -= 90

        pos = pygame.mouse.get_pos()
        grid = grid_x, grid_y = pos[0] // image_size[0], pos[1] // image_size[0]
        screen.blit(choosen_card, (grid_x*image_size[0],grid_y*image_size[1]))
        screen.blit(transparent_square, (grid_x*image_size[0],grid_y*image_size[1]))






    elif mode == "menu":
        bg_rect = Backgrounds["bg_menu"].get_rect()
        bg_rect.center = (screen.get_width() / 2, screen.get_height() / 2)
        screen.blit(Backgrounds["bg_menu"], bg_rect)


        screen.blit(Backgrounds["title"], title_rect)

        for button in buttons:
            button.draw()

        for event in pygame.event.get():

            for button in buttons:
                button.click(event)
                if button.to_game:
                    Key.new_name = "___"
                    mode = "game"
                    button.to_game = False
                    if Is_game_over(Card(choosen_card, 0, 0, choosen_tile, rotation), cards):
                        mode = "save"
                        Pack = Create_pack()
                        EmptyFile("Pack")
                        EmptyFile("PrewGame")
                        EmptyFile("CurrentCard")
                elif button.to_leaderboard:
                    mode = "leaderboard"
                    button.to_leaderboard = False
                elif button.to_exit:
                    sys.exit()

            if event.type == pygame.QUIT:
                running = False
                exit()

            elif event.type == pygame.KEYDOWN:
                MusicKeyHandler(event, choosen_music)






    elif mode == "save":

        color = (255, 255, 255)
        font = pygame.font.Font('freesansbold.ttf', 30)
        for event in pygame.event.get():

            screen.fill((30,30,30))

            screen.blit(font.render(Key.new_name[-3:], True, color), font.render(Key.new_name[-3:], True, color).get_rect(topleft=(screen.get_width() / 2 - 125, 500)))
            screen.blit(font.render(str(Score.Score(cards)), True, color),font.render(str(Score.Score(cards)), True, color).get_rect(topright=(screen.get_width() / 2 + 125, 500)))


            dict_y = 10
            Scores = dict(sorted(Scores.items(), key=lambda x: x[1], reverse=True))



            for score in Scores.keys():
                font_place = font.render(str((dict_y - 10) / 40 + 1)[:-1], True, color)
                font_place_rect = font_place.get_rect(topleft=(10, dict_y))

                font_name = font.render(score[-3:], True, color)
                font_name_rect = font_name.get_rect(topleft=(screen.get_width() / 2 - 125, dict_y))

                font_point = font.render(str(Scores[score]), True, color)
                font_point_rect = font_point.get_rect(topright=(screen.get_width() / 2 + 125, dict_y))

                screen.blit(font_place, font_place_rect)
                screen.blit(font_name, font_name_rect)
                screen.blit(font_point, font_point_rect)
                dict_y += 40
                if (dict_y-10)/40 > 9:
                    break

            for key in keys:
                key.draw()
                key.click(event)

            if event.type == pygame.QUIT:
                running = False
                exit()

            elif event.type == pygame.KEYDOWN:
                MusicKeyHandler(event, choosen_music)

        if len(Key.new_name) > 5:
            if Key.new_name[-3:] in [x[-3:] for x in Scores.keys()]:
                if Scores[Key.new_name[-3:]] < Score.Score(cards):
                    Scores[Key.new_name[-3:]] = Score.Score(cards)
                    WriteHighScore()
                    mode = "menu"
                    cards = []
                else:
                    Key.new_name = "___"
            else:
                Scores[Key.new_name[-3:]] = Score.Score(cards)
                WriteHighScore()
                mode = "menu"
                cards = []

    elif mode == "leaderboard":


        for event in pygame.event.get():

            screen.fill((30,30,30))


            dict_y = 10
            Scores = dict(sorted(Scores.items(), key=lambda x: x[1], reverse=True))

            color = (255, 255, 255)
            font = pygame.font.Font('freesansbold.ttf', 30)
            for score in Scores.keys():
                font_place = font.render(str((dict_y-10)/40+1)[:-1], True, color)
                font_place_rect = font_place.get_rect(topleft=(10, dict_y))

                font_name = font.render(score[-3:], True, color)
                font_name_rect = font_name.get_rect(topleft=(screen.get_width() / 2 - 125, dict_y))

                font_point = font.render(str(Scores[score]), True, color)
                font_point_rect = font_point.get_rect(topright=(screen.get_width() / 2 + 125, dict_y))


                screen.blit(font_place, font_place_rect)
                screen.blit(font_name, font_name_rect)
                screen.blit(font_point, font_point_rect)

                dict_y += 40
                if (dict_y-10)/40 > 20:
                    break


            if event.type == pygame.QUIT:
                running = False
                exit()

            elif event.type == pygame.KEYDOWN:
                MusicKeyHandler(event, choosen_music)
                if event.key == pygame.K_ESCAPE:
                    mode = "menu"

        if len(Key.new_name) > 5:
            if Key.new_name[-3:] in [x[-3:] for x in Scores.keys()]:
                if Scores[Key.new_name[-3:]] < Score.Score(cards):
                    Scores[Key.new_name[-3:]] = Score.Score(cards)
                    WriteHighScore()
                    mode = "menu"
                    cards = []
                else:
                    Key.new_name = "___"
            else:
                Scores[Key.new_name[-3:]] = Score.Score(cards)
                WriteHighScore()
                mode = "menu"
                cards = []






    pygame.display.update()
