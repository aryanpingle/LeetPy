from typing import List, Optional


# References:
# https://leetcode.com/problems/clone-graph/
class Node_Graph:
    """
    Used in graphs.

    NOTE: Leetcode refers to this as "Node".
    """

    def __init__(self, val=0, neighbors: List["Node_Graph"] = None):
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []


# References:
# https://leetcode.com/problems/add-two-numbers/
class ListNode:
    """Used in singly-linked lists."""

    def __init__(self, val: any = 0, next: Optional["ListNode"] = None):
        self.val = val
        self.next = next


# References:
# https://leetcode.com/problems/flatten-a-multilevel-doubly-linked-list/
class Node_DLL:
    """
    Used in doubly-linked lists.

    NOTE: Leetcode refers to this as "Node"
    """

    def __init__(self, val, prev, next, child):
        self.val = val
        self.prev = prev
        self.next = next
        self.child = child


# References:
# https://leetcode.com/problems/binary-tree-inorder-traversal/
class TreeNode:
    """Used in binary trees."""

    def __init__(
        self,
        val: any = 0,
        left: Optional["TreeNode"] = None,
        right: Optional["TreeNode"] = None,
    ):
        self.val = val
        self.left = left
        self.right = right

    def __str__(self):
        """
        This string representation function is NOT provided by Leetcode. This is purely
        for your convenience.
        """
        left_str = None if self.left is None else f"Node({self.left.val})"
        right_str = None if self.right is None else f"Node({self.right.val})"
        return f"Node({self.val},L={left_str},R={right_str})"
