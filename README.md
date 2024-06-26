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

**`LeetPy`** offers a wide range of utility functions - for a wide range of data structures. For a comprehensive list of usage examples, check out [/examples/README.md](./examples/README.md).

## Development

**`LeetPy`** has plans to support the following data structures:

- [X] 1-D Arrays
- [X] 2-D Arrays
- [X] Binary Trees
- [X] Singly Linked Lists
- [ ] Doubly Linked Lists
- [ ] Undirected Graphs (Weighted + Unweighted)
- [ ] Directed Graphs (Weighted + Unweighted)

All data structures have some common API's:

- `create() -> structure` - To create the structure with random data and properties based on certain parameters
- `export_as_code(structure) -> str` - To get an independent Python3 function that when called, returns the given data structure
- `export_as_svg(structure) -> None` - To create an SVG file with a visualization of the given data structure
- `print(structure) -> None` - To print a representation of the data structure to the terminal
