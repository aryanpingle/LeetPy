import random
from rich import print as rich_print
from typing import Iterable, List, Optional, Tuple


INT_MIN = -2147483648
INT_MAX = 2147483647


class Array2D:
    """
    Algorithms and utility functions related to the 2-D Array data structure (a.k.a the
    Matrix). All functions are static and stateless.
    """

    @staticmethod
    def count(arr: List[List[any]]):
        """The number of cells in the given 2-D array."""
        return len(arr) * len(arr[0])

    @staticmethod
    def create(
        rows: int,
        cols: int,
        min_val: int = INT_MIN,
        max_val: int = INT_MAX,
        index_as_val: bool = False,
        choices: Iterable = [],
    ):
        """
        Create a 2-D array based on the given parameters.

        If a list of choices is provided, a random choice is chosen for each cell value.
        Otherwise, cell values are randomly generated in the range [`min_val`, `max_val`].

        Args:
            rows: The number of rows in the 2-D array.
            cols: The number of columns in the 2-D array.
            min_val: The minimum possible value of any randomly generated cell value.
            max_val: The maximum possible value of any randomly generated cell value.
            index_as_val: Enabling this sets cell values to the 0-based order in which
                they were created. Overrides `min_val` and `max_val`.
            choices: A list of possible cell values to be randomly chosen from.
        """
        arr = None
        if choices:
            arr = [
                [random.choice(choices) for col in range(cols)] for row in range(rows)
            ]
        else:
            arr = [
                [
                    (
                        row * cols + col
                        if index_as_val
                        else random.randint(min_val, max_val)
                    )
                    for col in range(cols)
                ]
                for row in range(rows)
            ]

        return arr

    @staticmethod
    def print(arr: List[List[any]], title: Optional[str] = None):
        """Print the 2-D array with row and column indices."""
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

        if title is not None:
            TABLE_WIDTH = first_col_width + 1 + (1 + (col_width + 1) * COLS)
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

    @staticmethod
    def search(arr: List[List[any]], val: any) -> Optional[Tuple[int]]:
        """
        Search the 2-D array for the given value from left-to-right, and top-to-bottom.

        Returns the 0-based coordinates of the first cell that contains the given value,
        or `None` if not found.
        """
        ROWS = len(arr)
        COLS = len(arr[0])
        for row_index in range(ROWS):
            for col_index in range(COLS):
                if arr[row_index][col_index] == val:
                    return (row_index, col_index)
        return None

    @staticmethod
    def travel(arr: List[List[any]]) -> any:
        """Yield the elements of the 2-D array from left-to-right, and top-to-bottom."""
        ROWS = len(arr)
        COLS = len(arr[0])
        for row_index in range(ROWS):
            for col_index in range(COLS):
                yield arr[row_index][col_index]
