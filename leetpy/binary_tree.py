from collections import deque
import json
import random
from typing import Deque, Iterator, List, Optional, Set, TypedDict, TypeVar
from rich import print as rich_print

from ._reingold_tilford_algorithm import TR_create_drawing, TR_Node


INT_MIN = -2147483648
INT_MAX = 2147483647


# Generic type for any object that represents a node in a binary tree
NodeLike = TypeVar("NodeLike")
"""
A generic type for any object that represents a node in a binary tree. It will have three
unique attributes: for its data, for its left child and for its right child.
"""


# References:
# https://leetcode.com/problems/binary-tree-inorder-traversal/
class TreeNode:
    """A basic definition of a binary tree's node."""

    def __init__(
        self,
        val: any = 0,
        left: Optional["TreeNode"] = None,
        right: Optional["TreeNode"] = None,
    ):
        self.val = val
        self.left = left
        self.right = right


class NodeConfig(TypedDict):
    """
    A 1:1 mapping of the three attributes of a binary tree node to the corresponding
    attribute names in a custom node object.
    """

    data_attr: str
    left_attr: str
    right_attr: str


TreeNodeConfig: NodeConfig = {
    "data_attr": "val",
    "left_attr": "left",
    "right_attr": "right",
}
"""
The default node configuration, which represents an instance of `TreeNode`.
"""


def _indented(s: str, spaces: int):
    return " " * spaces + s


