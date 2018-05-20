import re,os,sys,glob,random
import pandas as pd
import numpy as np

class Game:
    def __init__(self):
        return

    def step(self, s, a):
        ''' Takes a state (tuple of dealer's first card and player's sum 1-21), and
            an action (hit 1 or stick 0), and returns a sample of the next state s_prime
            (player's sum will be -1 if it is terminal) and reward r.
        '''

        if a == 0:
            # player stick
            dealer_val = self.dealer_round(s[0])

            if dealer_val ==-1 or dealer_val < s[1]:
                # player wins
                return ((s[0], -1), 1)
            elif dealer_val ==s[1]:
                # draw
                return ((s[0], -1), 0)
            else:
                # lose
                return ((s[0], -1), -1)
        else:
            # player hit
            player_val = s[1] + self.draw_card()
            if player_val >21 or player_val < 1:
                # busted
                return ((s[0], -1), -1)
            else:
                # not busted
                return ((s[0], player_val), 0)


    def dealer_round(self, first):
        ''' takes a first card of the deal and returns the dealer's final counts (-1 if busted)
        '''

        total = first
        while total <=21 and total >=1:
            total += self.draw_card()

            if total >=17: break

        if total >21 or total < 1: total = -1
        return total

    def draw_card(self):
        return random.randint(1,10) * (1.0 if random.random()<2.0/3.0 else -1.0)

    def new_game_state(self):
        ''' return an initial state for a new game
        '''
        return (random.randint(1,10), random.randint(1,10))

    def to_file(self, Q, out_file):
        V = {}
        for SA in Q:
            if SA[0] not in V:
                V[SA[0]] = Q[SA]
            else:
                V[SA[0]] = max(Q[SA], V[SA[0]])

        dealer = [s[0] for s in V]
        player = [s[1] for s in V]
        returns= [V[s] for s in V]

        df = pd.DataFrame({"D":dealer, "P":player, "R":returns})
        df.sort_values(by=["P", "D"], axis=0, inplace=True)

        df.to_csv(out_file,sep='\t', header=True, index=False)
