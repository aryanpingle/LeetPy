from collections import deque
import json
import random
from typing import Deque, List, Optional

from ..algorithms import BinaryTreeAlgos as BTAlgos
from ..types import TreeNode


INT_MIN = -2147483648
INT_MAX = 2147483647


class BinaryTree:
    @staticmethod
    def create(
        n: int,
        min_val: int = INT_MIN,
        max_val: int = INT_MAX,
        index_as_val: bool = False,
        make_complete: bool = False,
        make_bst: bool = False,
    ) -> Optional[TreeNode]:
        """
        Generates a rooted binary tree based on the parameters, and returns the root.
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

    @staticmethod
    def import_from_leetcode_array(leetcode_str: str) -> Optional[TreeNode]:
        """
        Creates a rooted binary tree from the given Leetcode testcase format and \
        returns its root.

        In the Leetcode format, a level-order traversal is followed where direct \
        children of non-null nodes must always be specified. i.e. "null" denotes \
        that the parent node has a null node as its left/right child. Children of \
        null nodes are omitted.

        Example:
            `import_from_leetcode_array("[1,null,2,null,3]")`
        """

        leetcode_arr: List[Optional[int]] = json.loads(leetcode_str)

        if len(leetcode_arr) == 0:
            return None

        root = TreeNode(leetcode_arr[0])
        q = deque([root])
        is_left = True
        for val in leetcode_arr[1:]:
            node = None
            if val is not None:
                node = TreeNode(val)

            if is_left:
                q[0].left = node
            else:
                q[0].right = node
            if node:
                q.append(node)

            if not is_left:
                q.popleft()

            is_left = not is_left

        return root

    @staticmethod
    def export_as_function(
        root: Optional[TreeNode],
        indent: int = 4,
        function_name: str = "get_root",
        node_alias: str = "TreeNode",
        type_hints: bool = True,
    ) -> str:
        """
        Generates and returns the code for a Python3 function that creates the given \
        rooted binary tree.
        
        Args:
            root: The root node of a binary tree.
            indent: The number of spaces to be used while indenting the function body.
            function_name: The name of the function in the generated code. \
                (default = "get_root") 
            node_alias: The name of the class used to create a node for the binary \
                tree. (default = "TreeNode")
            type_hints: When enabled, the function code will have a Python3 return \
                type declaration for the given node_alias. \
                (example: `-> Optional[TreeNode]`)
        """
        code__return_type = f" -> Optional[{node_alias}]" if type_hints else ""
        code__func_signature = f"def {function_name}(){code__return_type}:"

        if root is None:
            return "\n".join([code__func_signature, " " * indent + "return None"])

        def get_node_repr(node: Optional[TreeNode]) -> str:
            if node is None:
                return "None"
            return f"{node_alias}({node.val})"

        code__setter_lines = []
        internal_node_reprs: List[str] = []
        internal_node_index = [0]

        def travel(node: Optional[TreeNode], is_left_child: bool, parent_idx: int):
            if node == None:
                return

            if node.left or node.right:
                # Internal node
                curr_index = internal_node_index[0]
                internal_node_index[0] += 1

                if parent_idx != -1:
                    setter_line = (
                        f"nodes[{parent_idx}]."
                        + ("left" if is_left_child else "right")
                        + " = "
                        + f"nodes[{curr_index}]"
                    )
                    code__setter_lines.append(setter_line)

                # Add its repr to be declared in the array
                internal_node_reprs.append(get_node_repr(node))

                travel(node.left, True, curr_index)
                travel(node.right, False, curr_index)

                return

            # Leaf node
            if parent_idx != -1:
                setter_line = (
                    f"nodes[{parent_idx}]."
                    + ("left" if is_left_child else "right")
                    + " = "
                    + get_node_repr(node)
                )
                code__setter_lines.append(setter_line)

        travel(root, False, -1)

        # statement to declare array of nodes
        code__declare_array = "nodes = [" + ", ".join(internal_node_reprs) + "]"
        # statement to return nodes[0] (the root)
        code__return_statement = "return nodes[0]"

        # unindented function body lines
        function_body_lines = [
            code__declare_array,
            *code__setter_lines,
            code__return_statement,
        ]

        return "\n".join(
            [
                code__func_signature,
                *[" " * indent + line for line in function_body_lines],
            ]
        )

    @staticmethod
    def export_as_leetcode_array(root: Optional[TreeNode]) -> str:
        """
        Returns the Leetcode array representation of the given rooted binary tree.

        This representation can be directly pasted into a Leetcode custom testcase.
        """
        arr = []
        q = deque([root])
        while q:
            curr = q.popleft()

            if curr is None:
                arr.append("null")
                continue

            arr.append(str(curr.val))
            q.append(curr.left)
            q.append(curr.right)

        # Get rid of redundant "null" nodes
        while arr and arr[-1] == "null":
            arr.pop()

        return "[" + ",".join(arr) + "]"
