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
    y=y+h+10
    buttons.append({'name': 'Watch', 'coordinates': (x,y,w,h)})

    return(buttons)

def draw_buttons():
    
    for b in buttons[:len(buttons)-1]:
        pygame.draw.rect(screen, GRAY, b['coordinates'])
        pygame.draw.rect(screen, BLACK, b['coordinates'], 3)
        text=font.render(b['name'], True, BLACK)
        screen.blit(text, (b['coordinates'][0]+17,b['coordinates'][1]+5))
    
    if selected!=-1:
        pygame.draw.rect(screen, PINK, buttons[selected]['coordinates'])
        pygame.draw.rect(screen, BLACK, buttons[selected]['coordinates'], 3)
        text=font.render(buttons[selected]['name'], True, BLACK)
        screen.blit(text, (buttons[selected]['coordinates'][0]+17,buttons[selected]['coordinates'][1]+5))

    pygame.draw.rect(screen, GRAY, buttons[-2]['coordinates'])
    pygame.draw.rect(screen, BLACK,  buttons[-2]['coordinates'], 3)
    text=font.render( buttons[-2]['name'], True, BLACK)
    screen.blit(text, ( buttons[-2]['coordinates'][0]+8, buttons[-2]['coordinates'][1]+5))

    pygame.draw.rect(screen, GRAY, buttons[-1]['coordinates'])
    pygame.draw.rect(screen, BLACK,  buttons[-1]['coordinates'], 3)
    text=font.render( buttons[-1]['name'], True, BLACK)
    screen.blit(text, ( buttons[-1]['coordinates'][0]+22, buttons[-1]['coordinates'][1]+5))

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

def init_grids(l, cell_width):
    draw_background()
    draw_buttons()
    if(l==0):
        cell_width=70
    elif(l==1):
        cell_width=56
    elif(l==2):
        cell_width=40
    elif(l==3):
        cell_width=20
    elif(l==4):
        cell_width=10
    print(cell_width)
    draw_grid(cell_width)
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

    return(gird_visited, grid_walls, cell_width)

def display_visited(row, col, cell_color, wall_color=BACKGROUND_COLOR):
    color_cell(row, col, cell_color)
    walls=grid_walls[row][col]
    for i in range (len(walls)):
        if(walls[i]==1):
            draw_wall(row,col,i,wall_color)

def draw_wall(row,col,n,wall_color=BACKGROUND_COLOR):
    #0->up, 1->right, 2->down, 3->left
    x,y,w,h=col*cell_width+20, row*cell_width+20, cell_width,cell_width
    match n:
        case 0:
            pygame.draw.line(screen, wall_color, (x,y),(x+cell_width,y), 3)
        case 1:
            pygame.draw.line(screen, wall_color, (x+cell_width,y),(x+cell_width,y+cell_width), 3)
        case 2:
            pygame.draw.line(screen, wall_color, (x,y+cell_width),(x+cell_width,y+cell_width), 3)
        case 3:
            pygame.draw.line(screen, wall_color, (x,y),(x,y+cell_width), 3)
    if(row==0 and col==0):
        pygame.draw.line(screen, RED, (20,20),(20+cell_width,20), 3)
    elif(row==(560/cell_width)-1 and col==(560/cell_width)-1):
        pygame.draw.line(screen, RED, ( (row*cell_width)+cell_width+20 , (col*cell_width)+20 ) , ((row*cell_width)+cell_width+20 , (col*cell_width)+cell_width+20), 3)


def vis_gen_maze(row,col, prev_row, prev_col):
    while (row is not None):
        print(row,col, prev_row, prev_col)
        time.sleep(0.01)
        display_visited(row,col,(0,255,0))
        if(prev_row is not None):
            display_visited(prev_row,prev_col,BACKGROUND_COLOR)
        gird_visited[row][col]=1

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

            prev_row=row
            prev_col=col
            row=new_r
            col=new_c
        else:       

            if(check_all_visited()):
                prev_row=None
                prev_col=None
                row=None
                col=None
            else:
                temp=stack[-1]
                stack.pop()
                prev_row=row
                prev_col=col
                row=temp[0]
                col=temp[1]
        pygame.display.flip()
    return(None,None,None,None)

def gen_maze(row, col, cell_width):
    while (row is not None):

        gird_visited[row][col]=1

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

            row=new_r
            col=new_c
            
        else:       

            if(check_all_visited()):
                row=None
                col=None
            else:
                temp=stack[-1]
                stack.pop()
                row=temp[0]
                col=temp[1]
        pygame.display.flip()
    
    size=int(560/cell_width)
    for i in range(size):
        grid_walls[0][i][0]=0
        grid_walls[i][0][3]=0
        grid_walls[size-1][i][2]=0
        grid_walls[i][size-1][1]=0
    grid_walls[0][0][0]=1
    grid_walls[size-1][size-1][1]=1
    return(None,None,None,None)

def check_all_visited():
    for r in gird_visited:
        for c in r:
            if c==0:
                return False
    return(True)

