import pygame
from settings import *
from random import sample

def draw_background():
    screen.fill(BACKGROUND_COLOR)
    draw_grid()

def draw_grid():
    cell_width=40
    for i in range (20,581,cell_width):
        pygame.draw.line(screen, BLACK, (i,20),(i,580))
        pygame.draw.line(screen, BLACK, (20,i),(580,i))

def gen_buttons():
    x,y,w,h=640,20,100,30
    buttons=[]
    for i in range (1,6):
        buttons.append({'name': 'Level '+str(i), 'coordinates': (x,y,w,h)})
        y=y+h+10
    buttons.append({'name': 'Generate', 'coordinates': (x,y,w,h)})

    return(buttons)

def draw_buttons():
    for b in buttons[:len(buttons)-1]:
        pygame.draw.rect(screen, GRAY, b['coordinates'])
        pygame.draw.rect(screen, BLACK, b['coordinates'], 3)
        text=font.render(b['name'], True, BLACK)
        screen.blit(text, (b['coordinates'][0]+17,b['coordinates'][1]+5))

    pygame.draw.rect(screen, GRAY, buttons[-1]['coordinates'])
    pygame.draw.rect(screen, BLACK,  buttons[-1]['coordinates'], 3)
    text=font.render( buttons[-1]['name'], True, BLACK)
    screen.blit(text, ( buttons[-1]['coordinates'][0]+8, buttons[-1]['coordinates'][1]+5))

def select_level(l):
    pygame.draw.rect(screen, PINK, buttons[l]['coordinates'])
    pygame.draw.rect(screen, BLACK, buttons[l]['coordinates'], 3)
    text=font.render(buttons[l]['name'], True, BLACK)
    screen.blit(text, (buttons[l]['coordinates'][0]+17,buttons[l]['coordinates'][1]+5))

pygame.init()
clock=pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT), flags, vsync=1)
pygame.display.set_caption('Maze♥')
font = pygame.font.SysFont('arial', 20)

draw_background()
buttons=gen_buttons()
draw_buttons()
selected=-1
run  = True
while run:
    for event in pygame.event.get():
        if (event.type == pygame.QUIT or (event.type==pygame.KEYDOWN and event.key==pygame.K_ESCAPE)):
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            x,y=pygame.mouse.get_pos()
            for i in range (len(buttons)):
                if(x>=buttons[i]['coordinates'][0] and x<=buttons[i]['coordinates'][0]+buttons[i]['coordinates'][2] and y>=buttons[i]['coordinates'][1] and y<=buttons[i]['coordinates'][1]+buttons[i]['coordinates'][3]):
                    selected=i
                    select_level(i)
                    break
                else:
                    selected=-1
                    draw_buttons()
        if (event.type == pygame.KEYDOWN):
            pass
            # for i in range(len(INPUTS)):
            #     if (event.key==INPUTS[i]):
            #         if(selected_cell[0]!=-1 and (grid[selected_cell[0]][selected_cell[1]]==0 or grid_bold[selected_cell[0]][selected_cell[1]]==0)):
            #             draw_number(selected_cell[0],selected_cell[1], i+1)
                    

    pygame.display.flip()
    clock.tick(30)
    

pygame.quit()

