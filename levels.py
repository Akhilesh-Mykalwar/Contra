import pygame
from tkinter import *
import button
import csv
import pickle
pygame.init()

clock = pygame.time.Clock()
FPS = 60
font = pygame.font.SysFont('Futura', 30)
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 640
level = 0
LOWER_MARGIN = 100
SIDE_MARGIN = 300

current_tile = 0
screen = pygame.display.set_mode((SCREEN_WIDTH + SIDE_MARGIN,SCREEN_HEIGHT + LOWER_MARGIN))
pygame.display.set_caption('Level Editor')


ROWS = 16
MAX_COLS = 150

tile = SCREEN_HEIGHT // ROWS
tile_types = 21
scroll_left = False
scroll_right = False
scroll = 0
scroll_speed = 1




pine1_img = pygame.image.load("C:\\Users\\Akhil\\OneDrive\\Desktop\\Contra Files\\background\\pine1.png").convert_alpha()
pine2_img = pygame.image.load("C:\\Users\\Akhil\\OneDrive\\Desktop\\Contra Files\\background\\pine2.png").convert_alpha()
mountain_img = pygame.image.load("C:\\Users\\Akhil\\OneDrive\\Desktop\\Contra Files\\background\\mountain.png").convert_alpha()
sky_img = pygame.image.load("C:\\Users\\Akhil\\OneDrive\\Desktop\\Contra Files\\background\\sky_cloud.png").convert_alpha()

img_list = []

for i in range(tile_types):
    img = pygame.image.load(f"C:\\Users\\Akhil\\OneDrive\\Desktop\\Contra Files\\tiles\\{i}.png")
    img = pygame.transform.scale(img, (tile,tile))
    img_list.append(img)
save_img = pygame.image.load("C:\\Users\\Akhil\\OneDrive\\Desktop\\Contra Files\\tiles\\save_btn.png").convert_alpha()
load_img = pygame.image.load("C:\\Users\\Akhil\\OneDrive\\Desktop\\Contra Files\\tiles\\load_btn.png").convert_alpha()

GREEN = (144,201,120)
WHITE = (255,255,255)
RED = (200,25,25)


world_data = []
for row in range(ROWS):

    r = [-1] * MAX_COLS
    world_data.append(r)

for Tile in range(0, MAX_COLS):
    world_data[ROWS - 1][Tile] = 0

def draw_text(text , font, text_col, x, y):
    img = font.render(text, True,text_col)
    screen.blit(img,(x,y))

def draw_bg():
    screen.fill(GREEN)
    width = sky_img.get_width()
    

    for x in range(10):

        
        screen.blit(sky_img, ((x * width) - scroll * 0.5, 0))
        screen.blit(mountain_img,((x * width) - scroll * 0.65, SCREEN_HEIGHT - mountain_img.get_height() - 300))
        screen.blit(pine1_img,((x * width) - scroll * 0.8, SCREEN_HEIGHT - pine1_img.get_height() - 150))
        screen.blit(pine2_img,((x * width) - scroll * 0.95, SCREEN_HEIGHT - pine2_img.get_height()))

def draw_grid():

    for c in range(MAX_COLS + 1):
        pygame.draw.line(screen, WHITE,(c * tile - scroll, 0),(c * tile - scroll, SCREEN_HEIGHT))


    for c in range(ROWS + 1):
        pygame.draw.line(screen, WHITE,(0,c * tile),(SCREEN_WIDTH, c * tile))



button_list = []
button_col = 0
button_row = 0
save_button = button.Button(SCREEN_WIDTH // 2, SCREEN_HEIGHT + LOWER_MARGIN - 50 , save_img, 1)
load_button = button.Button(SCREEN_WIDTH // 2 + 200, SCREEN_HEIGHT + LOWER_MARGIN - 50 , load_img, 1)

for i in range(len(img_list)):
    
    tile_button = button.Button(SCREEN_WIDTH + (75 * button_col) + 50, 75 * button_row + 50, img_list[i], 1) 
    button_list.append(tile_button)
    button_col += 1
    if button_col == 3:
        button_row += 1
        button_col = 0
def draw_world():
    for y, row in enumerate(world_data):
        for x,Tile in enumerate(row):
            if Tile >= 0:
                screen.blit(img_list[Tile],(x * tile - scroll,y * tile))
run = True

while run:

    clock.tick(FPS)

    draw_bg()

    draw_grid()

    draw_world()

    
    draw_text(f'Level : {level}',font,WHITE,10, SCREEN_HEIGHT + LOWER_MARGIN - 90)
    draw_text('Press UP or DOWN To Change Level',font,WHITE,10, SCREEN_HEIGHT + LOWER_MARGIN - 60)
    


    if save_button.draw(screen):

        with open(f'level{level}_data.csv','w', newline='') as csvfile:
            writer = csv.writer(csvfile , delimiter = ',')
            for row in world_data:
                writer.writerow(row)


    if load_button.draw(screen):

        scroll = 0
        with open(f'level{level}_data.csv', newline='') as csvfile:
            reader = csv.reader(csvfile , delimiter = ',')
            for x ,row in enumerate(reader):
                for y, Tile in enumerate(row):
                    world_data[x][y] = int(Tile)


    pygame.draw.rect(screen,GREEN,(SCREEN_WIDTH, 0,SIDE_MARGIN,SCREEN_HEIGHT))

    save_button.draw(screen)
    load_button.draw(screen)

    button_count = 0
    for button_count, i in enumerate(button_list):
        if i .draw(screen):
            current_tile = button_count
            
    pygame.draw.rect(screen, RED, button_list[current_tile].rect,3)



    if scroll_left == True and scroll > 0:
        scroll -= 5 * scroll_speed
    if scroll_right == True and scroll < (MAX_COLS * tile) - SCREEN_WIDTH:
        scroll += 5 * scroll_speed
    

    pos = pygame.mouse.get_pos()
    x = (pos[0] + scroll) // tile
    y = pos[1] // tile

    if pos[0] < SCREEN_WIDTH and pos[1] < SCREEN_HEIGHT:
        if pygame.mouse.get_pressed()[0] == True:
            if world_data[y][x] != current_tile:
                world_data[y][x] = current_tile

        if pygame.mouse.get_pressed()[2] == True:
            world_data[y][x] = -1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                scroll_left = True
            if event.key == pygame.K_d:
                scroll_right = True
            if event.key == pygame.K_LSHIFT:
                scroll_speed = 7
            if event.key == pygame.K_UP:
                level += 1
            if event.key == pygame.K_DOWN and level > 0:
                level -= 1

            

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                scroll_left = False
            if event.key == pygame.K_d:
                scroll_right = False
            if event.key == pygame.K_LSHIFT:
                scroll_speed = 1

 
    pygame.display.update()

pygame.quit()