"""
An implementation of the tree drawing algorithm as outlined in the paper, "Tidier Drawings
of Trees" by Edward M. Reingold & John S. Tilford.

Paper: https://reingold.co/tidier-drawings.pdf

Further Reading: https://llimllib.github.io/pymag-trees/
"""

from typing import Optional

from leetpy.types import TreeNode


MINIMUM_SEPARATION = 3


class TR_Node:
    """
    A node class to represent the nodes of the binary tree.
    """

    def __init__(self, val: any = 0):
        self.val: any = val
        self.left: Optional[TR_Node] = None  # Left child
        self.right: Optional[TR_Node] = None  # Right child
        self.x_coord: int = 0  # Absolute x-coordinate
        self.y_coord: int = 0  # Absolute y-coordinate
        self.offset: int = 0  # Offset of either child
        self.has_thread: bool = False  # Is the left or right child a thread pointer?


class TR_Extreme:
    """
    A node class to represent the leftmost and rightmost nodes of a subtree.
    """

    def __init__(self):
        self.node: Optional[TR_Node] = None
        self.offset: int = 0
        self.level: int = 0

    def set(self, other):
        self.node = other.node
        self.offset = other.offset
        self.level = other.level


def TR_setup(
    T: Optional[TR_Node],
    LEVEL: int,
    RMOST: TR_Extreme,
    LMOST: TR_Extreme,
    MINIMUM_SEPARATION: int = 3,
):
    if T is None:
        LMOST.level = -1
        RMOST.level = -1
    else:
        T.y_coord = LEVEL

        L = T.left
        R = T.right

        # Create pointers
        LL, LR, RL, RR = TR_Extreme(), TR_Extreme(), TR_Extreme(), TR_Extreme()

        TR_setup(L, LEVEL + 1, LR, LL)
        TR_setup(R, LEVEL + 1, RR, RL)

        if R is None and L is None:  # Leaf
            RMOST.node = T
            RMOST.level = LEVEL
            RMOST.offset = 0
            LMOST.node = T
            LMOST.level = LEVEL
            LMOST.offset = 0
            T.offset = 0
        else:  # T is not a leaf
            # Set up for subtree pushing. Place
            # roots of subtrees minimum distance apart

            CURSEP = MINIMUM_SEPARATION
            ROOTSEP = MINIMUM_SEPARATION
            LOFFSUM = 0
            ROFFSUM = 0

            # Now consider each level in turn until one subtree is exhausted,
            # pushing the subtrees apart when necessary.

            while L is not None and R is not None:
                if CURSEP < MINIMUM_SEPARATION:
                    ROOTSEP = ROOTSEP + (MINIMUM_SEPARATION - CURSEP)
                    CURSEP = MINIMUM_SEPARATION

                # Advance L & R
                if L.right is not None:
                    LOFFSUM = LOFFSUM + L.offset
                    CURSEP = CURSEP - L.offset
                    L = L.right
                else:
                    LOFFSUM = LOFFSUM - L.offset
                    CURSEP = CURSEP + L.offset
                    L = L.left

                if R.left is not None:
                    ROFFSUM = ROFFSUM - R.offset
                    CURSEP = CURSEP - R.offset
                    R = R.left
                else:
                    ROFFSUM = ROFFSUM + R.offset
                    CURSEP = CURSEP + R.offset
                    R = R.right

            # set the offset in node T and include it in accumulated offsets for L and R
            T.offset = (ROOTSEP + 1) // 2
            LOFFSUM = LOFFSUM - T.offset
            ROFFSUM = ROFFSUM + T.offset

            # Update extreme descendents' information

            if RL.level > LL.level or T.left is None:
                LMOST.set(RL)
                LMOST.offset = LMOST.offset + T.offset
            else:
                LMOST.set(LL)
                LMOST.offset = LMOST.offset - T.offset

            if LR.level > RR.level or T.right is None:
                RMOST.set(LR)
                RMOST.offset = RMOST.offset - T.offset
            else:
                RMOST.set(RR)
                RMOST.offset = RMOST.offset + T.offset

            # If subtrees of T were of uneven heights
            # Check to see if threading is necessary
            # At most one thread needs to be inserted

            if L is not None and L is not T.left:
                RR.node.has_thread = True
                RR.node.offset = abs((RR.offset + T.offset) - LOFFSUM)
                if LOFFSUM - T.offset <= RR.offset:
                    RR.node.left = L
                else:
                    RR.node.right = L
            elif R is not None and R is not T.right:
                LL.node.has_thread = True
                LL.node.offset = abs((LL.offset - T.offset) - ROFFSUM)
                if ROFFSUM + T.offset >= LL.offset:
                    LL.node.right = R
                else:
                    LL.node.left = R
        # endif T is not leaf
    # endif T is not None


def TR_petrify(T: Optional[TR_Node], XPOS: int):
    """
    Perform a preorder traversal of the tree, converting the relative offsets to absolute
    coordinates.
    """

    if T is None:
        return

    T.x_coord = XPOS
    if T.has_thread:
        T.has_thread = False
        T.right = None
        T.left = None
    TR_petrify(T.left, XPOS - T.offset)
    TR_petrify(T.right, XPOS + T.offset)


def _TR_create_tree_copy(root: Optional[TreeNode]) -> Optional[TR_Node]:
    """
    Create a deep copy of the given binary tree root, where every node object is replaced
    by its `TR_Node` counterpart.
    """
    if root is None:
        return None

    TR_root = TR_Node(root.val)
    TR_root.left = _TR_create_tree_copy(root.left)
    TR_root.right = _TR_create_tree_copy(root.right)
    return TR_root


def TR_create_drawing(
    root: Optional[TreeNode], minimum_separation: int = 3
) -> Optional[TR_Node]:
    """
    Create a copy of the given binary tree with coordinates for each node on a 2-D plane.
    """

    TR_root = _TR_create_tree_copy(root)
    TR_setup(TR_root, 0, TR_Extreme(), TR_Extreme(), minimum_separation)
    TR_petrify(TR_root, 0)
    return TR_root
