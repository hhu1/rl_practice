# lights_out

This script implements a tabular Q-learning solution to the 3x3 lights out puzzle. <https://en.wikipedia.org/wiki/Lights_Out_(game)> It first does the training, and then test the model with a special test case.

# Random Walk Monte-Carlo and temporal difference

You have a line segments with length n (0, 1,..., n-1). The left and right side (0 and n-1) are the aborbing states. The question is, starting from a random place and talk left and right with equal probability, what is the probability of ending in 0 vs. (n-1)th position eventually?

