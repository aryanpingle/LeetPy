import random
from typing import Iterable, Iterator, List, Optional, Set
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
        """
        Create a linked list based on the given parameters.

        Args:
            n: The number of nodes to be generated as part of the linked list.
            min_val: The minimum possible value of any randomly generated node value.
            max_val: The maximum possible value of any randomly generated node value.
            index_as_val: Enabling this sets node values to the 0-based order in which
                they were created. Overrides `min_val` and `max_val`.
            choices: A list of possible node values to be randomly chosen from.
        """

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
    def create_from_array(array: Iterable[any]) -> Optional[ListNode]:
        """Create a linked list where every node contains an element of the array."""

        sentinel = ListNode(-1)

        head = sentinel
        for value in array:
            head.next = ListNode(value)
            head = head.next

        return sentinel.next

    @staticmethod
    def export_as_function(
        head: Optional[ListNode],
        indent: int = 4,
        function_name: str = "get_head",
        node_alias: str = "ListNode",
        type_hints: bool = True,
    ) -> str:
        """
        Generate code for a Python3 function that returns the head of the given linked
        list.

        Args:
            head: The head of a linked list.
            indent: The number of spaces to be used while indenting the function body.
            function_name: The name of the function in the generated code. (default =
                "get_head")
            node_alias: The name of the class used to create a node for the linked list.
                (default = "ListNode")
            type_hints: When enabled, the function code will have a Python3 return type
                declaration for the given node_alias. (example: `-> Optional[ListNode]`)
        """

        code__return_type = f" -> Optional[{node_alias}]" if type_hints else ""
        code__func_signature = f"def {function_name}(){code__return_type}:"

        if head is None:
            return "\n".join([code__func_signature, " " * indent + "return None"])

        def get_node_repr(node: Optional[ListNode]) -> str:
            if node is None:
                return "None"
            return f"{node_alias}({node.val})"

        N = LinkedList.count_nodes(head)

        code__func_body = []

        # Create the first node (index 0)
        code__func_body.append(f"node_0 = {get_node_repr(head)}")

        node_to_index = {head: 0}
        for i in range(1, N):
            head = head.next
            # Create the new node
            code__func_body.append(f"node_{i} = {get_node_repr(head)}")
            node_to_index[head] = i
            # Justify its existence
            code__func_body.append(f"node_{i-1}.next = node_{i}")

        # head is now the last node

        # Create the cyclic reference, if any
        if LinkedList.is_cyclic(head):
            code__func_body.append(f"# cyclic dependency")
            code__func_body.append(f"node_{N-1}.next = node_{node_to_index[head.next]}")

        code__func_body.append("return node_0")  # Return statement

        return "\n".join(
            [
                code__func_signature,
                *[" " * indent + line for line in code__func_body],
            ]
        )

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
        return LinkedList.get(head, N - 1).next

    @staticmethod
    def is_cyclic(head: Optional[ListNode]) -> Optional[ListNode]:
        """Check whether there is a cyclic reference somewhere in the linked list."""
        return LinkedList.get_cyclic_node(head) is not None

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
    def search(head: Optional[ListNode], value: any) -> Optional[ListNode]:
        """
        Search for a node that contains the given value, and return the first match if
        any.

        NOTE: Cyclic references do not cause a problem.
        """

        N = LinkedList.count_nodes(head)

        for _ in range(N):
            if head.val == value:
                return True

        return False

    @staticmethod
    def to_array(head: Optional[ListNode]) -> List[ListNode]:
        """
        Return a list of unique nodes in the linked list.

        NOTE: Cyclic references do not cause a problem.
        """

        N = LinkedList.count_nodes(head)
        array = [None] * N

        for i in range(N):
            array[i] = head
            head = head.next

        return array

    @staticmethod
    def travel(head: Optional[ListNode]) -> Iterator[ListNode]:
        """
        Generator function that sequentially yields nodes of the linked list.

        NOTE: if a cycle exists, the iterator will keep yielding nodes infinitely.
        """

        while head is not None:
            yield head
            head = head.next