def display_maze():
    size=int(560/cell_width)
    draw_grid(cell_width)
    for r in range (size):
        for c in range (size):
            walls=grid_walls[r][c]
            for i in range(len(walls)):
                if walls[i]==1:
                    draw_wall(r,c,i)
    draw_wall(0,0,0)
    draw_wall(size-1,size-1,1)

def select_watch():
    pygame.draw.rect(screen, PINK, buttons[6]['coordinates'])
    pygame.draw.rect(screen, BLACK, buttons[6]['coordinates'], 3)
    text=font.render(buttons[6]['name'], True, BLACK)
    screen.blit(text, (buttons[6]['coordinates'][0]+22,buttons[6]['coordinates'][1]+5))

def move_player(dir, cell_width):
    size=560/cell_width
    player_cell=stack_player[-1]
    valid=False

    print(grid_walls[player_cell[0]][player_cell[1]][0])
    print(grid_walls[player_cell[0]][player_cell[1]][1])
    print(grid_walls[player_cell[0]][player_cell[1]][2])
    print(grid_walls[player_cell[0]][player_cell[1]][3])

    if dir==0 and grid_walls[player_cell[0]][player_cell[1]][0]==1 and player_cell[0]-1>=0:
        player_cell=(player_cell[0]-1, player_cell[1])
        valid=True
    elif dir==1 and grid_walls[player_cell[0]][player_cell[1]][1]==1 and player_cell[1]+1<size:
        player_cell=(player_cell[0], player_cell[1]+1)
        valid=True
    elif dir==2  and grid_walls[player_cell[0]][player_cell[1]][2]==1:
        player_cell=(player_cell[0]+1, player_cell[1])
        valid=True
    elif dir==3 and grid_walls[player_cell[0]][player_cell[1]][3]==1:
        player_cell=(player_cell[0], player_cell[1]-1) 
        valid=True
    if valid:
        if (len(stack_player)>0):
            if(len(stack_player)>1 and stack_player[-2][0]==player_cell[0]  and stack_player[-2][1]==player_cell[1]):
                display_visited(stack_player[-1][0],stack_player[-1][1], BACKGROUND_COLOR)
                stack_player.pop()
            else:
                display_visited(stack_player[-1][0],stack_player[-1][1],  DARK_GREEN, DARK_GREEN)
                stack_player.append(player_cell)
        display_visited(player_cell[0],player_cell[1],GREEN,GREEN)      
        if(player_cell==(size-1,size-1)):
            display_text("Victory")

def display_text(text):
    print(text)
    pygame.draw.rect(screen, BACKGROUND_COLOR, (600,500,300,100))
    font = pygame.font.SysFont('arial', 25)
    text=font.render(text, True, PINK)
    screen.blit(text, (630,540))
    pygame.display.update()





pygame.init()
clock=pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT), flags, vsync=1)
pygame.display.set_caption('Maze♥')
font = pygame.font.SysFont('arial', 20)


cell_width=70
r1,c1,r2,c2=0,0,None,None
stack=[]
stack_player=[(0,0)]
selected=-1
selected_watch=False
prova=False
gird_visited, grid_walls=[],[]
generated=False
draw_background()
buttons=gen_buttons()
draw_buttons()


run  = True
while run:

    for event in pygame.event.get():
        if (event.type == pygame.QUIT or (event.type==pygame.KEYDOWN and event.key==pygame.K_ESCAPE)):
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            x,y=pygame.mouse.get_pos()
            display_text("")
            for i in range (len(buttons)):
                if(x>=buttons[i]['coordinates'][0] and x<=buttons[i]['coordinates'][0]+buttons[i]['coordinates'][2] and y>=buttons[i]['coordinates'][1] and y<=buttons[i]['coordinates'][1]+buttons[i]['coordinates'][3]):
                    if(i<len(buttons)-2):
                        selected=i
                        break
                    elif(i==5):
                        stack=[]
                        stack_player=[(0,0)]
                        generated=True
                        if(selected!=-1):
                            display_text("Generating")
                            gird_visited, grid_walls, cell_width=init_grids(selected, cell_width)
                            draw_grid(cell_width)
                            display_text("Generating")
                            print(cell_width)
                            gen_maze(0,0,cell_width)
                            display_maze()
                            display_visited(0,0,GREEN)
                            display_text("")
                        else:
                            display_text("Select level")
                    else:
                        stack=[]
                        if(selected!=-1):
                            gird_visited, grid_walls, cell_width=init_grids(selected, cell_width)
                            draw_grid(cell_width)
                            vis_gen_maze(0,0,None,None)
                        else:
                            display_text("Select level")
                        # else:
                        #     print("fine")
                        #     draw_background()
                        #     display_maze()
            else:
                selected=-1
            draw_buttons()              
        if (event.type == pygame.KEYDOWN):
            for i in range(len(INPUTS)):
                if (event.key==INPUTS[i] and generated==True):
                    move_player(i, cell_width)
                        
                    

    pygame.display.flip()
    clock.tick(30)
    

pygame.quit()

