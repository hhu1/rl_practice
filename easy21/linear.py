from easy21 import Game
import random
import numpy as np

class Linear:
    def __init__(self, lamb):
        self.all_states = set()
        self.all_states_actions = set()
        self.w = np.array([0.0 for i in range(36)])

        for player_sum in range(1,22):
            for dealer_first in range(1,11):
                self.all_states.add((dealer_first, player_sum))
                for action in range(0,2):
                    self.all_states_actions.add(((dealer_first, player_sum), action))

        self.game= Game()
        self.lamb = lamb

    def Q(self, state, action):
        return (self.encode(state, action) * self.w).sum()
        
    def take_one_step(self, state):
        epsilon = 0.05

        val0 = self.Q(state, 0)
        val1 = self.Q(state, 1)

        action = None
        if random.random() < epsilon:
            if random.random() < 0.5:
                action =1
            else:
                action =0
        else:
            if val0 > val1:
                action = 0
            else:
                action = 1

        s, r = self.game.step(state, action)

        return (s, r, action)

    def encode(self, state, action):
        index = -1
        features = [0 for i in range(36)]

        for dealer_range in [[1,4], [4,7], [7,10]]:
            for player_range in [[1,6],[4,9],[7,12],[10,15],[13,18],[16,21]]:
                for action_range in [0,1]:
                    index +=1
                    if (state[0] >=dealer_range[0] and state[0] <=dealer_range[1]
                            and state[1] >=player_range[0] and state[1] <=player_range[1]
                            and action == action_range):
                        features[index] = 1
        return np.array(features)

    def run_one_episode(self):
        state = self.game.new_game_state()

        # OMG! E becomes a freezing vector! Isn't that adorable ?!!
        E = np.array([0 for i in range(36)])

        while True:
            new_state, reward, action    = self.take_one_step(state)

            estimated_return = None

            if new_state[1] ==-1:
                estimated_return = reward
            else:
                new_state2, reward2, action2 = self.take_one_step(new_state)
                estimated_return = self.Q(new_state, action2)

            delta = estimated_return - self.Q(state, action)

            E = self.lamb * E + self.encode(state, action)
            self.w += 0.01 * delta * E

            if new_state[1] ==-1:
                break
            else:
                state = new_state

    def create_Q(self):
        Q = {}
        for SA in self.all_states_actions:
            Q[SA] = self.Q(SA[0], SA[1])
        return Q

    def train(self, N):
        for i in range(N):
            self.run_one_episode()


if __name__ == '__main__':
    sec = Linear(0.5)
    sec.train(50000)
    sec.game.to_file(sec.create_Q(), "Q_linear.txt")
