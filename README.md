# Small grids world

In a N x N grids, top left corner (0,0) is the escape (absorbing state). Every time, you can only take one step to left, right, up, or down directoin, and the reward for doing this is -1. The goal is to calculate the return of each position in this grid world.

The implemented solution is a value iteration method which is a special case of dynamic programming implementation.

# Lights Out

This script implements a tabular Q-learning solution to the 3x3 lights out puzzle. <https://en.wikipedia.org/wiki/Lights_Out_(game)> It first does the training, and then test the model with a special test case.

# Random Walk Monte-Carlo and temporal difference

You have a line segments with length n (0, 1,..., n-1). The left and right side (0 and n-1) are the aborbing states. Starting somewhere in the line  and walk to left and right with equal probability, what is the probability of ending up being absorbed at (n-1)-th position?

# Easy 21.

Using TD(lambda), Monte-Carlo and linear approximation TD(lambda) to solve a variation of blackjack game called easy 21. Find more details about the programming task in the easy21 folder.
