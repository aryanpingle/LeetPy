from collections import deque
import json
import random
import re as regex
from rich import print as rich_print
from typing import Deque, Iterator, List, Optional, Set, TypedDict, TypeVar, Type

from ._reingold_tilford_algorithm import TR_create_drawing, TR_Node


INT_MIN = -2147483648
INT_MAX = 2147483647


# Generic type for any object that represents a node in a binary tree
NodeLike = TypeVar("NodeLike")
"""
A generic type for any object that represents a node in a binary tree. It will have three
unique attributes: for its data, for its left child and for its right child.
"""

SupportsWrite = TypeVar("SupportsWrite")
"""
A generic type for any `.write()`-supporting file-like object."""


class NodeConfig(TypedDict):
    """
    A 1:1 mapping of the three attributes of a binary tree node to the corresponding
    attribute names in a custom node object.
    """

    data_attr: str
    left_attr: str
    right_attr: str


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
        root: Optional[NodeLike], config: NodeConfig = TreeNodeConfig
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
        klass: Type[NodeLike] = TreeNode,
        config: NodeConfig = TreeNodeConfig,
    ) -> Optional[NodeLike]:
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

        root = klass(random.randint(min_val, max_val))

        if index_as_val:
            setattr(root, config["data_attr"], 0)

        created_count = 1
        q: Deque[klass] = deque([root])
        while q and created_count < n:
            if make_complete:
                pass
            else:
                # Choose a random element to be the parent
                index = random.randint(0, len(q) - 1)
                q[index], q[0] = q[0], q[index]
            curr = q.popleft()

            # Create the new node
            new_node = klass(
                created_count if index_as_val else random.randint(min_val, max_val)
            )

            # Set it to the left or right child randomly
            child = random.randint(0, 1)
            if make_complete:  # override random child if 'make_complete' is enabled
                child = 0
            if child == 0:  # left first
                if getattr(curr, config["left_attr"]) is None:
                    setattr(curr, config["left_attr"], new_node)
                else:
                    setattr(curr, config["right_attr"], new_node)
            else:  # right first
                if getattr(curr, config["right_attr"]) is None:
                    setattr(curr, config["right_attr"], new_node)
                else:
                    setattr(curr, config["left_attr"], new_node)

            # Add the newly created node to the queue
            q.append(new_node)
            created_count += 1

            # If the parent isn't fully filled, add it to the queue
            if (
                getattr(curr, config["left_attr"]) is None
                or getattr(curr, config["right_attr"]) is None
            ):
                # appendleft only matters when 'make_complete' is enabled
                q.appendleft(curr)

        if make_bst:
            arr = [
                getattr(node, config["data_attr"])
                for node in BinaryTree.travel_inorder(root)
            ]
            arr.sort()
            i = 0
            for node in BinaryTree.travel_inorder(root):
                setattr(node, config["data_attr"], arr[i])
                i += 1

        return root

    @staticmethod
    def create_from_leetcode_array(
        leetcode_str: str,
        klass: Type[NodeLike] = TreeNode,
        config: NodeConfig = TreeNodeConfig,
    ) -> Optional[NodeLike]:
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

        root = klass(leetcode_arr[0])
        q = deque([root])
        is_left = True
        for val in leetcode_arr[1:]:
            node = None
            if val is not None:
                node = klass(val)

            if is_left:
                setattr(q[0], config["left_attr"], node)
            else:
                setattr(q[0], config["right_attr"], node)

            if node is not None:
                q.append(node)

            if not is_left:
                q.popleft()

            is_left = not is_left

        return root

    @staticmethod
    def equals(
        root1: Optional[NodeLike],
        root2: Optional[NodeLike],
        config1: NodeConfig = TreeNodeConfig,
        config2: NodeConfig = TreeNodeConfig,
    ) -> bool:
        """
        Check if the binary trees formed by two root nodes are equal in structure and
        data.

        Args:
            root1: The root node of the first binary tree.
            root2: The root node of the second binary tree.
            config1: A dictionary that maps the three attributes of `TreeNode` to the
                corresponding attribute names in `root1`. This is only needed if `root1`
                is not an instance of `TreeNode`.
            config2: A dictionary that maps the three attributes of `TreeNode` to the
                corresponding attribute names in `root2`. This is only needed if `root2`
                is not an instance of `TreeNode`.
        """

        if root1 is None and root2 is None:
            return True

        data1 = getattr(root1, config1["data_attr"])
        data2 = getattr(root2, config2["data_attr"])
        if data1 != data2:
            return False

        is_left_equal = BinaryTree.equals(
            getattr(root1, config1["left_attr"]),
            getattr(root2, config2["left_attr"]),
            config1,
            config2,
        )
        is_right_equal = BinaryTree.equals(
            getattr(root1, config1["right_attr"]),
            getattr(root2, config2["right_attr"]),
            config1,
            config2,
        )

        return is_left_equal and is_right_equal

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
    def export_as_code(
        root: Optional[NodeLike],
        source_config: NodeConfig = TreeNodeConfig,
        target_config: NodeConfig = TreeNodeConfig,
        indent: int = 4,
        function_name: str = "get_root",
        node_alias: str = "TreeNode",
        type_hints: bool = True,
        inline_args: bool = False,
    ) -> str:
        """
        Generate code for a Python3 function that returns the root of the given binary
        tree.

        Args:
            root: The root node of a binary tree.
            source_config: A dictionary that maps the three attributes of `TreeNode` to
                the corresponding attribute names in `root`. This is only needed if `root`
                is not an instance of `TreeNode`.
            target_config: A dictionary that maps the three attributes of `TreeNode` to
                the corresponding attribute names in the exported code. By default,
                TreeNode's definition of a binary tree node will be used.
            indent: The number of spaces to be used while indenting the function body.
            function_name: The name of the function in the generated code. (default =
                "get_root")
            node_alias: The name of the class used to create a node for the binary tree.
                (default = "TreeNode")
            type_hints: When enabled, the function code will have a Python3 return type
                declaration for the given node_alias. (example: `-> Optional[TreeNode]`)
            inline_args: When enabled, the children of any node will be directly passed to
                its constructor. Enable this only if your node class's constructor accepts
                the data, left child and right child in order. When disabled, children
                will be set using the dot notation (`obj.attribute`).
        """
        code__return_type = ""
        if type_hints:
            code__return_type = " -> " + ("None" if root is None else node_alias)
        code = f"def {function_name}(){code__return_type}:"

        if root is None:
            # (in code) return None
            code += "\n" + _indented("return None", indent)
            return code

        def get_node_repr(
            node: Optional[NodeLike],
            left: str = "None",
            right: str = "None",
        ) -> str:
            if node is None:
                return "None"
            data = getattr(node, source_config["data_attr"])
            if left == "None" and right == "None":
                return f"{node_alias}({data})"
            else:
                return f"{node_alias}({data}, {left}, {right})"

        N_ptr = [BinaryTree.count_nodes(root, source_config) - 1]

        # TODO: Switch to BinaryTree.travel_postorder instead of this recursive method
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

            if not inline_args:
                # Define this node
                code_lines.append(
                    _indented(f"{node_var} = {get_node_repr(node)}", indent)
                )
                # Define children
                if left_var != "None":
                    code_lines.append(
                        _indented(
                            f"{node_var}.{target_config['left_attr']} = {left_var}",
                            indent,
                        )
                    )
                if right_var != "None":
                    code_lines.append(
                        _indented(
                            f"{node_var}.{target_config['right_attr']} = {right_var}",
                            indent,
                        )
                    )
            else:
                # Define this node
                node_repr = get_node_repr(node, left_var, right_var)
                code_lines.append(_indented(f"{node_var} = {node_repr}", indent))

            return node_var

        code_lines = []
        root_var = travel(root, code_lines)
        # Add a comment containing the array representation (for convenience)
        array_repr = BinaryTree.export_as_leetcode_array(root, source_config)
        code += "\n" + _indented("# " + array_repr, indent)
        # Add all the lines of code creating nodes
        code += "\n" + "\n".join(code_lines)
        # Return the root node
        code += "\n" + _indented(f"return {root_var}", indent)

        return code

    @staticmethod
    def save_as_svg(
        root: Optional[TreeNode],
        fp: SupportsWrite,
        node_color: str = "transparent",
        stroke_color: str = "black",
    ):
        """
        Save a visualization of the given binary tree as an SVG illustration.

        Args:
            fp: A file pointer (or any `.write()`-implementing object).
            node_color: The background color of a node as a CSS-string.
            stroke_color: The color of edges and node outlines as a CSS-string.
        """
        TR_root = TR_create_drawing(root, "val", "left", "right", minimum_separation=1)

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

        ###################################
        #         SVG Calculations        #
        ###################################

        # TODO: Create a utility module for SVG stuff

        CELL_WIDTH = 100
        CELL_HEIGHT = 2 * CELL_WIDTH  # Terminal char height = 2*width

        SVG_VIEWBOX_LEFT = CELL_WIDTH * x_bounds[0]
        SVG_VIEWBOX_RIGHT = CELL_WIDTH * (x_bounds[1] + 1)
        SVG_VIEWBOX_UP = 0
        SVG_VIEWBOX_DOWN = CELL_HEIGHT * (y_bounds[1] + 1)

        SVG_WIDTH = SVG_VIEWBOX_RIGHT - SVG_VIEWBOX_LEFT
        SVG_HEIGHT = SVG_VIEWBOX_DOWN - SVG_VIEWBOX_UP

        NODE_RADIUS = min(CELL_WIDTH, CELL_HEIGHT) // 3
        EDGE_STROKE_WIDTH = (2 * NODE_RADIUS) * 0.05
        FONT_HEIGHT = NODE_RADIUS
        CHAR_WIDTH = FONT_HEIGHT / 2

        node_g = []  # A list of all SVGs that represent a node
        node_mask_g = []  # Copies of node_g used for masking
        text_g = []  # A list of all SVGs that represent a node's data
        edge_g = []  # A list of all SVGs that represent an edge

        def get_centered_text_svg(text: str, cx: int, cy: int) -> str:
            baseline_x = cx - (CHAR_WIDTH) * (len(text) / 2)
            baseline_y = cy + (FONT_HEIGHT / 2) * 0.8
            return f"""
            <text x="{baseline_x}" y="{baseline_y}" style="font-family: monospace;"
            font-size="{FONT_HEIGHT}">{text}</text>
            """

        def add_node_svg(data: any, x_coord: int, y_coord: int):
            cx = (x_coord * CELL_WIDTH) + (CELL_WIDTH / 2)
            cy = (y_coord * CELL_HEIGHT) + (CELL_HEIGHT / 2)
            node_g.append(
                f"""
                <ellipse cx="{cx}" cy="{cy}" rx="{NODE_RADIUS}" ry="{NODE_RADIUS}"
                fill="{node_color}" stroke="{stroke_color}"
                stroke-width="{EDGE_STROKE_WIDTH}">
                </ellipse>
                """
            )
            node_mask_g.append(
                f"""
                <ellipse cx="{cx}" cy="{cy}" rx="{NODE_RADIUS}" ry="{NODE_RADIUS}"
                fill="black" stroke="black" stroke-width="{EDGE_STROKE_WIDTH}">
                </ellipse>
                """
            )
            text_g.append(get_centered_text_svg(str(data), cx, cy))

        def add_edge_svg(x1: int, y1: int, x2: int, y2: int):
            x1 = (x1 * CELL_WIDTH) + (CELL_WIDTH / 2)
            x2 = (x2 * CELL_WIDTH) + (CELL_WIDTH / 2)
            y1 = (y1 * CELL_HEIGHT) + (CELL_HEIGHT / 2)
            y2 = (y2 * CELL_HEIGHT) + (CELL_HEIGHT / 2)
            edge_g.append(
                f"""
                <line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{stroke_color}"
                stroke-width="{EDGE_STROKE_WIDTH}"></line>
                """
            )

        def build_svg(node: TR_Node):
            if node is None:
                return

            # Build edge svg's
            if node.left is not None:
                add_edge_svg(
                    node.x_coord, node.y_coord, node.left.x_coord, node.left.y_coord
                )
            if node.right is not None:
                add_edge_svg(
                    node.x_coord, node.y_coord, node.right.x_coord, node.right.y_coord
                )

            # Build node svg
            add_node_svg(node.val, node.x_coord, node.y_coord)

            build_svg(node.left)
            build_svg(node.right)

        build_svg(TR_root)

        # This is used for the node mask
        background_rect_white = f"""
        <rect x="{SVG_VIEWBOX_LEFT}" y="{SVG_VIEWBOX_UP}" width="{SVG_WIDTH}"
        height="{SVG_HEIGHT}" fill="white"></rect>
        """

        code = f"""
        <svg
        version="1.1"
        viewBox="{SVG_VIEWBOX_LEFT} {SVG_VIEWBOX_UP} {SVG_WIDTH} {SVG_HEIGHT}"
        xmlns="http://www.w3.org/2000/svg">
          <mask id="node-mask-group">
            {background_rect_white}
            {''.join(node_mask_g)}
          </mask>
          <g id="leetpy-bt-edges" mask="url(#node-mask-group)">{''.join(edge_g)}</g>
          <g id="leetpy-bt-nodes">{''.join(node_g)}</g>
          <g id="leetpy-bt-node-texts">{''.join(text_g)}</g>
        </svg>
        """

        # Remove newlines and leading spaces in lines (for compression)
        code = regex.sub(r"\s*(\n\s*)+", " ", code)

        fp.write(code)

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
    def get_max_width(
        root: Optional[NodeLike], config: NodeConfig = TreeNodeConfig
    ) -> int:
        """
        The maximum number of nodes at any level of the given binary tree.

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

        widths = {}

        def dfs(root: Optional[NodeLike], depth: int) -> None:
            if root is None:
                return

            if not depth in widths:
                widths[depth] = 0
            widths[depth] += 1

            dfs(getattr(root, config["left_attr"]), depth + 1)
            dfs(getattr(root, config["right_attr"]), depth + 1)

        dfs(root, 0)

        return max(widths.values())

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
    def print_structure(root: Optional[NodeLike], config: NodeConfig = TreeNodeConfig):
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
