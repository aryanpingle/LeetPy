"""
Create a randomized 1-D array with 5 elements using a list of choices and visualize it.
"""

from leetpy import Array1D

root = Array1D.create(
    n=5, choices=["Aryan", "Pingle", "Genius", "God"]
)  # create a random 1-D array with 5 elements using a list of choices
Array1D.print(root)  # visualize the array

"""
(random) Output:
  0      1      2      3      4   
──────────────────────────────────
 God   Genius  God   Genius Aryan
"""
