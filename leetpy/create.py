"""
Utility functions that let you create randomized data structures like Binary Trees
"""

from collections import deque
import random
from typing import Deque, Iterable, Optional

from .algorithms import BinaryTreeAlgos as BTAlgos
from .types import TreeNode


INT_MIN = -2147483648
INT_MAX = 2147483647


def create_binary_tree(
    n: int,
    min_val: int = INT_MIN,
    max_val: int = INT_MAX,
    index_as_val: bool = False,
    make_complete: bool = False,
    make_bst: bool = False,
) -> Optional[TreeNode]:
    """Generates a rooted binary tree based on the parameters, and returns the root.
    Node values are randomly generated, except when `index_as_val` is enabled.

    Args:
        n: The number of nodes to be generated as part of the binary tree.
        min_val: The minimum possible value of any randomly generated node value.
        max_val: The maximum possible value of any randomly generated node value.
        index_as_val: Enabling this sets node values to the 0-based order in \
            which they were created. Overrides `min_val` and `max_val`.
        make_complete: Enabling this ensures the generated binary tree will \
            satisfy the properties of a Complete Binary Tree i.e. All levels \
            except the last will be filled to the end, and the last level will \
            be filled from left to right.
        make_bst: Enabling this ensures the generated binary tree will satisfy \
            the properties of a Binary Search Tree i.e. the inorder traversal of \
            node values yields a sorted array.
    """
    if n <= 0:
        return None

    root = TreeNode(random.randint(min_val, max_val))

    if index_as_val:
        root.val = 0

    created_count = 1
    q: Deque[TreeNode] = deque([root])
    while q and created_count < n:
        if make_complete:
            pass
        else:
            # Choose a random element to be the parent
            index = random.randint(0, len(q) - 1)
            q[index], q[0] = q[0], q[index]
        curr = q.popleft()

        # Create the new node
        new_node = TreeNode(
            created_count if index_as_val else random.randint(min_val, max_val)
        )

        # Set it to the left or right child randomly
        child = random.randint(0, 1)
        if make_complete:  # override random child if 'make_complete' is enabled
            child = 0
        if child == 0:  # left first
            if not (curr.left):
                curr.left = new_node
            else:
                curr.right = new_node
        else:  # right first
            if not (curr.right):
                curr.right = new_node
            else:
                curr.left = new_node

        # Add the newly created node to the queue
        q.append(new_node)
        created_count += 1

        # If the parent isn't fully filled, add it to the queue
        if not (curr.left and curr.right):
            # appendleft only matters when 'make_complete' is enabled
            q.appendleft(curr)

    if make_bst:
        arr = [i.val for i in BTAlgos.travel_inorder(root)]
        arr.sort()
        i = 0
        for node in BTAlgos.travel_inorder(root):
            node.val = arr[i]
            i += 1

    return root


def create_2d_array(
    rows: int,
    cols: int,
    min_val: int = INT_MIN,
    max_val: int = INT_MAX,
    index_as_val: bool = False,
    choices: Iterable = [],
):
    """Generates and returns a 2-dimensional array based on the given parameters.
    If a list `choices` is provided, a random choice is chosen for each cell value. \
    Otherwise, cell values are randomly generated in the range [`min_val`, `max_val`].
    
    Args:
        rows: The number of rows in the 2D array.
        cols: The number of columns in the 2D array.
        min_val: The minimum possible value of any randomly generated cell value.
        max_val: The maximum possible value of any randomly generated cell value.
        index_as_val: Enabling this sets cell values to the 0-based order in \
            which they were created. Overrides `min_val` and `max_val`.
        choices: A list of possible cell values to be randomly chosen from.
    """
    arr = None
    if choices:
        arr = [[random.choice(choices) for col in range(cols)] for row in range(rows)]
    else:
        arr = [
            [
                (row * cols + col if index_as_val else random.randint(min_val, max_val))
                for col in range(cols)
            ]
            for row in range(rows)
        ]

    return arr
