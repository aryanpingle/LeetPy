from collections import deque
import json
import random
from typing import Deque, Dict, Iterable, Iterator, List, Optional, Set
from rich import print as rich_print

from ..types import ListNode


INT_MIN = -2147483648
INT_MAX = 2147483647


class LinkedList:
    """
    Algorithms and utility functions related to the Singly Linked List data structure. All
    functions are static and stateless.
    """

    @staticmethod
    def count_nodes(head: Optional[ListNode]) -> int:
        """
        Count the number of unique nodes in the linked list.

        NOTE: Cyclic references do not cause a problem.
        """

        seen: Set[ListNode] = set()
        count = 0
        for node in LinkedList.travel(head):
            if node in seen:
                break
            seen.add(node)
            count += 1
        return count

    @staticmethod
    def create(
        n: int,
        min_val: int = INT_MIN,
        max_val: int = INT_MAX,
        index_as_val: bool = False,
        choices: Iterable[any] = [],
    ) -> Optional[ListNode]:
        sentinel = ListNode(-1)
        tail = sentinel
        for i in range(n):
            data = None
            if index_as_val:
                data = i
            elif len(choices) >= 1:
                data = random.choice(choices)
            else:
                data = random.randint(min_val, max_val)

            node = ListNode(data)
            tail.next = node
            tail = node

        return sentinel.next

    @staticmethod
    def print(head: Optional[ListNode]):
        """
        Print the linked list to stdout in a visually appealing format.

        NOTE: Cyclic references do not cause a problem.
        """

        cycle_start_node = LinkedList.get_cyclic_node(head)

        seen: Set[LinkedList] = set()
        for node in LinkedList.travel(head):
            if node is None:
                break
            if node in seen:
                rich_print(f"[cyan]↺[/]", end=" ")
                break
            seen.add(node)

            if node is cycle_start_node:
                rich_print("[cyan]↺ →[/]", end=" ")
            print(node.val, end=" ")
            if node.next is not None:
                rich_print("[cyan]→[/]", end=" ")
        print()

    @staticmethod
    def get(head: Optional[ListNode], n: int) -> Optional[ListNode]:
        """
        Get the n'th node in the given linked list (0-based indexing). Negative indices
        will return nodes from the end of the linked list.

        NOTE: Cyclic references do not cause a problem. Negative indices start backwards
        from a path which does not contain a cycle.
        """

        N = LinkedList.count_nodes(head)

        if n < 0:
            n += N

        def _get(head: Optional[ListNode], n: int):
            if head is None:
                return None
            if n == 0:
                return head
            return _get(head.next, n - 1)

        return _get(head, n)

    @staticmethod
    def get_cyclic_node(head: Optional[ListNode]) -> Optional[ListNode]:
        """
        If a cycle exists, return the first node of the cycle in the linked list, or
        `None` otherwise.
        """

        if head == None:
            return None
        N = LinkedList.count_nodes(head)
        return LinkedList.get(head, N-1).next

    @staticmethod
    def is_cyclic(head: Optional[ListNode]) -> Optional[ListNode]:
        """Check whether there is a cyclic reference somewhere in the linked list."""
        return LinkedList.get_cyclic_node(head) is None

    @staticmethod
    def search(head: Optional[ListNode], value: any) -> Optional[ListNode]:
        """
        Search for a node that contains the given value, and return the first match if
        any.

        NOTE: Cyclic references do not cause a problem.
        """

        seen: Set[ListNode] = set()
        for node in LinkedList.travel(head):
            if node in seen:
                break
            seen.add(node)
            if node.val == value:
                return True
        return False

    @staticmethod
    def travel(head: Optional[ListNode]) -> Iterator[ListNode]:
        """
        Generator function that sequentially yields nodes of the linked list.

        NOTE: if a cycle exists, the iterator will keep yielding nodes infinitely.
        """

        if head is None:
            return
        yield head
        yield from LinkedList.travel(head.next)
