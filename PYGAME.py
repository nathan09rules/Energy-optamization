import pygame
from math import sin , cos
import math as m
import numpy as np
import copy

#values for structure

WIDTH , HEIGHT = 1000 , 600
border_size = 10

info_panel_width = 300
slider_height = 30
slider_size = 10

button_size = 50

deep = 10

#derived values

sub_window = [WIDTH - info_panel_width - 2 * border_size , HEIGHT - 2 * slider_height - 2 * border_size] #dimension on where sun is
gradient = 1

#values preset

efficency = 0.15 # between 0.15 , 0.22
pi = m.pi

#values changed once

list_energy = []

#values that will be changed

s_percent = 0
slider_time = 0 # ranges from 0 to 1
area = 0
energy = 0
energy_total = 0

#checking cmd

time_ch = 0

#sky

SKY = (173, 216, 230)
light_intensity = 0.5

#interaction

hitbox = ["slider"]

cycle_solar = 2

#TRUE AND FALSE VARIABLES

STATE = [False , False , False , 0 , False] 
STATE_FOR = ["is mouse held", "has slidet been held" , "drawing solar","all_solar" , "checking"]

#classes

class solar_panel():
    def __init__(self , start : (int , int) , end : (int , int)):
        self.addition = 0
        self.start_base = start
        self.end_base = end
    
    #properties
    
    @property
    def add(self):
        return self.addition
    
    @property
    def start(self):
        return (self.start_base[0] + self.addition , self.start_base[1])
    
    @property
    def end(self):
        return (self.end_base[0] + self.addition , self.end_base[1])
    
    #func

    @add.setter
    def add(self , value):
        self.addition = value

#values for design

PEACH = (255, 178, 127)  
MINT = (159, 226, 191)  
BLUE = (135, 206, 250)  
PURPLE = (200, 160, 255)  
PINK = (255, 160, 180)  
YELLOW = (255, 245, 157)  
RED = (255, 140, 140)  
DARK_BLUE = (20, 30, 60)
LIGHT_BLUE = (173, 216, 230)  
LILAC = (220, 190, 255)  
GREEN = (119, 221, 119)  
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

#sky colours

sky_colors = {
    1.0: (10, 10, 40),        # Night (very dark blue)
    0.9: (30, 30, 60),        # Night (deep navy blue)
    0.8: (80, 100, 130),      # Early dawn (blue-gray)
    0.7: (100, 130, 170),     # Cool twilight
    0.6: (120, 160, 200),     # Blue early sky
    0.5: (135, 185, 220),     # Morning sky
    0.4: (140, 200, 235),     # Bright sky
    0.3: (135, 215, 245),     # Clear sky
    0.2: (130, 225, 250),     # Near zenith
    0.1: (120, 235, 255),     # Brightest blue
    0.0: (110, 240, 255),     # Zenith (overhead)
    -0.1: (120, 235, 255)     # Post-zenith
}

#functions that sre used

def event_check() -> None:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit
            exit()
        
        elif event.type == pygame.KEYDOWN:

            if event.key == pygame.K_k:
                pygame.quit()
                exit()

            elif event.key == pygame.K_RETURN:
                debug_values()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x , mouse_y = pygame.mouse.get_pos()

            print((mouse_x , mouse_y))
            for i in range(len(hitbox)):
                box = hitbox[i]
                if mouse_x > box[0][0] and mouse_x < box[1][0]:
                    if mouse_y > box[0][1] and mouse_y < box[1][1]:
                        if i == 0:
                            STATE[1] = True
                            STATE[0] = True
        
        elif event.type == pygame.MOUSEBUTTONUP:
            mouse_x , mouse_y = pygame.mouse.get_pos()

            for i in range(len(hitbox)):
                box = hitbox[i]
                print(i)
                if mouse_x > box[0][0] and mouse_x < box[1][0]:
                    if mouse_y > box[0][1] and mouse_y < box[1][1]:
                        if i != 0:
                            box[2]()

#function used for the overall structure

