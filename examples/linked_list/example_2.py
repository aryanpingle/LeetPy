"""
Create a randomized AND CYCLIC singly linked list with 20 UNIQUE nodes and visualize it.
"""

from leetpy import LinkedList
from random import randint

head = LinkedList.create(n=20)  # create a random linked list with 20 nodes

# form a cycle by connecting the last node with some other random node
last = LinkedList.get(head, 19)  # get the last node
last.next = LinkedList.get(head, randint(0, 18))

LinkedList.print(head)  # visualize the binary tree

"""
(random) Output:
-1630827585 → 696861798 → -7286643 → -1291323604 → 893615702 → 98480058 → -1483119591 → 2065341134 → -81388430 → ↺ → -567954753 → -69891826 → -241908785 → 1399909508 → -1114291183 → 1480827252 → -1193702890 → -1596154928 → 1986679451 → 531716373 → -1910042243 → ↺
"""
