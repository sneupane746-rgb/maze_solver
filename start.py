import random
import numpy as np
way=[[1,0,0,0,1],[0,0,0,0,0],[0,0,1,0,0],[0,1,1,0,0],[0,0,1,0,0]]
maze=np.array(way)



actions={"up":[-1,0],"down":[1,0],"right":[0,1],"left":[0,-1]}
actions_in_num={"up":1,"down":2,"right":3,"left":4}
learing_rate=0.01
gamma=0.9
epsilon=0.3

prep=np.zeros((25,5))
for k in range(25):
    prep[k][0]=k
qtable=prep


ending_position=[4,4]
current_position=[4,0]
move_limit=20


def find_reward(pos):
 if(pos==ending_position):
    reward=0
 else:
    reward=-1
 return reward

def next_posfinder(position,indices):
    row,col=indices
    next_p=[position[0]+row,position[1]+col]
    if(next_p[0]<0 or next_p[0]>4 or next_p[1]<0 or next_p[1]>4 or maze[next_p[0]][next_p[1]]==1 ):
       return position
    else: 
      return next_p


for i in range(100000):
   starting_position=[4,0]
   current_position=starting_position
   ml=1
   while(ml<=move_limit and current_position!=ending_position):
    s  = current_position[0]*5 + current_position[1]

    if random.random() < epsilon:
        action=random.choice(list(actions))
    else:
        action=list(actions)[np.argmax(qtable[s][1:5])]
    #print(action)


    next_position=next_posfinder(current_position,actions[action])
    #print(next_position)  
    
    s2 = next_position[0]*5 + next_position[1]
    a  = actions_in_num[action]

    reward = find_reward(next_position)
    best_next = max(qtable[s2][1:])
    qtable[s][a] += learing_rate * (reward + gamma * best_next - qtable[s][a])

    current_position = next_position
    ml = ml + 1     

#print(qtable)
answer=[]
for i in range(25):
 answer.append((np.argmax(qtable[i][1:5])+1)%5)



numpy_answer=np.array(answer,dtype=object)
numpy_answer[numpy_answer == 1] = "up"
numpy_answer[numpy_answer == 2] = "down"
numpy_answer[numpy_answer == 3] = "right"
numpy_answer[numpy_answer == 4] = "left"

np.set_printoptions(legacy='1.25')
for r in range(5):
    for c in range(5):
        if maze[r][c] == 1:
            numpy_answer[r*5 + c] = "wall"

numpy_answer[24]="goal"
#print("the path for the maze is: \n")
grid = np.array(numpy_answer.tolist()).reshape(5,5)

for row in grid:
    print(" | ".join(cell.ljust(5) for cell in row))