"""
In some coding challenge, contestants must perform some operation on the root node of a
binary tree.

Constraints:
    * Each node is an instance of class `MyNode`
    * The number of nodes in the tree is in the range [0, 100]
    * -100 <= Node.val <= 100

Here is a way to automate the creation of 10 test binary trees for this problem.
"""


class MyNode:
    def __init__(self, data=0):
        self.data = data
        self.left_child = None
        self.right_child = None


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
    )

    file_contents += "\n\n" + code

with open("testcases.py", "w") as f:
    f.write(file_contents + "\n")
