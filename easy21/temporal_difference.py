from easy21 import Game
import random

class TemporalDifference:
    def __init__(self, lamb):
        Nsa = {}
        Ns  = {}
        Q   = {}

        for player_sum in range(1, 22):
            for dealer_first in range(1, 11):
                state = (dealer_first, player_sum)
                Ns[state] = 0
                for action in range(0,2):
                    Nsa[(state, action)] = 0
                    Q[(state, action)] = 0.0

        self.Nsa = Nsa
        self.Ns  = Ns
        self.Q   = Q
        self.game= Game()
        self.N0  = 100.0
        self.lamb = lamb

    def take_one_step(self, state):
        epsilon = self.N0 / (self.N0 + self.Ns[state])

        val0 = self.Q[(state, 0)]
        val1 = self.Q[(state, 1)]

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

        return (s,r, action)

    def run_one_episode(self):
        state = self.game.new_game_state()
        E = {}
        for SA in self.Q:
            E[SA] = 0.0

        while True:
            new_state, reward, action    = self.take_one_step(state)

            estimated_return = None

            if new_state[1] ==-1:
                estimated_return = reward
            else:
                new_state2, reward2, action2 = self.take_one_step(new_state)
                estimated_return = self.Q[(new_state, action2)]

            delta = estimated_return - self.Q[(state, action)]

            E[(state, action)] +=1
            self.Nsa[(state, action)] += 1.0

            for SA in self.Q:
                if E[SA]  >0.0:
                    alpha = 1.0 / self.Nsa[SA]
                    self.Q[SA] += alpha * delta * E[SA]
                    E[SA] *= self.lamb

            if new_state[1] ==-1:
                break
            else:
                state = new_state

    def train(self, N):
        for i in range(N):
            self.run_one_episode()


if __name__ == '__main__':
    sec = TemporalDifference(0.5)
    sec.train(50000)
    sec.game.to_file(sec.Q, "Q_td.txt")
    
