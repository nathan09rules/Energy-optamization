import pygame
from func.final import *
import copy
import numpy as np
import random as rd

pygame.init()

fail = loc([[0,0]],0,0,0,"FROM")
fail2 = loc([[0,0]],0,0,0,"TO")

WIDTH , HEIGHT = 1000,600
t_WIDTH , t_HEIGHT = 700 , 600
border_size = 10
grid_size = 20
line_width = 8
el_speed = 1
num = 0
current_loc = 0
E_C = False
current_mouse_tab1e = [0,0]
current_page = [0 , fail , fail2]

WHITE = (255,255,255)
BLACK = (0,0,0)
BLUE = (80,80,200)
YELLOW = (225,225,40)
GREEN = (118, 190, 88)
GRAY = (200 , 200 , 200)
DARK_GRAY = (220 , 220 , 220)
RED = (255 , 0 , 0)
LIGHT_BLUE = ( 20 , 20 , 200)
BLOCK_NUM = 10
BLOCK_COLOUR = (200,80,80)

vibrant_colors = [
    (255, 99, 71),    # Tomato Red
    (135, 206, 250),  # Sky Blue
    (255, 165, 0),    # Bright Orange
    (255, 215, 0),    # Gold
    (186, 85, 211),   # Medium Orchid
    (60, 179, 113),   # Medium Sea Green
    (240, 128, 128),  # Light Coral
    (30, 144, 255),   # Dodger Blue
    (221, 160, 221),  # Plum
    (255, 140, 0),    # Dark Orange
    (127, 255, 0),    # Chartreuse
    (218, 112, 214),  # Orchid
    (0, 255, 255),    # Cyan
    (0, 128, 128),    # Teal
    (255, 69, 0),     # Red-Orange
    (173, 216, 230),  # Light Blue
]

COLOURS = {
    "BROWN" : (215 , 124 , 104),
    "WHITE" : (255 , 255 , 255),
    "BLUE"  : (73 , 143 , 192),
    "RED"   : (192 , 73 , 73),
    "LIGHT_BROWN" : (209 , 188 , 123),
    "DARK_BLUE" : (57 ,  116 , 158),
}

all_click_p = []
COLOUR_RANGE = [(0,0,0),(21,48,65),(33,75,95),(108,80,76),(225,119,57),(225,203,104),(225,225,225)] #30 is reserved

num_1 , num_2 , num_3 , num_4= True , True , False , False #ui True is up

sub_width , sub_height = t_WIDTH-2*border_size,t_HEIGHT-2*border_size

debug_menu = False
#setting things up
pygame.display.set_caption("Lighting test")
screen = pygame.display.set_mode((WIDTH,HEIGHT))
screen.fill(BLUE)

draw = False

clock = pygame.time.Clock()

COLOUR_LEN = len(COLOUR_RANGE)-1

table_width ,table_height = sub_width//grid_size , sub_height//grid_size
table = [[0 for x in range(table_width )] for y in range(table_height )]

#functions to use
def event_check():
    global num , num_1 , num_2 , num_3 ,num_4 , current_mouse_tab1e , all_click_p

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN :
            global num_2 , num_1 , debug_menu
            if event.key == pygame.K_k:
                pygame.quit()
                exit()
            elif event.key == pygame.K_f:
                debug_menu = not(debug_menu)
                if debug_menu==True:
                    frame_rate()
                else:
                    draw_grid()
            elif event.key == pygame.K_4:
                num_4 = not(num_4)
            elif event.key == pygame.K_3:
                num_3 = not(num_3)
            elif event.key == pygame.K_2:
                num_2 = not(num_2)
            elif event.key == pygame.K_1:
                num_1 = not(num_1)
            elif event.key == pygame.K_DELETE:
                all_click_p.pop()
            
            elif event.key == pygame.K_n:
                if num <= len(ENERGY_BOOK) -1:
                    Read_BOOK(ENERGY_BOOK , num , start_all_loc)
                    num += 1
            elif event.key == pygame.K_b:
                if num > 0:
                    Back_BOOk(ENERGY_BOOK , num , start_all_loc)
                    num -= 1
        if event.type == pygame.MOUSEBUTTONDOWN:
            x , y = pygame.mouse.get_pos()
            if num_2 == True:
                ui_clicked([x ,y] , start_all_loc ) #issue with how the code is made to deep to fix
            elif num_2 == False:
                start = get_table_from_poi([x, y])
                make_new_loc([x,y],all_loc)
                ptable(ENERGY_BOOK)
            if num_3 == True:
                poi = get_table_from_poi([x, y])
                poi = [poi[1],poi[0]]
                for l in start_all_loc:
                    for p in l.poi:
                        if p == poi:
                            draw_new_line(start_all_loc , all_lines , [x,y])
                            break
            elif num_4 == True:
                p = [y , x]
                p = get_table_from_poi(p)
                all_click_p.append(p)

            
            current_mouse_tab1e = get_table_from_poi([x,y])
    if debug_menu==True:
        frame_rate()

