from collections import deque
import json
import random
from typing import Deque, List, Optional
from rich import print as rich_print

from ..types import TreeNode


INT_MIN = -2147483648
INT_MAX = 2147483647


class BinaryTree:
    """
    Algorithms and utility functions related to the Binary Tree data structure. All
    functions are static and stateless.
    """

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

    @staticmethod
    def count_nodes(root: Optional[TreeNode]) -> int:
        if root == None:
            return 0
        return (
            1 + BinaryTree.count_nodes(root.left) + BinaryTree.count_nodes(root.right)
        )

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
        Create a rooted binary tree based on the parameters.

        Args:
            n: The number of nodes to be generated as part of the binary tree.
            min_val: The minimum possible value of any randomly generated node value.
            max_val: The maximum possible value of any randomly generated node value.
            index_as_val: Enabling this sets node values to the 0-based order in which
                they were created. Overrides `min_val` and `max_val`.
            make_complete: Enabling this ensures the generated binary tree will satisfy
                the properties of a Complete Binary Tree i.e. All levels except the last
                will be filled to the end, and the last level will be filled from left to
                right.
            make_bst: Enabling this ensures the generated binary tree will satisfy the
                properties of a Binary Search Tree i.e. the inorder traversal of node
                values yields a sorted array.
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
            arr = [i.val for i in BinaryTree.travel_inorder(root)]
            arr.sort()
            i = 0
            for node in BinaryTree.travel_inorder(root):
                node.val = arr[i]
                i += 1

        return root

    @staticmethod
    def create_from_leetcode_array(leetcode_str: str) -> Optional[TreeNode]:
        """
        Create a rooted binary tree from a string in Leetcode's testcase format.

        In the Leetcode format, a level-order traversal is followed where direct children
        of non-null nodes must always be specified. i.e. "null" denotes that the parent
        node has a null node as its left/right child. Children of null nodes are omitted.

        Example:
            `create_from_leetcode_array("[1,null,2,null,3]")`
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
    def export_as_leetcode_array(root: Optional[TreeNode]) -> str:
        """
        Generate a representation of the given rooted binary tree in Leetcode's testcase
        format.

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

    @staticmethod
    def export_as_function(
        root: Optional[TreeNode],
        indent: int = 4,
        function_name: str = "get_root",
        node_alias: str = "TreeNode",
        type_hints: bool = True,
    ) -> str:
        """
        Generate code for a Python3 function that returns the root of the given binary
        tree.

        Args:
            root: The root node of a binary tree.
            indent: The number of spaces to be used while indenting the function body.
            function_name: The name of the function in the generated code. (default =
                "get_root")
            node_alias: The name of the class used to create a node for the binary tree.
                (default = "TreeNode")
            type_hints: When enabled, the function code will have a Python3 return type
                declaration for the given node_alias. (example: `-> Optional[TreeNode]`)
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
    def get_depth(root: Optional[TreeNode]) -> int:
        """
        Returns the maximum depth/height of the given binary tree. For a single root node,
        the depth is 1.
        """
        if root == None:
            return 0
        return 1 + max(
            BinaryTree.get_depth(root.left), BinaryTree.get_depth(root.right)
        )

    @staticmethod
    def is_binary_search_tree(root: Optional[TreeNode]) -> bool:
        """
        Checks if the given Binary Tree satisfies the properties of the Binary Search Tree
        data structure.
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
    def print_leveled(root: Optional[TreeNode], data_attr_name: str = "val"):
        """
        Print an indented representation of a binary tree.

        There are other algorithms that are visually easier on the eyes, and have the same
        time complexity. The only benefit of this algorithm is that the code is easily
        readable, and can thus be trusted to always give the correct output.

        Args:
            data_attr_name: The name of the attribute storing the node's data. Useful in
                situations where you pass a custom node definition.
        """
        def _print__leveled(root: Optional[TreeNode], level: int):
            if root is None:
                return

            indent_string = " " * (2 * level)
            print(indent_string, f"{getattr(root, data_attr_name)}", sep="")

            if root.left:
                _print__leveled(root.left, level + 1)
            else:
                rich_print(indent_string, "  ", "[italic]~ no left node[/]", sep="")

            if root.right:
                _print__leveled(root.right, level + 1)
            else:
                rich_print(indent_string, "  ", "[italic]~ no right node[/]", sep="")
        _print__leveled(root, 0)

    @staticmethod
    def search(root: Optional[TreeNode], val: any) -> Optional[TreeNode]:
        """
        Searches nodes in a binary tree for the given value in an inorder traversal.
        Returns the first node that contains the given value, or `None` if not found.
        """
        for node in BinaryTree.travel_inorder(root):
            if node.val == val:
                return node
        return None

    @staticmethod
    def travel_inorder(root: Optional[TreeNode]):
        """
        Generator function that yields nodes in an inorder traversal (left -> root ->
        right).
        """
        if root is not None:
            yield from BinaryTree.travel_inorder(root.left)
            yield root
            yield from BinaryTree.travel_inorder(root.right)

    @staticmethod
    def travel_levelorder(root: Optional[TreeNode]):
        """
        Generator function that yields nodes in a levelorder traversal (left to right for
        each level in the binary tree).
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
    def travel_postorder(root: Optional[TreeNode]):
        """
        Generator function that yields nodes in a postorder traversal (left -> right ->
        root).
        """
        if root is not None:
            yield from BinaryTree.travel_postorder(root.left)
            yield from BinaryTree.travel_postorder(root.right)
            yield root

    @staticmethod
    def travel_preorder(root: Optional[TreeNode]):
        """
        Generator function that yields nodes in an preorder traversal (root -> left ->
        right).
        """
        if root is not None:
            yield root
            yield from BinaryTree.travel_preorder(root.left)
            yield from BinaryTree.travel_preorder(root.right)
