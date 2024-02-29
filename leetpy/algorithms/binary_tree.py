"""
Algorithms and utility functions relating to Binary Trees
"""

from typing import Optional, List, Dict
from leetpy.types import TreeNode


def count_nodes(root: Optional[TreeNode]) -> int:
    if root == None:
        return 0
    return 1 + count_nodes(root.left) + count_nodes(root.right)


def get_depth(root: Optional[TreeNode]) -> int:
    if root == None:
        return 0
    return 1 + max(get_depth(root.left), get_depth(root.right))


def is_binary_search_tree(root: Optional[TreeNode]) -> bool:
    def util(root, min_val, max_val) -> bool:
        if root == None:
            return True
        if root.val >= max_val or root.val <= min_val:
            return False
        return util(root.left, min_val, root.val) and util(
            root.right, root.val, max_val
        )

    return util(root, -float("inf"), float("inf"))