def draw_screen() -> None:
    #math done

    light_intensity_math(slider_time)

    #starting scene

    screen.fill(PURPLE)

    #sky

    pygame.draw.rect(screen , SKY , (border_size , border_size , WIDTH - 2 * border_size , HEIGHT - 2 * border_size - 2 * slider_height),border_radius=5)
    
    #solar

    draw_solar_shadow(all_solar)
    draw_all_solar(all_solar)

    #ui

    pygame.draw.rect(screen , WHITE , (WIDTH - info_panel_width - border_size, border_size , info_panel_width , HEIGHT - 2 * border_size - 2 *slider_height) , border_bottom_right_radius=5)

    #PURPLE boders

    pygame.draw.rect(screen , PURPLE , (0 , 0 , border_size , HEIGHT))
    pygame.draw.rect(screen , PURPLE , (0 , 0 , WIDTH , border_size))
    pygame.draw.rect(screen , PURPLE , (0 , HEIGHT - border_size , WIDTH , border_size))
    pygame.draw.rect(screen , PURPLE , (WIDTH - border_size , 0 , WIDTH , HEIGHT))


    #between border

    pygame.draw.rect(screen , PURPLE , (WIDTH - info_panel_width - border_size, border_size , border_size , HEIGHT - 2 * border_size - 2 * slider_height))
    pygame.draw.rect(screen , PURPLE , (border_size , HEIGHT - border_size - 2 * slider_height , WIDTH - 2 * border_size , border_size))

    #ui
    ui()

#dunction to do math

def light_intensity_math(slider_time) -> None: # I=A * cos(θ) for 0 just put slider_time
    angle = round(slider_time , 5) * pi

    #LINK to get A the maximum https://en.wikipedia.org/wiki/Sunlight#Intensity_in_the_Solar_System for EARTH A is 1413

    global light_intensity , SKY , gradient

    gradient = round(sin(angle) / cos(angle) , 5)

    light_intensity = abs(1413 * sin((angle))) # Watts / m ^ 2
    if slider_time > 0.99:
        light_intensity = 0

    time = abs ( int ( slider_time * 200 - 100) / 100 )
    
    time1 = round(time , 1)
    time2 = round(time1 - 0.1 , 1)

    percent = abs( time - time1 ) * 10

    colour = [(1 - percent) * sky_colors[time1][i] + (percent) * sky_colors[time2][i] for i in range(3)]
    SKY = colour

    #fun fact by me sunrise is not more energy than sunset for solar panels

def shadow_math() -> None:

    sum = 0

    for s in all_solar:
        m1 = (s.start[1] - s.end[1]) / (s.start[0] - s.end[0]) # gradent
        m2 = (s.start[0] - s.end[0]) / (s.start[1] - s.end[1]) #inverse gradend

        c1 = s.start[1] - m1 * s.start[0]
        
        num = 0

        for x in np.linspace(s.start[0] , s.end[0] , deep):

            y = m1 * x + c1

            depth = 10

            if m1 > 0:
                colour = screen.get_at((abs(int((x + depth ))) , abs(int(y - m2 * depth ))))
                #pygame.draw.circle(screen , RED , (x + depth , y - m2 * depth ) , 10)
            else:
                colour = screen.get_at((abs(int(x - depth )) , abs(int(y - m2 * - depth ))))
                #pygame.draw.circle(screen , RED , (x - depth , y - m2 * - depth ) , 10)

            colour = colour[0] + colour[1] + colour[2] #only rgb

            if colour < 100:
                num += 1

                pygame.draw.circle(screen , RED , (x - depth , y - m2 * + depth ) , 10)

        sum += num

    average = (sum + 10) / (len(all_solar) * deep) * 100

    if average == 2.5:
        average = 0

    return average

def make_all_solar(module):
    width = 0
    for s in module:
        width += s.end[0] - s.start[0]
    
    num = sub_window[0] // width

    all_solar = []

    for i in range(num):

        mod = copy.deepcopy(module)

        for s in mod:

            s.add = i * width

            all_solar.append(s)

    return all_solar

def solar_energy(area , light_intensity): #formula is POWER = A * I * T
    return area * light_intensity * efficency

#math

def math():
    global s_percent , energy , area , STATE

    s_percent = shadow_math()

    area = 0

    for s in all_solar:
        #do
        area += m.sqrt(( s.end[0] - s.start[0] ) ** 2 + (s.end[1] - s.start[1]) ** 2 )

    area = area * (1 - s_percent)

    energy = solar_energy(area , light_intensity)


    if STATE[4] == False:
        STATE[4] = total_energy()

