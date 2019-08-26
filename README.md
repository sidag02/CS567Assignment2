# CS567Assignment2
This code covers the solution for Assignment 2 of CSCI 567- Fpundations of Artificial Intelligence offered during Fall 2018 at USC.
The problem was around gameplay with Max-Max strategy to optimize result for both the players.
The code uses classic branching technique to look at all the possible solutions in a tree form. The tree is accessed in a Depth First Manner.
Thhere was a small optimization to reduce the size of the tree.
The possible set of moves could be divided into 3 categories - Played by both players, Player 1 only, Player 2 only.
It was realized that choosing from the both player bin first did not make an impact to the overall final result.
However, it helped to reduce the size of the tree to bve traversed.
Also, because of this optimization, it was possible to store the state of possible solutions in a dictionary to avoid recomputing same result.