def write(string : str ,size : int, x : int , y : int):
    font = pygame.font.Font(pygame.font.get_default_font(), size)  # Use default font with size 
    text_surface = font.render(string, True, BLACK)  # Text is black and antialiased
    screen.blit(text_surface, (x - text_surface.get_width() // 2, y - text_surface.get_height() // 2))

def draw_grid():
    """
    for x in range(table_width):
        for y in range(table_height):
                value = table[y][x]
                if value == BLOCK_NUM:
                    pygame.draw.rect(screen,BLOCK_COLOUR,(x*grid_size + border_size,y * grid_size + border_size,grid_size,grid_size))
                    pass
                    print("done")
                else:
                    pygame.draw.rect(screen,COLOUR_RANGE[value],(x*grid_size + border_size,y * grid_size + border_size,grid_size,grid_size))
    """   
    for x in range(border_size ,t_WIDTH-border_size + grid_size,grid_size):
        pygame.draw.line(screen,COLOUR_RANGE[-1],(x,border_size),(x,t_HEIGHT-border_size))
    for y in range(border_size ,t_HEIGHT-border_size + grid_size,grid_size):
        pygame.draw.line(screen,COLOUR_RANGE[-1],(border_size,y),(t_WIDTH-border_size,y))

def frame_rate():
    pygame.draw.rect(screen,WHITE,(border_size,border_size,sub_width,25))
    write(str(clock),20,t_WIDTH//2,border_size+10)

def all_net(loc : [loc]):
    sum = 0
    for l in loc:
        sum += l.net()
    return sum

def ptable(table):
    for x in table:
        pass

def draw_grid_net(all_loc):
    pygame.draw.rect(screen,COLOUR_RANGE[0],(border_size,border_size,sub_width,sub_height))
    max_c = 20

    n_high = abs(max((-l.net) for l in all_loc) if all_loc else 1)
    c_high = max((l.store) for l in all_loc) if all_loc else 1
    n_ratio = 255 / n_high if n_high > 0 else 1
    c_ratio = 255 / c_high if c_high > 0 else 1

    for l in all_loc:
        RED, GREEN, BLUE = 0, 0, 0

        if l.net < 0:
            RED = -(l.net ) * n_ratio * 3
        else:
            GREEN = 112  # Green intensity is halved for balance

        if l.cap != 0:
            BLUE = l.store * c_ratio  //  2
        else:
            GREEN += 0  # Green intensity is shared with capacity

        RED = max(RED , max_c)
        GREEN = max(GREEN , max_c)
        BLUE = max(BLUE, max_c)

        RED = min(RED , 255)
        GREEN = min(GREEN , 255)
        BLUE = min(BLUE, 255)

        for poi in l.poi:
            pygame.draw.rect(
                screen,
                (RED, GREEN, BLUE),
                (
                    poi[1] * grid_size + border_size,
                    poi[0] * grid_size + border_size,
                    grid_size,
                    grid_size,
                ),
            )
        draw_grid()

def ui_write(string : str ,size : int, x : int , y : int):
    font = pygame.font.Font(pygame.font.get_default_font(), size)  # Use default font with size 
    text_surface = font.render(string, True, BLACK)  # Text is black and antialiased
    screen.blit(text_surface , (x , y) )

def display_ui(l , all_loc):
    global current_loc
    current_loc = l
    pygame.draw.rect(screen , WHITE , (t_WIDTH , border_size , (WIDTH - t_WIDTH) - border_size , HEIGHT - 2 * border_size))
    write(l.type , 30 , 850 , 30)
    ui_write((f" PRODUCTION "), 20 ,t_WIDTH + border_size , 60)
    ui_write((f": {l.prod}"), 21 ,t_WIDTH + border_size + 150 , 60)
    ui_write((f" DEMAND "), 20 ,t_WIDTH + border_size , 80)
    ui_write((f": {l.dem}"), 21 ,t_WIDTH + border_size + 150 , 80)
    ui_write((f" STORAGE"), 20 ,t_WIDTH + border_size , 100)
    ui_write((f": {l.store}"), 21 ,t_WIDTH + border_size + 150 , 100)
    ui_write((f" EXTERANAL"), 20 ,t_WIDTH + border_size , 120)
    ui_write((f": {l.net_ex}"), 21 ,t_WIDTH + border_size + 150 , 120)
    ui_write((f" NET"), 20 ,t_WIDTH + border_size , 140)
    ui_write((f": {l.net}"), 21 ,t_WIDTH + border_size + 150 , 140)
    ui_write((f" CAPACITY "), 20 ,t_WIDTH + border_size , 160)
    ui_write((f": {l.cap}"), 21 ,t_WIDTH + border_size + 150 , 160)
    poi = get_poi_from_table([35 , 15])
    if current_page[1] not in ["PASS","FAILED"]:
        ui_write(str(str(int(current_page[0])) + " " + current_page[1].type + " " + current_page[2].type) , 25 ,t_WIDTH + border_size, 200)
    else:
        if current_page[0] in ["PASS"]:
            ui_write(str(" ".join(current_page)) , 30 ,t_WIDTH + border_size, 200)
        else:
            ui_write(str(str(int(current_page[0])) + " ".join(current_page[1::])) , 30 ,t_WIDTH + border_size, 200)
    font = pygame.font.Font(pygame.font.get_default_font(), 20)  # Use default font with size 
    text_surface = font.render("PRODUCTION", True, BLACK)

    for p in l.poi:
        poi = get_poi_from_table(p)
        line = [[poi[1] - grid_size//2  , poi[0] - grid_size//2] , [poi[1] + grid_size//2,poi[0] - grid_size//2] , [poi[1] + grid_size//2 , poi[0] + grid_size//2] , [poi[1] - grid_size//2 , poi[0] + grid_size//2]]
        pygame.draw.lines(screen , RED , True , line)

    p = get_poi_from_table([36 , 25])
    p2= get_poi_from_table([41.5, 25])
    p3 = get_poi_from_table([47, 25])

    pygame.draw.circle(screen , BLACK ,  p , 15)
    pygame.draw.circle(screen , BLACK ,  p2, 15)
    pygame.draw.circle(screen , BLACK ,  p3, 15)

    if num_1 == False:
        pygame.draw.circle(screen , GREEN , p , 10)
    else:
        pygame.draw.circle(screen , RED , p , 10)
    if num_2 == False:
        p = get_poi_from_table([41.5, 25])
        pygame.draw.circle(screen , GREEN , p2, 10)
    else:
        pygame.draw.circle(screen , RED , p2, 10)
    if num_3 == True:
        pygame.draw.circle(screen , GREEN , p3, 10)
    else:
        pygame.draw.circle(screen , RED , p3, 10)

def get_table_from_poi(coordinates : tuple [int , int]) -> tuple [int , int]: #return in reverse order... and returns in form sent so switch in table
    return [(coordinates[0] - border_size) // grid_size , (coordinates[1] - border_size) // grid_size]

def get_poi_from_table(coordinates : tuple [int , int]) -> tuple [int , int]:
    return [border_size + coordinates[0] * grid_size + grid_size//2 , border_size + coordinates[1] * grid_size + grid_size//2]

def ui_clicked(mouse_poi , all_loc ) :
    x , y = get_table_from_poi(mouse_poi)
    for l in all_loc:
        for poi in l.poi:
            if [y , x] == poi:
                display_ui(l , all_loc)
                break

def make_new_loc(table_coords : tuple [int , int] , all_loc):
    table_coords = [table_coords[1] , table_coords[0]]

        
    for p in [table_coords]:
        p = get_table_from_poi(p)
        poi = get_poi_from_table(p)
        line = [[poi[1] - grid_size//2  , poi[0] - grid_size//2] , [poi[1] + grid_size//2,poi[0] - grid_size//2] , [poi[1] + grid_size//2 , poi[0] + grid_size//2] , [poi[1] - grid_size//2 , poi[0] + grid_size//2]]
        pygame.draw.lines(screen , RED , True , line)

    writing = True
    typed = ""
    loc_type , loc_prod , loc_dem , loc_store  = "" , "" , "" , ""
    data = [loc_type , loc_prod , loc_dem , loc_store  ]
    height = [30 , 60 , 80 , 100] # 1 - 3 are size 20
    currrent_write , colo , timer = 0 , ( 0 ,0 ,0) , 0
    while writing:
        clock.tick(20)
        pygame.draw.rect(screen , WHITE , (t_WIDTH , border_size , (WIDTH - t_WIDTH) - border_size , HEIGHT - 2 * border_size))
        write(data[0] ,  30 , 850 , 30)
        ui_write((f" PRODUCTION "), 20 ,t_WIDTH + border_size , 60)
        ui_write((f": {data[1]}"), 21 ,t_WIDTH + border_size + 150 , 60)
        ui_write((f" DEMAND "), 20 ,t_WIDTH + border_size , 80)
        ui_write((f": {data[2]}"), 21 ,t_WIDTH + border_size + 150 , 80)
        ui_write((f" STORAGE"), 20 ,t_WIDTH + border_size , 100)
        ui_write((f": {data[3]}"), 21 ,t_WIDTH + border_size + 150 , 100)

        if timer % 10 < 3:
            colo = (0 , 0 ,0)  # Text is black and antialiased
            if currrent_write == 0:
                font = pygame.font.Font(pygame.font.get_default_font(), 30)  # Use default font with size 
                text_surface = font.render(typed, True, BLACK)
                pygame.draw.rect(screen , colo , (t_WIDTH + (WIDTH - t_WIDTH)//2 - text_surface.get_width() // 2, 30 - text_surface.get_height() // 2 , max(30 ,text_surface.get_width()) , text_surface.get_height()))
            else:
                font = pygame.font.Font(pygame.font.get_default_font(), 20)  # Use default font with size 
                text_surface = font.render(typed, True, BLACK)
                pygame.draw.rect(screen , colo , ( t_WIDTH + 165 + border_size , height[currrent_write], max(20 , text_surface.get_width() ), text_surface.get_height()))                

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                writing = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if currrent_write == 4:
                        writing = False
                    elif currrent_write == 0:
                        data[currrent_write] = typed
                    else:
                        if typed.isdigit():
                            data[currrent_write] = int(typed)
                        else:
                            data[currrent_write] = 0
                    typed = ""
                    currrent_write += 1
                elif event.key == pygame.K_BACKSPACE:
                    typed = typed[:-1]
                    data[currrent_write] = typed
                elif event.key == pygame.K_SLASH:
                    data = ["RANDOM" , rd.randint(0 , 20) , rd.randint(20 , 100) , 0]
                    data[3] =  rd.randint(data[2] , 100)
                    currrent_write = 4
                else:
                    typed += event.unicode
                    data[currrent_write] = typed
            if currrent_write == 4:
                writing = False
                break

        timer += 1
        pygame.display.flip()

    table_coords = get_table_from_poi(table_coords)
    new = loc([table_coords] , int(data[1]) ,int(data[2]) ,int(data[3]) , str(data[0]))
    new.center = center

    global start_all_loc , ENERGY_BOOK , num
    num = 0
    start_all_loc.append(new)
    t_all = copy.deepcopy(start_all_loc)
    ENERGY_BOOK = []
    ENERGY_BOOK = start(t_all , ENERGY_BOOK)

    display_ui(new , start_all_loc)

def draw_grid_line(path , COLOR):
    line = []
    for i in range(len(path)-1):
        start = (get_poi_from_table(path[i]))
        end = get_poi_from_table(path[i+1])
        pygame.draw.line(screen , COLOR , start , end ,  width = line_width)
        pygame.draw.circle(screen , COLOR ,  end , line_width)

def distance_of_path(path): #this is simple and dosent work with angles only direct directions
    sum = 0
    steps = []
    for i in range(len(path) - 1):
        steps.append(abs(path[i + 1][0] - path[i][0]) + abs(path[i + 1][1] - path[i][1]))
        sum += steps[-1]
    return steps + [sum]

def electron_flow(path , time , distance):
    # for now let freq be 1
    dis = el_speed * time
    sum = 0
    for n in range(len(distance) - 1):
        sum += distance[n]
        if sum >= dis:
            break
    sum -= distance[n]
    time = time - sum/el_speed
    dx = path[n + 1][0] - path[n][0]
    dy = path[n + 1][1] - path[n][1]
    if dx == 0:
        if dy > 0:
            current_poi = get_poi_from_table([path[n][0] , time + path[n][1]])
        else:
            current_poi = get_poi_from_table([path[n][0] ,path[n][1] - time])
    elif dy == 0:
        if dx > 0:
            current_poi = get_poi_from_table([time + path[n][0] , path[n][1]])
        else:
            current_poi = get_poi_from_table([path[n][0] - time, path[n][1]])
    else:
        gradient = dy/dx
        if dx > 0:
            current_poi = get_poi_from_table([time + path[n][0],gradient * time + path[n][1]])
        else:
            current_poi = get_poi_from_table([time + path[n][0],gradient * time - path[n][1]])
    pygame.draw.circle(screen , BLUE , current_poi , 10)
    pygame.draw.line(screen,WHITE,[current_poi[0]-5,current_poi[1]],[current_poi[0]+5,current_poi[1]],width = 3)

def e_list(electrons_pending , time): # format is line , the dis and the space between each
    changes = []
    for el in electrons_pending:
        loop = el[3]
        segment = el[1][-1]/el[2]
        if el[3] == True:
            time = round(100 * (time % ((segment))))/100 + el[1][-1] 
        else:
            time = (time % (el[1][-1] * 2 ))
        time = int(1000 * time)/1000
        timing = [abs((segment * (x + 1))) for x in range(el[2])]

        for t in timing:
            t_time = (time - t)
            if t_time > 0 and t_time < (el[1][-1] ):
                electron_flow(el[0] , t_time , el[1])  
            elif t_time > (el[1][-1] - 3):
                loop = True
        if loop == True:
            changes.append(el[:3] + [True])
        else:
            changes.append(el)
    
    return changes

def find_loc(all_loc , loc_poi):
    num = 0
    for l in range(len(all_loc)):
        for poi in all_loc[l].poi:
            poi = [poi[1] , poi[0]]
            if loc_poi == poi:
                num = 1
                return l
                break
        if num == 1:
            break
    if num == 1:
        return l
    
def find_loc_type(all_loc , loc_type):
    num = 0
    for l in all_loc:
        if loc_type == l.type:
                num = 1
                return l
                break
        if num == 1:
            break
    if num == 1:
        return l
        
def Read_BOOK(ENERGY_BOOK , step , all_loc):
    global start_all_loc , current_page
    if step < (len(ENERGY_BOOK)-1):
        page = ENERGY_BOOK[step]
    else:
        page = ENERGY_BOOK[-1] 

    if page[1] not in ["PASS","FAILED"]:
        fro = find_loc(start_all_loc , [page[1].poi[0][1],page[1].poi[0][0]])
        to = find_loc(start_all_loc , [page[2].poi[0][1],page[2].poi[0][0]])
        
        dis = abs(start_all_loc[fro].poi[0][0] - start_all_loc[to].poi[0][0]) + abs(start_all_loc[fro].poi[0][1] - start_all_loc[to].poi[0][1])
        start_all_loc[fro].net -= int(page[0]) * ( 1 + 0.1 ** dis) 
        start_all_loc[to].net += int(page[0]) 

        electrons_pending.clear()
        electrons_pending.append([start_all_loc[fro].grid_lines["Power Plant"],distance_of_path(start_all_loc[fro].grid_lines["Power Plant"]),distance_of_path(start_all_loc[fro].grid_lines["Power Plant"])[-1]//2,True]) 
        electrons_pending.append([start_all_loc[to].grid_lines["Power Plant"][-1::-1],distance_of_path(start_all_loc[to].grid_lines["Power Plant"][-1::-1]),distance_of_path(start_all_loc[to].grid_lines["Power Plant"][-1::-1])[-1]//2,True]) 
    else:
        electrons_pending.clear()
    current_page = page
    display_ui(current_loc , all_loc)

def Back_BOOk(ENERGY_BOOK , step, all_loc):
    global start_all_loc , current_page
    global start_all_loc , current_page
    if step < len(ENERGY_BOOK) and step > 0:
        page = ENERGY_BOOK[step - 1]
        if page[1] not in ["PASS","FAILED"]:
            fro = find_loc(start_all_loc , [page[1].poi[0][1],page[1].poi[0][0]])
            to = find_loc(start_all_loc , [page[2].poi[0][1],page[2].poi[0][0]])
            
            dis = abs(start_all_loc[fro].poi[0][0] - start_all_loc[to].poi[0][0]) + abs(start_all_loc[fro].poi[0][1] - start_all_loc[to].poi[0][1])
            start_all_loc[fro].net += int(page[0]) * ( 1 + 0.1 ** dis) 
            start_all_loc[to].net -= int(page[0]) 
    elif step < 0:
        page = ENERGY_BOOK[step - 1]
    else:
        page = ENERGY_BOOK[0]
    display_ui(current_loc , all_loc)
    electrons_pending.clear()
    if step < len(ENERGY_BOOK):
        page = ENERGY_BOOK[step - 1]
    else:
        page = ENERGY_BOOK[-1]
    current_page = page
    display_ui(current_loc , all_loc)

def nice_grid(all_loc):

    pygame.draw.rect(screen , GREEN , (border_size , border_size , sub_width , sub_height))
    draw_grid()
    for l in all_loc:
        if l.type[:5] == "house":
            if l.color == 0:
                l.color = vibrant_colors[rd.randint(0 , len(vibrant_colors)-1)]
            for poi in l.poi:
                poi = [poi[1],poi[0]]
                house(poi , l.color)
        elif l.type == "hospital":
            for poi in l.poi:
                poi = get_poi_from_table(poi)
                pygame.draw.rect(screen , COLOURS["BROWN"] , (poi[1] - grid_size//2 , poi[0] - grid_size//2 , grid_size , grid_size))
            
            poi = l.poi[0]
            poi = get_poi_from_table(poi)
            pygame.draw.rect(screen , COLOURS["WHITE"] , (poi[1] - grid_size//2 - grid_size * 1, poi[0] - grid_size//2 - grid_size * 2, grid_size * 2, grid_size * 3))
        elif l.type == "geothermal":
            poi = get_poi_from_table(l.poi[0])
            pygame.draw.rect(screen , COLOURS["BLUE"] , (poi[1] - grid_size//2 , poi[0] - grid_size//2 - grid_size , grid_size , grid_size * 2))
            pygame.draw.rect(screen , GRAY , (poi[1] + grid_size//2 , poi[0] - grid_size//2 - grid_size * 2, grid_size * 3, grid_size * 2))
            pygame.draw.rect(screen , COLOURS["RED"] , (poi[1] - grid_size//2 + grid_size * 4, poi[0] - grid_size//2 - grid_size , grid_size , grid_size * 2))
   
        elif l.type[:5] == "solar":
            for p in l.poi:
                p= [p[1] , p[0]]
                solar(p)
        else:
            for p in l.poi:
                poi = get_poi_from_table(p)
                pygame.draw.rect(screen , GRAY , (poi[1] - grid_size//2 , poi[0] - grid_size//2 , grid_size , grid_size))
                #pygame.draw.lines(screen , RED , False , [[poi[1] -grid_size//2 , poi[0] -grid_size//2] , [poi[1] , poi[1] + grid_size//3* 2] , [poi[1] + grid_size//2 , poi[0] -grid_size//2]])
    pygame.draw.lines(screen, BLACK , False , [[340, 20], [340, 220], [500, 220], [500, 120], [620, 120], [620, 20], [40, 20], [100, 20], [100, 460], [260, 460], [260, 280], [340, 280], [340, 220], [500, 220], [500, 120], [620, 120], [620, 460], [260, 460], [260, 280], [180, 280], [180, 140], [340, 140], [340, 280], [260, 280], [260, 460], [260, 580], [260, 600], [260, 280], [180, 280], [180, 140], [340, 140], [340, 280], [260, 280], [260, 460], [100, 460], [0, 460] ,[700,460]] , width = grid_size//2)
    pygame.draw.lines(screen, YELLOW , False , [[340, 20], [340, 220], [500, 220], [500, 120], [620, 120], [620, 20], [40, 20], [100, 20], [100, 460], [260, 460], [260, 280], [340, 280], [340, 220], [500, 220], [500, 120], [620, 120], [620, 460], [260, 460], [260, 280], [180, 280], [180, 140], [340, 140], [340, 280], [260, 280], [260, 460], [260, 580], [260, 600], [260, 280], [180, 280], [180, 140], [340, 140], [340, 280], [260, 280], [260, 460], [100, 460], [0, 460] ,[700,460]] , width = grid_size//20)
    pygame.draw.polygon(screen, COLOURS["LIGHT_BROWN"], [[693, 473], [645, 494], [518, 491], [467, 504], [437, 512], [412, 528], [364, 550], [337, 563], [310, 573], [285, 583], [269, 599], [693, 594]])
    pygame.draw.polygon(screen , COLOURS["BLUE"] , [[700, 480], [640, 500], [520, 500], [460, 520], [400, 560], [360, 580], [280, 600], [700, 600]])
    pygame.draw.polygon(screen , COLOURS["DARK_BLUE"], [[696, 532], [579, 566], [480, 578], [432, 599], [695, 598]])
    #pygame.draw.polygon(screen , COLOURS["BROWN"] , [[51, 448], [51, 432], [39, 430], [31, 418], [38, 412], [63, 413], [61, 427], [60, 431], [55, 431], [57, 455], [50, 455]])
    pygame.draw.lines(screen , BLUE , True , [[0, 600], [700, 600], [700, 0], [0, 0]] , width = border_size * 2)

def draw_all_line(all_line , COLOR):

    for lines in all_line:
        draw_grid_line(lines ,  COLOR)  

def start(all_loc , ENERGY_BOOK):
    ENERGY_BOOK = run(8,6,all_loc,ENERGY_BOOK) # there is an issue due to the list being mutable
    return ENERGY_BOOK
 
def draw_new_line(all_loc , all_lines , coords):
    global electrons_pending , time

    coords = get_table_from_poi(coords)
    running = True
    line = [coords]
    while running:
        clock.tick(20)
        poi = pygame.mouse.get_pos()
        poi = get_table_from_poi(poi)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_k:
                    pygame.quit()
                    exit()
                elif event.key == pygame.K_DELETE:
                    line.pop()
            if event.type == pygame.MOUSEBUTTONDOWN:
                poi = [poi[1],poi[0]]
                for l in all_loc:
                    for p in l.poi:
                        if p == coords:
                            pass
                        elif p == poi:
                            running = False
                            break

                poi = [poi[1],poi[0]]
                if coords != poi:
                    line.append(poi)
            

        if num_1 == False:
            draw_grid()
            draw_grid_net(start_all_loc)
            draw_all_line(all_lines , YELLOW)
            display_ui(current_loc , start_all_loc)
            electrons_pending = e_list(electrons_pending , time )
            
            time += 0.2
        else:
            draw_grid()
            nice_grid(start_all_loc)
            display_ui(current_loc , start_all_loc)
            draw_all_line(all_lines , DARK_GRAY)

        draw_grid_line(line + [poi], YELLOW)
        pygame.display.flip()
    
    all_lines.append(line)
    fix_lines(all_lines , all_loc)
    dis =  distance_of_path(line)
    start = all_loc[find_loc(all_loc , line[0])]
    end = all_loc[find_loc(all_loc , line[-1])]
    start.grid_lines[str(start.center.type)] = line
    start.center.grid_lines[str(end.type)] = line[-1::-1]

def house(poi , color):
    poi = get_poi_from_table(poi)
    pygame.draw.rect(screen , color , (poi[0] - grid_size//2 , poi[1] - grid_size//2 , grid_size , grid_size))

def solar(poi):
    poi = get_poi_from_table(poi)
    pygame.draw.rect(screen , GRAY , (poi[0] - grid_size//2 , poi[1] - grid_size//2, grid_size , grid_size * 0.9))
    pygame.draw.rect(screen , LIGHT_BLUE , (poi[0] - grid_size * 0.4 , poi[1] - grid_size * 0.4 , grid_size - grid_size * 0.15, grid_size//4))
    pygame.draw.rect(screen , LIGHT_BLUE , (poi[0] - grid_size * 0.4 , poi[1] , grid_size - grid_size * 0.15, grid_size//4))

def all_extra():
    ui_write(str(current_mouse_tab1e) , 15 , border_size + 10, HEIGHT - border_size - 20)

def fix_lines(all_lines , start_all_loc):
    global center 
    for line in all_lines:
        start = find_loc(start_all_loc , line[0])
        end = find_loc(start_all_loc , line[-1])
        start_all_loc[start].grid_lines[start_all_loc[start].center.type] = line
        center.grid_lines[start_all_loc[end].type] = line[-1::-1]

    #code

draw_grid()

#loc() (poi: Any, prod: Any, dem: Any, store: Any, type: Any) -> loc
house1 = loc([[11,21] , [12,21] , [13,21], [11,20] , [12,20] , [13,20]] , 10 , 30 , 10 , "house1")
house2 = loc([[11, 14], [12, 14], [12, 15], [11, 15]],10 , 50 , 5 , "house2")
house3 = loc([[10, 12], [10, 13], [11, 13], [12, 13], [12, 12], [11, 12]] , 15 ,20 ,3 , "house3")
house4 = loc([[12, 10], [12, 11], [11, 11], [11, 10], [10, 10]] ,  1 , 10 , 10 , "house4")
house5 = loc([[20, 13], [20, 14], [20, 15], [20, 16], [21, 16], [21, 15], [21, 14], [21, 13]] , 3 , 6 , 8 , "house5")
house6 = loc([[19, 10], [20, 10], [21, 10], [21, 11], [20, 11], [19, 11], [18, 11]], 2 , 15 , 0 , "house6")
my_house = loc([[20, 18], [21, 18], [21, 19], [20, 19], [20, 20], [21, 20], [21, 21], [20, 21], [19, 21], [19, 20]] , 0 , 20 , 0 , "housem")
fun_house = loc([[5, 15], [5, 14], [5, 13], [4, 13], [4, 14], [4, 15]] , 1 , 15 ,20 ,"house_fun")
house55 = loc([[19, 5], [20, 5], [21, 6], [20, 7]]  + [[21, 5], [21, 7], [20, 6]], 0 , 100  , 0 , "house_55")

cen = []
for y in range(2):
    cen = cen + [[3 - y , 28 - x ] for x in range(6)]
hos1 = loc(cen + [[1 , 27],[1 , 28]], 0 , 15 , 10 , "hospital")

cem = []
for x in range(3):
    cem = cem + [[3 , 18+ x],[4,18 + x],[5 ,18 + x],[6 ,18 + x],[7,18 + x]]
solar1 = loc(cem , 5 , 1 , 10 , "solar")
hydro = loc([[24,9]], 100 , 10 , 10 , "hydro")

store = loc([[1,1]] , 100 , 0 , 10, "store")
cen = []
for y in range(4):
    cen = cen + [[18 - x , 18 - y] for x in range(4)]
center = loc(cen, 0 , 0 , 10 ,"Power Plant")

solar2 = loc([[6, 25], [6, 26], [6, 27], [7, 27], [7, 26], [7, 25], [8, 25], [8, 26]], 50 , 0 , 15 , "solar2")

geo_thermal = loc([[3, 5], [2, 5], [2, 6], [1, 6], [1, 7], [2, 7], [2, 8], [1, 8], [2, 9], [3, 9]] , 50 , 1 , 10 , "geothermal")
wave_farm = loc([[23,26],[23,27],[23,28]], 100 , 1 ,10 , "wave1")
all_loc = [house1 , house2 , house3 , house4 , house5 , house6 , house55 , my_house , fun_house , geo_thermal , wave_farm , solar1 , solar2 , hos1 , hydro , store , center ]

for l in all_loc:
    l.center = center

all_lines = [[[5, 3], [5, 15], [15, 15]], [[11, 12], [11, 14], [15, 14], [15, 15]], [[13, 12], [13, 14], [15, 14], [15, 15]], [[15, 12], [15, 15]], [[20, 13], [20, 15], [18, 15]], [[15, 5], [17, 5], [17, 15]], [[18, 7], [17, 7], [17, 15]], [[23, 3], [23, 16], [18, 16]], [[25, 8], [23, 8], [23, 16], [18, 16]], [[21, 19], [21, 17], [18, 17]], [[16, 20], [16, 18]], [[11, 18], [15, 18]], [[7, 20], [7, 16], [15, 16]], [[9, 24], [9, 17], [15, 17]], [[26, 23], [17, 23], [17, 18]], [[1, 1], [1, 16], [15, 16]]]
time = 0
electrons_pending = [] # format is line , the dis and the space between each
"""
fix_lines(all_lines)
for line in all_lines:
    startt = all_loc.index(find_loc(all_loc , line[0]))
    endd = all_loc.index(find_loc(all_loc , line[-1]))
    all_loc[startt].grid_lines[str(all_loc[startt].center.type)] = line
    all_loc[startt].center.grid_lines[str(all_loc[endd].type)] = line[-1::-1]
    pass
    print("L",start.grid_lines["Power Plant"])
"""
start_all_loc = copy.deepcopy(all_loc)
fix_lines(all_lines , start_all_loc)
# START
ENERGY_BOOK = []
ENERGY_BOOK = start(all_loc ,  ENERGY_BOOK)

draw_grid_net(all_loc)
display_ui(all_loc[1] , all_loc)

ptable(ENERGY_BOOK)
"""
for e in ENERGY_BOOK:
    if e[1] == "FAILED":
        pass
        print(e)
    elif e[1] == "PASS":
        pass
        print(e)
    else:
        pass
        print(e[0] , e[1].type , e[2].type)
"""

for l in start_all_loc:
    for poi in l.poi:
        table[poi[1]][poi[0]] = l.net
    #pass
    # print(l.net , l.type , l.prod - l.dem)
while True:
    clock.tick(20)

    if num_1 == False:
        
        draw_grid()
        draw_grid_net(start_all_loc)
        draw_all_line(all_lines , YELLOW)
        electrons_pending = e_list(electrons_pending , time )
        
        time += 0.2
    else:
        time = 0
        nice_grid(start_all_loc)
        draw_all_line(all_lines , DARK_GRAY)
        if len(all_click_p) > 2:
            pygame.draw.lines(screen , BLUE , True , all_click_p )

        #pygame.draw.polygon(screen , (70, 130, 180) , [[696, 227], [641, 275], [610, 319], [572, 349], [521, 379], [476, 407], [425, 432], [381, 451], [315, 451], [264, 435], [206, 417], [156, 411], [70, 402], [20, 403], [2, 401], [4, 476], [19, 463], [36, 447], [59, 443], [132, 430], [179, 434], [222, 446], [250, 460], [283, 465], [328, 477], [318, 507], [300, 521], [272, 534], [242, 560], [210, 580], [184, 594], [241, 595], [265, 595], [271, 580], [283, 566], [330, 541], [349, 519], [375, 497], [409, 480], [441, 466], [487, 443], [543, 409], [587, 374], [629, 353], [653, 308], [681, 290], [696, 274]])
    display_ui(current_loc , start_all_loc)

    all_extra()
    event_check()
    pygame.display.flip()

pass
print("ERROR")