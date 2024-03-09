"""
Utility functions that let you debug data structures by printing them to the screen

Binary Tree Inspiration: https://github.com/miguelmota/ascii-binary-tree
"""

from typing import Optional, Dict, List
from rich import print as rich_print

from .types import TreeNode
from .algorithms import BinaryTreeAlgos as BTAlgos


def print_binary_tree(
    root: Optional[TreeNode],
    title: str = None,
    box_color: str = "magenta",
    line_color: str = "white",
):
    """
    Prints the rooted binary tree in a visually appealing format.

    Loosely based on the Reingold-Tilford Algorithm.
    """

    MIN_NODE_GAP = 3

    contours: Dict[TreeNode, dict] = {}

    def get_contour(root: Optional[TreeNode]) -> Optional[dict]:
        if root is None:
            return None

        # No children
        if (not root.left) and (not root.right):
            return {0: (0, 0)}

        # Only one child
        if (not root.left) or (not root.right):
            direction = 1 if root.right else -1
            contour_child = get_contour(root.left or root.right)

            level_count = len(contour_child)

            dist_between_children = MIN_NODE_GAP

            offset_distance = 1 + dist_between_children // 2

            contour = {0: (0, 0)}
            for level in range(level_count):
                leftmost = contour_child[level][0] + (direction * offset_distance)
                rightmost = contour_child[level][1] + (direction * offset_distance)
                contour[level + 1] = (leftmost, rightmost)

            contours[root] = contour
            return contour

        # confirmed: both children alive and kicking

        contour_left = get_contour(root.left)
        contour_right = get_contour(root.right)

        level_count = max(len(contour_left), len(contour_right))

        # The distance between roots needed so the two contours just touch each other
        max_hor_intersection = 0

        # Find the distance to keep them separated at
        for level in range(level_count):
            # One of the contours does not have this level
            # There won't be any possible intersections
            if (level not in contour_left) or (level not in contour_right):
                break

            # if both have this level, find the distance
            max_hor_intersection = max(
                max_hor_intersection,
                contour_left[level][1] - contour_right[level][0],
            )

        dist_between_children = max_hor_intersection + MIN_NODE_GAP

        offset_distance = 1 + dist_between_children // 2

        # Create the merged contour
        contour = {0: (0, 0)}
        for level in range(level_count):
            leftmost = 0
            rightmost = 0

            # Create left contour
            if level in contour_left:
                leftmost = contour_left[level][0] - offset_distance
            elif level in contour_right:
                leftmost = contour_right[level][0] + offset_distance

            # Create right contour
            if level in contour_right:
                rightmost = contour_right[level][1] + offset_distance
            elif level in contour_left:
                rightmost = contour_left[level][1] - offset_distance

            contour[level + 1] = (leftmost, rightmost)

        contours[root] = contour
        return contour

    get_contour(root)

    leftmost = min(contours[root][level][0] for level in contours[root])
    rightmost = max(contours[root][level][1] for level in contours[root])
    width = rightmost - leftmost + 1

    height = BTAlgos.get_depth(root)

    BLANK = "  "
    grid = [[BLANK] * (width) for _ in range(2 * height + 1)]

    # Print title
    if title:
        rich_print(f"[italic]{' '.join(['~', title, '~']):^{2*width}}[/]")
        print()

    def line_format(s: str):
        return f"[{line_color}]{s}[/]"

    def recursive_draw(root: Optional[TreeNode], x: int, depth: int):
        if root is None:
            return

        grid[2 * depth][x] = f"[{box_color}]██[/]"

        # If this is a leaf, exit
        if not root in contours:
            return

        contour = contours[root]
        (offset_left, offset_right) = contour[1]

        # Special case to accomodate straight line exceptions
        below_current = [" ", " "]

        if root.left:
            # Go left
            left_child_x = x + offset_left
            for i in range(left_child_x + 1, x):
                grid[2 * depth + 1][i] = line_format("──")

            if offset_left == -1:  # immediately to the left, use a straight line
                below_current[0] = "/"
            else:  # far away, use fancy lines
                below_current[0] = "┘"
                grid[2 * depth + 1][left_child_x] = " ┌"

            recursive_draw(root.left, left_child_x, depth + 1)

        if root.right:
            # Go right
            right_child_x = x + offset_right
            for i in range(x + 1, right_child_x):
                grid[2 * depth + 1][i] = line_format("──")

            if offset_right == +1:  # immediately to the right, use a straight line
                below_current[1] = r"\\"
            else:  # far away, use fancy lines
                below_current[1] = "└"
                grid[2 * depth + 1][right_child_x] = "┐ "

            recursive_draw(root.right, x + offset_right, depth + 1)

        # ┐┌┘└─
        grid[2 * depth + 1][x] = line_format("".join(below_current))

    recursive_draw(root, -leftmost, 0)

    rich_print("\n".join("".join(row) for row in grid))


def print_2d_array(arr: List[List[int]], title: Optional[str] = None):
    ROWS = len(arr)
    COLS = len(arr[0])

    # The size of the columns (based on the largest element)
    col_width = 1
    for row in range(ROWS):
        for col in range(COLS):
            entry_width = len(str(arr[row][col]))
            col_width = max(col_width, entry_width)
    col_width = max(col_width, len(str(COLS - 1)))

    # Size of the column showing row indices
    first_col_width = len(str(ROWS - 1))

    TABLE_WIDTH = first_col_width + ((col_width + 1) * COLS)

    if title is not None:
        rich_print(f"[italic]{' '.join(['~', title, '~']):^{TABLE_WIDTH}}[/]")
        print()

    INDEX_STYLE = "yellow"

    # Print column indices
    row__column_indices = "".join(
        [
            " " * first_col_width,
            " ",
            "│",
            f"[{INDEX_STYLE}]",  # begin style
            *[f" {col:^{col_width}}" for col in range(COLS)],
            f"[/]",  # end style
        ]
    )
    rich_print(row__column_indices)
    # Print horizontal grid line
    print(
        "─" * first_col_width,  # cover column containing indices of rows
        "─",  # spacing
        "┼",  # intersection of grid lines
        "─" * (COLS * (col_width + 1)),  # cover table columns (with spacing)
        sep="",
    )

    # Print rows
    for row_index in range(ROWS):
        # Print row indices
        rich_print(
            f"[{INDEX_STYLE}]{row_index:>{first_col_width}}[/]",
            " │ ",
            sep="",
            end="",
        )
        rich_print(*[f"{entry:^{col_width}}" for entry in arr[row_index]])
