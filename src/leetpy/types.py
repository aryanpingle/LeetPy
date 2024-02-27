from typing import List, Optional


# References:
# https://leetcode.com/problems/clone-graph/
class Node_Graph:
    """
    Used in graphs.
    NOTE: Leetcode refers to this as "Node"
    """

    def __init__(self, val=0, neighbors: List["Node_Graph"] = None):
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []


# References:
# https://leetcode.com/problems/add-two-numbers/
class ListNode:
    """
    Used in singly-linked lists.
    """

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
