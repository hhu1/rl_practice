import re,os,sys,random
import numpy as np

class Qmodel:
    def __init__(self, alpha, gamma, epsilon):
        self.qs = {}
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
    
    def get_q(self, state, a):
        if (state, a) in self.qs:
            return self.qs[(state, a)]
        else:
            new_state = GlobalParams.transit(state, a)
            if self.has_won(new_state):
                self.qs[(state, a)] = 10000
            else:
                self.qs[(state, a)] = 0
            return self.qs[(state, a)]

    def e_greedy(self, state):
        '''given a state, return an action (a) to recommend under e-greedy
        '''
        q_vals = []
        for a in range(9):
            q_vals.append(self.get_q(state, a))

        if random.random() < 1- self.epsilon:
            return np.argmax(q_vals)
        else:
            return random.randint(0,8)

    def greedy(self, state):
        '''given a state, return an action (a) to recommend under greedy
        '''
        q_vals = []
        for a in range(9):
            q_vals.append(self.get_q(state, a))

        return np.argmax(q_vals)

    def update(self, state, a):
        ''' given state and recommended action, return the next
            state, and update the q function
        '''

        next_s = GlobalParams.transit(state,a)
        new_qs = []
        for ap in range(9):
            new_qs.append(self.get_q(next_s, ap))

        self.qs[(state, a)] = (1.0-self.alpha)*self.get_q(state,a) + \
                self.alpha * (-1.0+self.gamma*max(new_qs))

        #print("Updated state to %s" % str(next_s))
        return next_s

    def has_won(self, state):
        if sum(state) == 0:
            return True
        else:
            return False
		



class GlobalParams(object):
    neighbors = {
            0: [0,1,3],
            1: [0,1,2,4],
            2: [1,2,5],
            3: [0,3,4,6],
            4: [1,3,4,5,7],
            5: [2,4,5,8],
            6: [3,6,7],
            7: [4,6,7,8],
            8: [5,7,8]
            }

    @staticmethod
    def transit(state, a):
        new_state = list(state)

        for nei in GlobalParams.neighbors[a]:
            new_state[nei] = 1 - new_state[nei]

        return tuple(new_state)

    @staticmethod
    def random_initialize():
        state = [0]*9

        while sum(state)==0:
            for i in range(100):
                index = random.randint(0,8)
                state[index] = 1.0 - state[index]
        return tuple(state)


def train_one_episode(model, state):
    while not model.has_won(state):
        a = model.e_greedy(state)
        state = model.update(state,a)

def cal_optimal_path(model, state):
    steps = 0
    while not model.has_won(state):
        a = model.e_greedy(state)
        state = GlobalParams.transit(state, a)
        print ("Current state: %s" % str(state))
        steps +=1
    return steps

# setting alpha to a low rate typically gives better results
model = Qmodel(0.002, 0.99, 0.05)
print ("Training")
for episode in range(500):
    state = GlobalParams.random_initialize()
    print ("Episode %s" % episode)
    print ("Start state: %s" % str(state))
    train_one_episode(model, state)


test_state = tuple([1,0,0,1,0,0,0,0,1])
print("Testing")
print (cal_optimal_path(model, test_state))
