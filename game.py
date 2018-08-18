import pygame
import sys
import numpy as np
import imp
def read_data(filename):
    f = open(filename)
    global data
    data = imp.load_source('data', '', f)
    
read_data(sys.argv[2])
WI = int(data.imagewidth)
HE = int(data.imageheight)
MARGIN = int(data.linewidth)
x= MARGIN
y= MARGIN
list_xy=[0,0]
pick_coin=[]
pos=0
myscore=0
n=data.gridrow
m=data.gridcolumn
obstacle=[]

def draw_Grid(n,m):
  grid=[]
  for row in range(n):
    grid.append([])
    for column in range(m):
        grid[row].append(0)
  pygame.init()  
  robot,coin=load_robot_and_coin(WI,HE)
  obstacle,coin_pos_list=generate_obstacle_and_coin(n,m)
  #print obstacle  
  WINDOW_SIZE= [WI*n+n*MARGIN,HE*m+m*MARGIN]
  screen = pygame.display.set_mode(WINDOW_SIZE)
  file=open(sys.argv[1],"r")
  file=file.read()
  pygame.display.set_caption("Array Grid")
  return screen,robot,coin,file

   
def load_robot_and_coin(WI,HE):
  robot = pygame.image.load(data.robotimage)
  coin = pygame.image.load(data.coinimage)
  coin=pygame.transform.scale(coin,(WI,HE))
  robot=pygame.transform.scale(robot,(WI,HE))
  return robot,coin


def generate_obstacle_and_coin(n,m):
  coin_pos_list=[]  
  for i in range(n*m/3):
    op=[]
    coin_list=[]
    op.append(np.random.randint(1,n));
    op.append(np.random.randint(1,m))
    
    coin_list.append(np.random.randint(1,n));
    coin_list.append(np.random.randint(1,m));
    
    obstacle.append(op);
    coin_pos_list.append(coin_list)
  return obstacle,coin_pos_list
def draw_rectangle(x,y,pick_coin):
    B = (0, 0, 0) 
    W = (255, 255, 255)
    G = (0, 255, 0)
    R = (255, 0, 0)
    for row in range(n):
        for column in range(m):
            color = W
            op=[]
            op.append(row)
            op.append(column)
            if(op in obstacle ):
              color=B
            if op in pick_coin:
              color=W
            
            f1=(MARGIN + WI) * column + MARGIN
            f2=(MARGIN + HE) * row + MARGIN
            pygame.draw.rect(screen,color,
                             [f1,
                              f2,
                              WI,
                              HE])
           
            if(op not in obstacle and op not in pick_coin):
               screen.blit(coin,(f1,f2))
    return x,y,pick_coin
def right_mov(x,y,pos,done):
       pygame.time.delay(500)
       pos+=1
       list_xy[1]+=1
       x+=WI+MARGIN
       y+=0
       if(list_xy in obstacle ):
         print "cant move obstacle"
         done=True
         return x,y,pos,done
       screen.blit(robot, (x,y))
       pygame.display.flip()
       return x,y,pos,done
def down_mov(x,y,pos,done):
       pygame.time.delay(500)
       list_xy[0]+=1
       pos+=1
       x+=0
       y+=(HE+MARGIN)
       if(list_xy in obstacle ):
         print "cant move obstacle"
         done=True
         return x,y,pos,done
       screen.blit(robot, (x,y))
       return x,y,pos,done
def up_mov(x,y,pos,done):
       pygame.time.delay(500) 
       pos+=1
       list_xy[0]-=1
       x+=0
       y-=(HE+MARGIN)
       if(list_xy in obstacle ):
         print "cant move obstacle"
         done=True
         return x,y,pos,done
       screen.blit(robot, (x,y))
       return x,y,pos,done
def left_mov(x,y,pos,done):
       pygame.time.delay(500) 
       pos+=1
       list_xy[1]-=1
       x-=(WI+MARGIN)
       y+=0
       if(list_xy in obstacle ):
         print "cant move obstacle"
         done=True
         return x,y,pos,done
       screen.blit(robot, (x,y))
       return x,y,pos,done
def coin_picking(x,y,pos,pick_coin,myscore):
        myscore+=1;
        
        clist=[]
        clist.append(y/(HE+MARGIN))
        clist.append(x/(WI+MARGIN))
        pos+=1
        pick_coin.append(clist)
        pygame.time.delay(1000)
        return pick_coin,pos,myscore
def handle_event(screen,robot,coin,file,x,y):
  myscore=0
  pick_coin=[]
  print x
  global pos
  B = (0, 0, 0) 
  W = (255, 255, 255)
  G = (0, 255, 0)
  R = (255, 0, 0)

  done = False
  while not done:
    for event in pygame.event.get():  
        if event.type == pygame.QUIT: 
            done = True 
    screen.fill(R)
    x,y,pick_coin=draw_rectangle(x,y,pick_coin)
    if file[pos]=="r" and  pos<len(file)-1 :
        x,y,pos,done=right_mov(x,y,pos,done)
    elif file[pos]=="d" and  pos<len(file)-1:
        x,y,pos,done=down_mov(x,y,pos,done)
    elif file[pos]=="u" and  pos<len(file)-1:
          x,y,pos,done=up_mov(x,y,pos,done)   
    elif file[pos]=="l" and  pos<len(file)-1:
        x,y,pos,done=left_mov(x,y,pos,done)    
    elif file[pos]=="p" and  pos<len(file):
       pick_coin,pos,myscore=coin_picking(x,y,pos,pick_coin,myscore)
    pygame.display.flip()
  pygame.quit()
  return myscore

screen,robot,coin,file=draw_Grid(int(data.gridrow),int(data.gridcolumn))
myscore=handle_event(screen,robot,coin,file,x,y)
print myscore
