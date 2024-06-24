import pygame
from settings import *
import random 
import time

def draw_background():
    screen.fill(BACKGROUND_COLOR)

def draw_grid(cell_width):
    for i in range (20,581,cell_width):
        pygame.draw.line(screen, GRID_COLOR, (i,20),(i,580), 3)
        pygame.draw.line(screen, GRID_COLOR, (20,i),(580,i), 3)

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

def color_cell(row,col,color):
    x,y,w,h=col*cell_width+20, row*cell_width+20, cell_width,cell_width
    pygame.draw.rect(screen, color, (x,y,w,h))
    pygame.draw.line(screen, GRID_COLOR, (x,y),(x+cell_width,y), 3)
    pygame.draw.line(screen, GRID_COLOR, (x+cell_width,y),(x+cell_width,y+cell_width), 3)
    pygame.draw.line(screen, GRID_COLOR, (x,y+cell_width),(x+cell_width,y+cell_width), 3)
    pygame.draw.line(screen, GRID_COLOR, (x,y),(x,y+cell_width), 3)

def init_grids():
    size=int(560/cell_width)
    print(size)
    gird_visited=[]
    for i in range (size):
        t=[]
        for j in range (size):
            t.append(0)
        gird_visited.append(t)
    grid_walls= []
    for i in range (size):
        t=[]
        for j in range (size):
            t.append([0,0,0,0])
        grid_walls.append(t)

    return(gird_visited, grid_walls)

def display_visited(row, col):
    color_cell(row, col, GRAY)
    walls=grid_walls[row][col]
    for i in range (len(walls)):
        if(walls[i]==1):
            draw_wall(row,col,i)

def draw_wall(row,col,n):
    #0->up, 1->right, 2->down, 3->left
    x,y,w,h=col*cell_width+20, row*cell_width+20, cell_width,cell_width
    match n:
        case 0:
            pygame.draw.line(screen, BACKGROUND_COLOR, (x,y),(x+cell_width,y), 3)
        case 1:
            pygame.draw.line(screen, BACKGROUND_COLOR, (x+cell_width,y),(x+cell_width,y+cell_width), 3)
        case 2:
            pygame.draw.line(screen, BACKGROUND_COLOR, (x,y+cell_width),(x+cell_width,y+cell_width), 3)
        case 3:
            pygame.draw.line(screen, BACKGROUND_COLOR, (x,y),(x,y+cell_width), 3)

def gen_maze(row,col):

    time.sleep(0.1)
    display_visited(row,col)
    valid_cell=[]
    if(row-1!=-1 and gird_visited[row-1][col]==0):
        valid_cell.append([row-1,col,0])
    if(col-1!=-1 and gird_visited[row][col-1]==0):
        valid_cell.append([row,col-1,3])
    if(row+1!=len(gird_visited) and gird_visited[row+1][col]==0):
        valid_cell.append([row+1,col,2])
    if(col+1!=len(gird_visited) and gird_visited[row][col+1]==0):
        valid_cell.append([row,col+1,1])
    

    
    if (len(valid_cell)>0):
        stack.append((row,col))
        n=random.choice(valid_cell)
        new_r,new_c,wall=n

        gird_visited[row][col]=1
        grid_walls[row][col][wall]=1

        match wall:
            case 0:
                grid_walls[new_r][new_c][2]=1
            case 1:
                grid_walls[new_r][new_c][3]=1
            case 2:
                grid_walls[new_r][new_c][0]=1
            case 3:
                grid_walls[new_r][new_c][1]=1

        color_cell(row,col,BACKGROUND_COLOR)
        color_cell(new_r, new_c, (0,255,0))
        walls=grid_walls[row][col]

        for i in range (len(walls)):
            if(walls[i]==1):
                draw_wall(row,col,i)

        pygame.display.update()
        return(new_r,new_c)
        
    else:
        if(check_all_visited()):
            return None
        stack.pop()
        return(stack[-1])

def check_all_visited():
    for r in gird_visited:
        for c in r:
            if c==0:
                return False
    return(True)




pygame.init()
clock=pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT), flags, vsync=1)
pygame.display.set_caption('Maze♥')
font = pygame.font.SysFont('arial', 20)

draw_background()
cell_width=40
draw_grid(40)
buttons=gen_buttons()
draw_buttons()
gird_visited, grid_walls=init_grids()
coo=(0,0)
stack=[]
selected=-1
prova=False
run  = True
while run:

    if(coo is not None):
        coo=gen_maze(coo[0],coo[1])
        print(coo)
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
