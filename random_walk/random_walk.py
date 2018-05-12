import re,os,sys,random

n = 10

def generate_episode(n):
    # generate one episode of random walk
    i = int(n/2)
    steps = [i]

    while i!=0 and i!=n-1:
        if random.random() < 0.5:
            i -=1
        else:
            i = i+1
        steps.append(i)
    return steps

def mc_learn(num_episodes, n):
    episodes = [generate_episode(n) for j in range(num_episodes)]

    visits = {} # total num of visits for each state
    rights = {} # for each state, the number of visits that ends in the right

    for j in range(n):
        visits[j] = 0
        rights[j] = 0

    for episode in episodes:
        # this is the states that has been visited in this episode
        states = set(episode)

        for state in states:
            visits[state] +=1
            if episode[len(episode)-1]!=0:
                rights[state] +=1
    
    vals = [1.0 * rights[j] / visits[j] for j in range(n)]
    return vals

def td0_learn(num_episodes, n, alpha):
    episodes = [generate_episode(n) for j in range(num_episodes)]
    
    vals = [0.5 for i in range(n)]
    vals[0] = 0.0; vals[n-1] = 1.0

    for episode in episodes:
        for i in range(len(episode)-1):
            vals[episode[i]] += alpha * (vals[episode[i+1]]
                    - vals[episode[i]])
    return vals
            
def td2_learn(num_episodes, n, alpha):
    # learn from state returns in next step, two more steps, 
    # three more steps, averaged.

    episodes = [generate_episode(n) for j in range(num_episodes)]
    
    vals = [0.5 for i in range(n)]
    vals[0] = 0.0; vals[n-1] = 1.0

    for episode in episodes:
        for i in range(len(episode)-1):
            # G stores the returns from next 3 steps
            G = []
            # add returns from the next step
            G.append(vals[episode[i+1]]) 
            # add return from the next two steps
            if i+2 <= len(episode)-1:
                G.append(vals[episode[i+2]])
            # add return from the next three steps
            if i+3 <= len(episode)-1:
                G.append(vals[episode[i+3]])

            # use the average return from the next 3 steps
            mean_return = 1.0*sum(G) / len(G)

            # update the value function
            vals[episode[i]] += alpha * (mean_return
                    - vals[episode[i]])
    return vals

mc_vals = mc_learn(10000, 7)
print("MC:\n%s" % " ".join([str(round(x,3)) for x in mc_vals]))

td0_vals = td0_learn(10000, 7, 0.001)
print("TD0:\n%s" % " ".join([str(round(x,3)) for x in td0_vals]))

td2_vals = td2_learn(10000, 7, 0.001)
print("TD2:\n%s" % " ".join([str(round(x,3)) for x in td2_vals]))
