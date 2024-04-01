"""Create a randomized binary tree with 20 nodes and visualize it."""

from leetpy import BinaryTree

root = BinaryTree.create(n=20)  # create a random binary tree with 20 nodes
BinaryTree.print_structure(root)  # visualize the binary tree

"""
(random) Output:
╭───────────────────────────╮
│              *            │
│       ┌──────┴──────┐     │
│       *             *     │
│   ┌───┴───┐        ╱      │
│   *       *       *       │
│  ╱ ╲     ╱ ╲     ╱ ╲      │
│ *   *   *   *   *   *     │
│    ╱   ╱   ╱   ╱     ╲    │
│   *   *   *   *       *   │
│                      ╱ ╲  │
│                     *   * │
│                        ╱  │
│                       *   │
╰───────────────────────────╯
"""
