"""
Utility functions that let you debug data structures by printing them to the screen

Binary Tree Inspiration: https://github.com/miguelmota/ascii-binary-tree
"""

from rich import print as rich_print
from typing import Optional

from .types import TreeNode
from .algorithms import binary_tree as BTAlgos


# TODO: Needs MAJOR refactoring
# TODO: Not quite there yet. Need to research Layered Drawings more.
def print_binary_tree(root: Optional[TreeNode], key=lambda x: x.val):
    height = BTAlgos.get_depth(root)
    count = BTAlgos.count_nodes(root)

    BLANK = "  "

    def line_style(text: str) -> str:
        return f"[yellow]{text}[/]"

    UNDERLINE = line_style("__")

    # nodes and underscores at grid[2*depth]
    # slashes at grid[2*depth+1]
    grid = [[BLANK] * count for i in range(2 * height + 1)]

    v_slice = [0]

    def travel(root: Optional[TreeNode], depth: int):
        if root == None:
            return

        travel(root.left, depth + 1)

        # Add this node to grid
        slice = v_slice[0]
        grid[2 * depth][slice] = f"[on green]{BLANK}[/]"
        v_slice[0] += 1

        travel(root.right, depth + 1)

        # Add underlines to left
        if root.left:
            for i in range(slice - 1, -1, -1):
                below = grid[2 * (depth + 1)][i]
                if below == BLANK or below == UNDERLINE:
                    grid[2 * depth][i] = UNDERLINE
                else:
                    grid[2 * depth + 1][i] = line_style(" /")
                    break
        # Add underlines to right
        if root.right:
            for i in range(slice + 1, count):
                below = grid[2 * (depth + 1)][i]
                if below == BLANK or below == UNDERLINE:
                    grid[2 * depth][i] = UNDERLINE
                else:
                    grid[2 * depth + 1][i] = line_style("\ ")
                    break

    travel(root, 0)

    output = "\n".join(["".join(row) for row in grid])

    rich_print(output)
