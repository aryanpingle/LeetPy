"""
This module provides algorithms and utility functions for various data structures.

Todo:
    * For module TODOs
"""

from collections import deque
from typing import Optional

from .types import TreeNode


class BinaryTreeAlgos:
    """
    Contains algorithms and utility functions relating to the Binary Tree data structure.
    All functions are static and stateless.
    """

    @staticmethod
    def travel_preorder(root: Optional[TreeNode]):
        """
        Generator function that yields nodes in an preorder traversal (root -> left -> right).
        """
        if root is not None:
            yield root
            yield from BinaryTreeAlgos.travel_preorder(root.left)
            yield from BinaryTreeAlgos.travel_preorder(root.right)

    @staticmethod
    def travel_inorder(root: Optional[TreeNode]):
        """
        Generator function that yields nodes in an inorder traversal (left -> root -> right).
        """
        if root is not None:
            yield from BinaryTreeAlgos.travel_inorder(root.left)
            yield root
            yield from BinaryTreeAlgos.travel_inorder(root.right)

    @staticmethod
    def travel_postorder(root: Optional[TreeNode]):
        """
        Generator function that yields nodes in a postorder traversal (left -> right -> root).
        """
        if root is not None:
            yield from BinaryTreeAlgos.travel_postorder(root.left)
            yield from BinaryTreeAlgos.travel_postorder(root.right)
            yield root

    @staticmethod
    def travel_levelorder(root: Optional[TreeNode]):
        """
        Generator function that yields nodes in a levelorder traversal (left to right for each level in the binary tree).
        """
        q = deque([root])
        while q:
            curr = q.popleft()
            yield curr
            if curr.left:
                q.append(curr.left)
            if curr.right:
                q.append(curr.right)

    @staticmethod
    def count_nodes(root: Optional[TreeNode]) -> int:
        if root == None:
            return 0
        return (
            1
            + BinaryTreeAlgos.count_nodes(root.left)
            + BinaryTreeAlgos.count_nodes(root.right)
        )

    @staticmethod
    def get_depth(root: Optional[TreeNode]) -> int:
        """
        Returns the maximum depth/height of the given binary tree.
        For a single root node, the depth is 1.
        """
        if root == None:
            return 0
        return 1 + max(
            BinaryTreeAlgos.get_depth(root.left), BinaryTreeAlgos.get_depth(root.right)
        )

    @staticmethod
    def is_binary_search_tree(root: Optional[TreeNode]) -> bool:
        """
        Checks if the given Binary Tree satisfies the properties of the Binary Search Tree data structure.
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

    @staticmethod
    def count_leaf_nodes(root: Optional[TreeNode]) -> int:
        """
        Returns the number of leaf nodes in the given binary tree.
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