def total_energy():
    global energy_total , slider_time , time_ch , list_energy

    if time_ch == 0:
        time_ch + 1

        slider_time += 1 / deep
        slider_time = round(slider_time , 2)
        list_energy.append(energy)

        if slider_time == 1.0:
            slider_time = 0.5

            return True

    else: #check cmd
        time_ch = 0
        energy_total += energy

        if slider_time == 1.0:
            slider_time = 0.5

            return True
    
    return False
        
#functions to draw or visullise

def slider() -> None:
    global STATE , slider_time

    #slider and bg

    pygame.draw.rect(screen , MINT , (border_size , HEIGHT - border_size - 2 * slider_height , WIDTH - 2 * border_size , 2 * slider_height))
    pygame.draw.rect(screen , BLACK , (border_size * 2 , HEIGHT - slider_height - border_size, WIDTH - 4 * border_size , border_size) , border_radius=10)
    pygame.draw.rect(screen , PURPLE , (border_size , HEIGHT - border_size - 2 * slider_height , WIDTH - 2 * border_size , border_size))


    #circle

    pygame.draw.circle(screen , YELLOW , (slider_time * (WIDTH - 4 * border_size) + 2 * border_size, HEIGHT - slider_height - border_size / 2) , slider_size )
    pygame.draw.circle(screen , RED , (slider_time * (WIDTH - 4 * border_size) + 2 * border_size, HEIGHT - slider_height - border_size / 2) , slider_size // 2 )


    if STATE[1] == True:
        if pygame.mouse.get_pressed()[0] == True:
            drag_slider(pygame.mouse.get_pos()[0])

        else:
            STATE[1] = False

    hitbox[0] = [(slider_time * (WIDTH - 4 * border_size) + border_size, HEIGHT - slider_height - border_size / 2 - border_size) , (slider_time * (WIDTH - 4 * border_size) + 3 * border_size, HEIGHT - slider_height - border_size // 2 + border_size) , slider]

    #circle using the hitbox
    # box = hitbox[0]
    # pygame.draw.circle(screen , YELLOW , ((box[0][0] + box[1][0])//2 , (box[0][1] + box[1][1])//2) , slider_size)

def draw_all_solar(all_solar : tuple):
    for s in all_solar:
        pygame.draw.line(screen , BLUE , s.start , s.end ,  10)

def draw_solar_shadow(all_solar : tuple ,):
    
    sign = (gradient < 0) - (gradient > 0) 
    p1 , p2 = 0 ,0 

    for s in all_solar:
        
        depth = 500
        if gradient > 1000:
            p1 = (s.end[0] , s.end[1] + depth)
            p2 = (s.start[0] , s.start[1] + depth)
        elif gradient < 0:
            p1 = (s.end[0] + depth * sign , s.end[1] + depth * -gradient)
            p2 = (s.start[0] + depth * sign, s.start[1] + depth * -gradient)
        elif gradient > 0:
            p1 = (s.end[0] + depth * sign , s.end[1] + depth * gradient)
            p2 = (s.start[0] + depth * sign, s.start[1] + depth * gradient)
        else:
            p1 = (s.end[0] + depth * sign , s.end[1])
            p2 = (s.start[0] + depth * sign , s.start[1])

        """
        if p1[1] > 530:
            x = (530 - s.end[1] )/ -gradient
            p1 = (s.end[0] + x, s.end[1] + x * -gradient)
            if x == 0:
                p1 = (s.end[0] + depth , 530)

        if p2[1] > 530:
            x = (530 - s.start[1]) / gradient
            p2 = (s.start[0] + x,  s.start[1] + x * gradient)
            if x == 0:
                p2 = (s.start[0] + depth , 530)
        
        print(p1  , p2)
        """
        pygame.draw.polygon(screen , BLACK , [s.start , s.end , p1 , p2])

#functions for ui and stuff

def write(content : str , size : int , coords , colour , center : bool) -> None:
    font = pygame.font.SysFont(None , size)
    text = font.render(content , True , colour)

    if center == True:
        coords = (coords[0] - text.get_width()//2 , coords[1])
    
    screen.blit(text , coords)
    
def ui() -> None:
    write("SOLAR STATS" , 48 , (WIDTH - info_panel_width // 2 - border_size , border_size ) , BLACK , True)
    write(f"s_percent: {round(s_percent,2)}%" , 32 , (720 , 50) , BLACK , False)
    write(f"light_intensity: {round(light_intensity,2)}%" , 32 , (720 , 100) , BLACK , False)
    write(f"energy_prod: {abs(int(energy))}" , 32 , (720 , 150) , BLACK , False) # fix this its worng
    #write(f"total_energy: {list_energy[int(round(slider_time,2) * 10)]}" , 32 , (720 , 200) , BLACK , False)
    write(f"sun_angle: {round(slider_time , 2)}" , 32 , (720 , 250) , BLACK , False)

    print(list_energy)
    #draw buttons
    distance_button = (( info_panel_width - border_size) - (button_size * 3) ) // 3

    pygame.draw.rect(screen , BLUE , ( WIDTH - (button_size + distance_button) * 3, 450 , button_size , button_size))
    pygame.draw.rect(screen , BLUE , ( WIDTH - (button_size + distance_button) * 2, 450 , button_size , button_size))
    pygame.draw.rect(screen , BLUE , ( WIDTH - (button_size + distance_button) * 1, 450 , button_size , button_size))

# functions for moving or pressing

def drag_slider(pos_x):
    global slider_time

    percentage = (pos_x - border_size * 2) / (WIDTH - 4 * border_size)

    if percentage >= 0  and percentage <= 1:
        slider_time = percentage
    elif percentage < 0:
        slider_time = 0
    else:
        slider_time = 1

#state

def change_state():
    global STATE , all_solar
    STATE[3] += 1

    STATE[3] = STATE[3] % cycle_solar

    if STATE[3] == 0:
        s1 = solar_panel((10,530) , (160,330))
        s2 = solar_panel((160,330) , (310,530))

        module = [s1 , s2]

    elif STATE[3] == 1:
        s1 = solar_panel((10,530) , (180,330))

        module = [s1]

    all_solar = make_all_solar(module)

#debuging functions

def debug():
    for box in hitbox:
        pygame.draw.rect(screen , RED , (box[0][0] , box[0][1] , box[1][0] - box[0][0], box[1][1] - box[0][1]))
    
    pygame.draw.circle(screen , RED , (sub_window[0] // 2 + border_size , sub_window[1] - 2 * border_size) , 30)

    sun_ray = 300

    x =   int(cos(slider_time * pi) * sun_ray) + sub_window[0] // 2 + border_size
    y = - int(sin(slider_time * pi) * sun_ray) + sub_window[1] - 2 * border_size

    pygame.draw.line(screen , RED , (sub_window[0] // 2 + border_size , sub_window[1] - 2 * border_size) , ( x , y ) , border_size)

    for s in all_solar:
        m1 = (s.start[1] - s.end[1]) / (s.start[0] - s.end[0]) # gradent
        m2 = (s.start[0] - s.end[0]) / (s.start[1] - s.end[1]) #inverse gradend

        c1 = s.start[1] - m1 * s.start[0]
        num = 0

        for x in np.linspace(s.start[0] , s.end[0] , 10):

            y = m1 * x + c1

            depth = 10

            if m1 > 0:
                pygame.draw.circle(screen , RED , (x + depth , y - m2 * depth ) , 10)
            else:
                pygame.draw.circle(screen , RED , (x - depth , y - m2 * - depth ) , 10)

def debug_values():
    print(gradient)
    
#code before project starts

s1 = solar_panel((10,530) , (160,330))
s2 = solar_panel((160,330) , (310,530))

module = [s1 , s2]

all_solar = make_all_solar(module)

#initialising code

pygame.init()
pygame.display.set_caption("TEMPLATE")
screen = pygame.display.set_mode((WIDTH , HEIGHT))
clock = pygame.time.Clock()

distance_button = (( info_panel_width - border_size) - (button_size * 3) ) // 3


box = ((WIDTH - (button_size + distance_button) * 3 , 450 ) , (WIDTH - (button_size + distance_button) * 3 + button_size , 450 + button_size) , change_state)
hitbox.append(box)


#draw the structure

draw_screen()
slider()

#what changes

while True:
    clock.tick(20)

    event_check()

    draw_screen()

    slider()

    debug()

    math()

    shadow_math()

    pygame.display.flip()