class BinaryTree:
    """
    Algorithms and utility functions related to the Binary Tree data structure. All
    functions are static and stateless.
    """

    @staticmethod
    def count_leaf_nodes(
        root: Optional[TreeNode], config: NodeConfig = TreeNodeConfig
    ) -> int:
        """Returns the number of leaf nodes in the given binary tree."""

        assert not BinaryTree.is_cyclic(
            root, config
        ), "Cycle detected while traveling from the root"

        count = [0]

        def _count_leaf_nodes(root):
            if root is None:
                return
            if getattr(root, config["left_attr"]) or getattr(
                root, config["right_attr"]
            ):
                _count_leaf_nodes(getattr(root, config["left_attr"]))
                _count_leaf_nodes(getattr(root, config["right_attr"]))
            else:
                count[0] += 1

        _count_leaf_nodes(root)
        return count[0]

    @staticmethod
    def count_nodes(
        root: Optional[NodeLike], config: NodeConfig = TreeNodeConfig
    ) -> int:
        assert not BinaryTree.is_cyclic(
            root, config
        ), "Cycle detected while traveling from the root"

        def _count_nodes(root: Optional[NodeLike]):
            if root is None:
                return 0

            return (
                1
                + _count_nodes(getattr(root, config["left_attr"]))
                + _count_nodes(getattr(root, config["right_attr"]))
            )

        return _count_nodes(root)

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
    def export_as_leetcode_array(
        root: Optional[NodeLike], config: NodeConfig = TreeNodeConfig
    ) -> str:
        """
        Generate a representation of the given rooted binary tree in Leetcode's testcase
        format.

        This representation can be directly pasted into a Leetcode custom testcase.

        Args:
            config: A dictionary that maps the three attributes of `TreeNode` to the
                corresponding attribute names in `root`. This is only needed if `root` is
                not an instance of `TreeNode`.
        """
        arr = []
        q = deque([root])
        while q:
            curr = q.popleft()

            if curr is None:
                arr.append("null")
                continue

            arr.append(str(getattr(curr, config["data_attr"])))
            q.append(getattr(curr, config["left_attr"]))
            q.append(getattr(curr, config["right_attr"]))

        # Get rid of redundant "null" nodes
        while arr and arr[-1] == "null":
            arr.pop()

        return "[" + ",".join(arr) + "]"

    @staticmethod
    def export_as_function(
        root: Optional[TreeNode],
        source_config: NodeConfig = TreeNodeConfig,
        target_config: NodeConfig = TreeNodeConfig,
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
            config: A dictionary that maps the three attributes of `TreeNode` to the
                corresponding attribute names in `root`. This is only needed if `root` is
                not an instance of `TreeNode`.
        """
        code__return_type = f" -> Optional[{node_alias}]" if type_hints else ""
        code = f"def {function_name}(){code__return_type}:"

        if root is None:
            # (in code) return None
            code += "\n" + _indented("return None", indent)
            return code

        def get_node_repr(node: Optional[NodeLike]) -> str:
            if node is None:
                return "None"
            data = getattr(node, source_config["data_attr"])
            return f"{node_alias}({data})"

        N_ptr = [BinaryTree.count_nodes(root, source_config) - 1]

        def travel(node: Optional[NodeLike], code_lines: List[str]) -> str:
            """
            Append this node's definition to `code_lines` and return this node's variable
            name.
            """
            if node is None:
                return "None"

            left_var = travel(getattr(node, source_config["left_attr"]), code_lines)
            right_var = travel(getattr(node, source_config["right_attr"]), code_lines)

            node_var = f"node_{N_ptr[0]}"
            N_ptr[0] -= 1

            # Define this node
            code_lines.append(_indented(f"{node_var} = {get_node_repr(node)}", indent))
            # Define children
            if left_var != "None":
                code_lines.append(_indented(
                    f"{node_var}.{target_config['left_attr']} = {left_var}", indent
                ))
            if right_var != "None":
                code_lines.append(_indented(
                    f"{node_var}.{target_config['right_attr']} = {right_var}", indent
                ))

            return node_var

        code_lines = []
        root_var = travel(root, code_lines)
        code += "\n" + "\n".join(code_lines)
        code += "\n" + _indented(f"return {root_var}", indent)

        return code

    @staticmethod
    def get_depth(root: Optional[NodeLike], config: NodeConfig = TreeNodeConfig) -> int:
        """
        Returns the maximum depth/height of the given binary tree. For a single root node,
        the depth is 1.

        Args:
            config: A dictionary that maps the three attributes of `TreeNode` to the
                corresponding attribute names in `root`. This is only needed if `root` is
                not an instance of `TreeNode`.
        """

        assert not BinaryTree.is_cyclic(
            root, config
        ), "Cycle detected while traveling from the root"

        if root is None:
            return 0
        return 1 + max(
            BinaryTree.get_depth(getattr(root, config["left_attr"]), config),
            BinaryTree.get_depth(getattr(root, config["right_attr"]), config),
        )

    @staticmethod
    def is_binary_search_tree(
        root: Optional[NodeLike], config: NodeConfig = TreeNodeConfig
    ) -> bool:
        """
        Check if the given Binary Tree satisfies the properties of the Binary Search Tree
        data structure.

        Args:
            config: A dictionary that maps the three attributes of `TreeNode` to the
                corresponding attribute names in `root`. This is only needed if `root` is
                not an instance of `TreeNode`.
        """

        assert not BinaryTree.is_cyclic(
            root, config
        ), "Cycle detected while traveling from the root"

        def util(root: Optional[NodeLike], min_val: any, max_val: any) -> bool:
            if root is None:
                return True

            root_data = getattr(root, config["data_attr"])

            if root_data >= max_val or root_data <= min_val:
                return False

            left_is_bst = util(
                getattr(root, config["left_attr"]),
                min_val,
                root_data,
            )
            right_is_bst = util(
                getattr(root, config["right_attr"]),
                root_data,
                max_val,
            )
            return left_is_bst and right_is_bst

        return util(root, -float("inf"), float("inf"))

    @staticmethod
    def is_cyclic(
        root: Optional[NodeLike], config: NodeConfig = TreeNodeConfig
    ) -> bool:
        """
        Check whether the graph formed from the given root contains a cyclic reference.

        Useful for verifying whether the given root actually forms a binary tree or not.

        Args:
            config: A dictionary that maps the three attributes of `TreeNode` to the
                corresponding attribute names in `root`. This is only needed if `root` is
                not an instance of `TreeNode`.
        """

        visited: Set[NodeLike] = set()

        for node in BinaryTree.travel_inorder(root, config):
            if node in visited:
                return True
            visited.add(node)

        return False

    @staticmethod
    def print_structure(root: Optional[TreeNode], config: NodeConfig = TreeNodeConfig):
        """
        Print the shape of the given rooted binary tree to the terminal.

        Args:
            config: A dictionary that maps the three attributes of `TreeNode` to the
                corresponding attribute names in `root`. This is only needed if `root` is
                not an instance of `TreeNode`.
        """

        TR_root = TR_create_drawing(
            root, config["data_attr"], config["left_attr"], config["right_attr"]
        )

        # Find the minimum and maximum x and y coordinates (grid bounds)
        x_bounds = [0, 0]
        y_bounds = [0, 0]

        def calculate_bounds(root: TR_Node):
            if root is None:
                return
            x_bounds[0] = min(x_bounds[0], root.x_coord)
            x_bounds[1] = max(x_bounds[1], root.x_coord)
            y_bounds[0] = min(y_bounds[0], root.y_coord)
            y_bounds[1] = max(y_bounds[1], root.y_coord)

            calculate_bounds(root.left)
            calculate_bounds(root.right)

        calculate_bounds(TR_root)

        # x-coordinates may be negative
        # increment them enough so that the leftmost is at x=0
        def increment_x(node: TR_Node, increment: int):
            if node is None:
                return
            node.x_coord += increment
            increment_x(node.left, increment)
            increment_x(node.right, increment)

        increment_x(TR_root, -x_bounds[0])

        height = y_bounds[1] - y_bounds[0] + 1
        width = x_bounds[1] - x_bounds[0] + 1

        # x-coordinates are literal
        # y-cordinates of nodes skip a level to allow for lines
        grid = [[" "] * width for _ in range(2 * height - 1)]

        # Relevant unicode characters
        # ─╱╲┴
        # ┐┘┌└
        # ╮╯╭╰

        def draw_node(TR_node: TR_Node):
            if TR_node is None:
                return

            x = TR_node.x_coord
            y = 2 * TR_node.y_coord
            offset = TR_node.offset

            # Draw the node
            grid[y][x] = "*"

            # Draw children recursively
            draw_node(TR_node.left)
            draw_node(TR_node.right)

            # Draw a line to the left node
            if TR_node.left:
                left_index = x - offset
                if offset == 2:  # Immediately to the left
                    grid[y + 1][left_index + 1] = "╱"
                else:  # Far to the left
                    for i in range(left_index + 1, x):
                        grid[y + 1][i] = "─"
                    grid[y + 1][x] = "┘"
                    grid[y + 1][left_index] = "┌"

            # Draw a line to the right node
            if TR_node.right:
                right_index = x + offset
                if offset == 2:  # Immediately to the right
                    grid[y + 1][right_index - 1] = "╲"
                else:  # Far to the right
                    for i in range(x + 1, right_index):
                        grid[y + 1][i] = "─"
                    grid[y + 1][x] = "└"
                    grid[y + 1][right_index] = "┐"

            if TR_node.left and TR_node.right and offset != 2:
                grid[y + 1][x] = "┴"

        draw_node(TR_root)

        # Print characters to screen
        print("╭", "─" * (width + 2), "╮", sep="")
        for row in grid:
            print("│", "".join(row), "│")
        print("╰", "─" * (width + 2), "╯", sep="")

    @staticmethod
    def print_leveled(root: Optional[NodeLike], config: NodeConfig = TreeNodeConfig):
        """
        Print an indented representation of a binary tree.

        There are other algorithms that are visually easier on the eyes, and have the same
        time complexity. The only benefit of this algorithm is that the code is easily
        readable, and can thus be trusted to always give the correct output.

        Args:
            config: A dictionary that maps the three attributes of `TreeNode` to the
                corresponding attribute names in `root`. This is only needed if `root` is
                not an instance of `TreeNode`.
        """

        assert not BinaryTree.is_cyclic(
            root
        ), "Cycle detected while traveling from the root"

        def _print__leveled(root: Optional[NodeLike], level: int):
            if root is None:
                return

            indent_string = " " * (2 * level)
            print(indent_string, getattr(root, config["data_attr"]), sep="")

            left_child = getattr(root, config["left_attr"])
            if left_child:
                _print__leveled(left_child, level + 1)
            else:
                rich_print(indent_string, "  ", "[italic]~ no left node[/]", sep="")

            right_child = getattr(root, config["right_attr"])
            if right_child:
                _print__leveled(right_child, level + 1)
            else:
                rich_print(indent_string, "  ", "[italic]~ no right node[/]", sep="")

        _print__leveled(root, 0)

    @staticmethod
    def search(
        root: Optional[NodeLike], val: any, config: NodeConfig = TreeNodeConfig
    ) -> Optional[NodeLike]:
        """
        Searches nodes in a binary tree for the given value in an inorder traversal.
        Returns the first node that contains the given value, or `None` if not found.

        Args:
            config: A dictionary that maps the three attributes of `TreeNode` to the
                corresponding attribute names in `root`. This is only needed if `root` is
                not an instance of `TreeNode`.
        """
        for node in BinaryTree.travel_inorder(root, config):
            if getattr(root, config["data_attr"]) == val:
                return node
        return None

    @staticmethod
    def travel_inorder(
        root: Optional[NodeLike], config: NodeConfig = TreeNodeConfig
    ) -> Iterator[NodeLike]:
        """
        Generator function that yields nodes in an inorder traversal (left -> root ->
        right).

        Args:
            config: A dictionary that maps the three attributes of `TreeNode` to the
                corresponding attribute names in `root`. This is only needed if `root` is
                not an instance of `TreeNode`.
        """
        if root is not None:
            yield from BinaryTree.travel_inorder(
                getattr(root, config["left_attr"]), config
            )
            yield root
            yield from BinaryTree.travel_inorder(
                getattr(root, config["right_attr"]), config
            )

    @staticmethod
    def travel_levelorder(
        root: Optional[NodeLike], config: NodeConfig = TreeNodeConfig
    ) -> Iterator[NodeLike]:
        """
        Generator function that yields nodes in a levelorder traversal (left to right for
        each level in the binary tree).

        Args:
            config: A dictionary that maps the three attributes of `TreeNode` to the
                corresponding attribute names in `root`. This is only needed if `root` is
                not an instance of `TreeNode`.
        """
        q = deque([root])
        while q:
            curr = q.popleft()

            yield curr

            left_child = getattr(root, config["left_attr"])
            if left_child:
                q.append(left_child)
            right_child = getattr(root, config["right_attr"])
            if right_child:
                q.append(right_child)

    @staticmethod
    def travel_postorder(
        root: Optional[NodeLike], config: NodeConfig = TreeNodeConfig
    ) -> Iterator[NodeLike]:
        """
        Generator function that yields nodes in a postorder traversal (left -> right ->
        root).

        Args:
            config: A dictionary that maps the three attributes of `TreeNode` to the
                corresponding attribute names in `root`. This is only needed if `root` is
                not an instance of `TreeNode`.
        """
        if root is not None:
            yield from BinaryTree.travel_postorder(
                getattr(root, config["left_attr"]), config
            )
            yield from BinaryTree.travel_postorder(
                getattr(root, config["right_attr"]), config
            )
            yield root

    @staticmethod
    def travel_preorder(
        root: Optional[NodeLike], config: NodeConfig = TreeNodeConfig
    ) -> Iterator[NodeLike]:
        """
        Generator function that yields nodes in an preorder traversal (root -> left ->
        right).

        Args:
            config: A dictionary that maps the three attributes of `TreeNode` to the
                corresponding attribute names in `root`. This is only needed if `root` is
                not an instance of `TreeNode`.
        """
        if root is not None:
            yield root
            yield from BinaryTree.travel_preorder(
                getattr(root, config["left_attr"]), config
            )
            yield from BinaryTree.travel_preorder(
                getattr(root, config["right_attr"]), config
            )
