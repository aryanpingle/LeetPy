import random
from rich import print as rich_print
from typing import Iterable, List, Optional


INT_MIN = -2147483648
INT_MAX = 2147483647


class Array1D:
    """
    Algorithms and utility functions related to the 1-D Array data structure (a.k.a the
    List). All functions are static and stateless.
    """

    @staticmethod
    def create(
        n: int,
        min_val: int = INT_MIN,
        max_val: int = INT_MAX,
        index_as_val: bool = False,
        choices: Iterable = [],
    ):
        """
        Create a 1-D array based on the given parameters.

        If a list of choices is provided, a random choice is chosen for each entry value.
        Otherwise, entry values are randomly generated in the range [`min_val`,
        `max_val`].

        Args:
            n: The number of elements in the 1-D array.
            min_val: The minimum possible value of any randomly generated entry value.
            max_val: The maximum possible value of any randomly generated entry value.
            index_as_val: Enabling this sets entry values to the 0-based order in which
                they were created. Overrides `min_val` and `max_val`.
            choices: A list of possible entry values to be randomly chosen from.
        """
        arr = None
        if choices:
            arr = [random.choice(choices) for index in range(n)]
        else:
            arr = [
                (index if index_as_val else random.randint(min_val, max_val))
                for index in range(n)
            ]

        return arr

    @staticmethod
    def print(arr: List[any], title: Optional[str] = None):
        """Print the 1-D array with indices."""
        N = len(arr)

        # The size of the columns (based on the largest element)
        col_width = 1
        for index in range(N):
            entry_width = len(str(arr[index]))
            col_width = max(col_width, entry_width)
        col_width = max(col_width, len(str(N - 1)))

        if title is not None:
            TABLE_WIDTH = (N * col_width) + (N - 1)
            rich_print(f"[italic]{' '.join(['~', title, '~']):^{TABLE_WIDTH}}[/]")
            print()

        INDEX_STYLE = "yellow"

        # Print indices
        row__column_indices = (
            f"[{INDEX_STYLE}]"
            + " ".join([f"{index:^{col_width}}" for index in range(N)])
            + "[/]"
        )
        rich_print(row__column_indices)

        # Print horizontal grid line
        print("─" * ((N * col_width) + (N - 1)))

        # Print entries
        rich_print(*[f"{entry:^{col_width}}" for entry in arr])
