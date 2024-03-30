[![LeetPy Banner](https://raw.githubusercontent.com/aryanpingle/LeetPy/master/static/images/LeetPy%20Banner.png)](https://github.com/aryanpingle/LeetPy)

> Debugging is twice as hard as writing the code in the first place.

If you solve problems related to Data Structures & Algorithms (DSA), you know how frustrating it is to debug complex data structures like Binary Trees and Directed Graphs.

**`LeetPy`** is a lightweight Python package that makes you more efficient when you solve DSA problems. It contains utility functions and algorithms that make debugging and testing *SO MUCH* easier. Here are some features:

- **Several Data Structures**: Binary Trees, Linked Lists, 2-D Arrays, etc.
- **Visualize Your Objects**: **`LeetPy`** provides convenient `print()` functions that show you what your structure looks like (all inside your terminal!).
- **Save & Export**: Serialization and export functions help you save an exact copy of your structure, and give you the code to generate them from scratch.
- **Flexibility**: Create your data structure *however* you want; **`LeetPy`**'s algorithms will always work correctly.

## Usage & Examples

Consider debugging the Binary Tree data structure:

```python
from leetpy import BinaryTree

# from leetpy import TreeNode
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

# Randomly generate the root of a binary tree
root: TreeNode = BinaryTree.create(n=20, min_val=1, max_val=10)
# Or, import it from a serialized array (like on Leetcode)
root: TreeNode = BinaryTree.create_from_leetcode_array("[1,2,3,4,null,null,5]")

# Count the number of nodes in the binary tree
print(BinaryTree.count_nodes(root))
# Print all the nodes of the binary tree
for node in BinaryTree.travel_inorder(root):
    print(node)
# Visualize the structure of the binary tree
BinaryTree.print_structure(root)
```

**`LeetPy`** offers a wide range of utility functions - for a wide range of data structures.

## Installation

To install the latest stable release, run:

```bash
$ pip install leetpy
```

To install from the latest GitHub commit:

```bash
pip install git+https://github.com/aryanpingle/leetpy
```
