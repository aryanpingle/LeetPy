"""
Algorithms and utility functions relating to Binary Trees
"""

from typing import Optional, List, Dict
from ..types import TreeNode


def travel_preorder(root: Optional[TreeNode]):
    if root is not None:
        yield root
        yield from travel_preorder(root.left)
        yield from travel_preorder(root.right)


def travel_inorder(root: Optional[TreeNode]):
    if root is not None:
        yield from travel_inorder(root.left)
        yield root
        yield from travel_inorder(root.right)


def travel_postorder(root: Optional[TreeNode]):
    if root is not None:
        yield from travel_postorder(root.left)
        yield from travel_postorder(root.right)
        yield root


def count_nodes(root: Optional[TreeNode]) -> int:
    if root == None:
        return 0
    return 1 + count_nodes(root.left) + count_nodes(root.right)


def get_depth(root: Optional[TreeNode]) -> int:
    """
    Returns the maximum depth/height of the given Binary Tree.
    For a single root node, the depth is 1.
    """
    if root == None:
        return 0
    return 1 + max(get_depth(root.left), get_depth(root.right))


def is_binary_search_tree(root: Optional[TreeNode]) -> bool:
    """
    Checks if the given Binary Tree satisfies the properties of a Binary Search Tree
    """

    def util(root, min_val, max_val) -> bool:
        if root == None:
            return True
        if root.val >= max_val or root.val <= min_val:
            return False
        return util(root.left, min_val, root.val) and util(
            root.right, root.val, max_val
        )

    return util(root, -float("inf"), float("inf"))


def count_leaf_nodes(root: Optional[TreeNode]) -> int:
    """
    Returns the number of leaf nodes in the given Binary Tree
    """
    count = [0]

    def util(root):
        if root == None:
            return
        if root.left or root.right:
            util(root.left)
            util(root.right)
        else:
            count[0] += 1

    util(root)
    return count[0]
