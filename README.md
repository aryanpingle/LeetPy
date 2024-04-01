[![LeetPy Banner](https://raw.githubusercontent.com/aryanpingle/LeetPy/master/static/images/LeetPy%20Banner.png)](https://github.com/aryanpingle/LeetPy)

> Debugging is twice as hard as writing the code in the first place.

If you solve problems related to Data Structures & Algorithms (DSA), you know how frustrating it is to debug complex data structures like Binary Trees and Directed Graphs.

**`LeetPy`** is a lightweight Python package that makes you more efficient when you solve DSA problems. It contains utility functions and algorithms that make debugging and testing *SO MUCH* easier. Here are some features:

- **Several Data Structures**: Binary Trees, Linked Lists, 2-D Arrays, etc.
- **Visualize Your Objects**: **`LeetPy`** provides convenient `print()` functions that show you what your structure looks like (all inside your terminal!).
- **Save & Export**: Serialization and export functions help you save an exact copy of your structure, and give you the code to generate them from scratch.
- **Flexibility**: Create your data structure *however* you want; **`LeetPy`**'s algorithms will always work correctly.

## Installation

To install the latest stable release, run:

```bash
$ pip install leetpy
```

To install from the latest GitHub commit:

```bash
pip install git+https://github.com/aryanpingle/leetpy
```

## Usage & Examples

Here's a minimal use-case:

```python
# Create a random binary tree and visualize it

from leetpy import BinaryTree

root = BinaryTree.create(n=20)  # create a random binary tree with 20 nodes
BinaryTree.print_structure(root)  # visualize the binary tree
```

And here's a complex one:

```python
# Suppose you want to 'save' 10 binary search trees (example: for testing purposes)
# You would need some Python code that generates each tree exactly

from leetpy import BinaryTree

for i in range(1, 11):
    # Generate a random binary search tree (BST) with 20 nodes
    # Each node should have a value between 1 and 10 (inclusive)
    root = BinaryTree.create(n=20, min_val=1, max_val=10, make_bst=True)
    
    # Get the python code that generates this exact BST
    # Oh, and make each node an object of class "CustomNode"
    # Oh, and keep indentation to 2 spaces
    code += "\n" + BinaryTree.export_as_code(root, node_alias="CustomNode", indent=2)

with open("testing.py", "w") as f:
    f.write(code)
```

**`LeetPy`** offers a wide range of utility functions - for a wide range of data structures. Here's a comprehensive list of examples:

|Example|Description|
|---|---|
|[Binary Tree Example 1](./examples/binary_tree/example_1.py)|Create a randomized binary tree with 20 nodes and visualize it.|
|[Binary Tree Example 2](./examples/binary_tree/example_2.py)|Generate a file which contains code for creating randomized binary trees with some constraints (without dependending on the leetpy package).|
|[Binary Tree Example 3](./examples/binary_tree/example_3.py)|Same as example 2, but with inlined generated code (reducing the number of generated lines).|
|[Linked List Example 1](./examples/linked_list/example_1.py)|Create a randomized singly linked list with 20 nodes and visualize it.|
|[Linked List Example 2](./examples/linked_list/example_2.py)|Create a randomized AND CYCLIC singly linked list with 20 UNIQUE nodes and visualize it.|
