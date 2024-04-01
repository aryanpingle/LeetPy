"""
This is an extension to `binary_tree/example_2.py`.

The only difference here is that the custom node class accepts optional arguments for the
left and right child as well. If you pass `inline_args=True` to the `export_as_code`
function, leetpy takes advantage of these optional arguments to "inline" the children,
which reduces the number of generated lines.
"""


class MyNode:
    # Unlike in example 2, this constructor accepts optional args for children
    def __init__(self, data=0, left_child=None, right_child=None):
        self.data = data
        self.left_child = left_child
        self.right_child = right_child


from leetpy import BinaryTree
from random import randint

# Configuration options
# Only needed because we are using a custom node class instead of leetpy.TreeNode
config = {
    "data_attr": "data",
    "left_attr": "left_child",
    "right_attr": "right_child",
}

# Contents of the generated test file
file_contents = """
class MyNode:
    def __init__(self, data=0):
        self.data = data
        self.left_child = None
        self.right_child = None
""".strip()

for test_index in range(1, 11):
    num_nodes = randint(0, 100)

    root = BinaryTree.create(n=num_nodes, min_val=1, max_val=100)
    code = BinaryTree.export_as_code(
        root,
        target_config=config,  # The generated code should use the correct attribute names
        function_name=f"testcase_{test_index}",  # The generated function's name
        node_alias="MyNode",  # The generated code should call MyNode(...)
        inline_args=True,
    )

    file_contents += "\n\n" + code

with open("testcases.py", "w") as f:
    f.write(file_contents + "\n")
