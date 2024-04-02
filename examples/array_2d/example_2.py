"""
Create a randomized 2-D array (10 rows x 5 columns) where elements are chosen randomly
from "X" and "O" and visualize it.
"""

from leetpy import Array2D

root = Array2D.create(rows=10, cols=5, choices=["X", "O"])  # create a random 2-D array
Array2D.print(root)  # visualize the array

"""
(random) Output:
  │ 0 1 2 3 4
──┼──────────
0 │ O X O X O
1 │ O X X X X
2 │ O O X X X
3 │ O O X X X
4 │ X X O O O
5 │ O X X X X
6 │ O O X X X
7 │ O X O O O
8 │ X O O O O
9 │ X O X O X
"""
