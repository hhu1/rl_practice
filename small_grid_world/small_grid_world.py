import re,os,sys,random,copy

def initialize_grids(grids, n):
    for i in range(n):
        for j in range(n):
            if i==0 and j==0:
                grids[(i,j)] = 0
            else:
                grids[(i,j)] = random.random() 

    return grids

def update_value(old_grids, new_grids, state,n):
    for state in old_grids:
        if state ==(0,0):continue
        else:
            neighbor_vals = []
            for neighbor in find_neighbors(state, n):
                neighbor_vals.append(old_grids[neighbor])

            new_grids[state] = max(neighbor_vals) -1

def find_neighbors(state,n):
    x, y = state
    neis = []
    if legit(x+1, y, n): neis.append((x+1, y))
    if legit(x-1, y, n): neis.append((x-1, y))
    if legit(x, y+1, n): neis.append((x, y+1))
    if legit(x, y-1, n): neis.append((x, y-1))

    return neis

def legit(x,y,n):
    if x<0 or y<0 or x>=n or y>=n:return False
    else: return True
    

grids = {}
n = 4
iterations = 100

initialize_grids(grids, n)

for iteration in range(iterations):
    new_grids = copy.deepcopy(grids)
    for state in grids:
        update_value(grids, new_grids, state,n)
    grids = new_grids

for state in grids:
    print (state, grids[state])
