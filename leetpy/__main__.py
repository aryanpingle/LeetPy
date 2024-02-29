import argparse
import json
from pkg_resources import resource_string
from rich import prompt
from rich import print as rich_print
from rich.table import Table
from rich.console import Console
from typing import TypedDict, List, Dict

from .questions import QuestionMetadata


class MetaData(TypedDict):
    question_count: int
    topics: List[str]
    difficulty_count: Dict[str, int]
    paid_count: int


def search_and_display(
    search_term: str,
    search_topics: List[str],
    search_difficulties: List[str],
    limit_results: int,
):
    # Preprocess search params
    search_term = search_term.strip().lower()
    search_topics = search_topics
    search_difficulties = [difficulty.lower() for difficulty in search_difficulties]

    # Load questions
    questions: List[QuestionMetadata] = json.loads(
        resource_string(__name__, "info/per-question-metadata.json")
    )

    filtered = [True] * len(questions)
    scores = [0] * len(questions)

    # Filter by difficulty
    if search_difficulties:
        for i in range(len(questions)):
            if not filtered[i]:
                continue
            question = questions[i]

            if not question["difficulty"] in search_difficulties:
                filtered[i] = False

    # Filter by topics
    if search_topics:
        for i in range(len(questions)):
            if not filtered[i]:
                continue
            question = questions[i]

            if not all([topic in question["topics"] for topic in search_topics]):
                filtered[i] = False

    # Filter by search term
    if search_term:
        for i in range(len(questions)):
            if not filtered[i]:
                continue
            question = questions[i]

            if search_term in question["title"].lower():
                scores[i] = 3
            elif search_term in question["description"].lower():
                scores[i] = 2
            else:
                # Doesn't contain the search term
                filtered[i] = False

    result_indices = [i for i in range(len(questions)) if filtered[i]]
    result_indices.sort(key=lambda i: scores[i], reverse=True)

    result_count = min(limit_results, len(result_indices))

    # If there are no results, break
    if result_count == 0:
        print("No search results found.")
        return

    # If there are too many results, ask user if he wants to view them all
    RESULT_THRESHOLD = 20
    if result_count > RESULT_THRESHOLD:
        confirmation = prompt.Confirm.ask(
            f"{result_count} results found. Do you wish to view them all?"
        )

        if not confirmation:
            return

    # Start creating the results table
    table = Table(
        title=f"{result_count} Search Result" + ("" if result_count == 1 else "s"),
        show_lines=True,
    )

    table.add_column("ID", style="bold cyan")
    table.add_column("Title", style="green")
    table.add_column("Topics")
    table.add_column(
        "Link",
        style="blue",
        no_wrap=True,
    )

    # Add entries to results table
    for i in range(result_count):
        question_idx = result_indices[i]
        if not filtered[question_idx]:
            continue
        question = questions[question_idx]

        question_url = "https://leetcode.com/problems/" + question["title_slug"]
        table.add_row(
            str(question["id"]),
            question["title"],
            " * ".join([f"[bold magenta]{topic}[/]" for topic in question["topics"]]),
            question_url,
        )

    # Print the results table
    console = Console()
    console.print(table)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="leetpy", description="The best DSA helper")

    # Add arguments
    parser.add_argument(
        "-s",
        "--search",
        action="store",
        default="",
        help="Filter questions by searching for a phrase (case-insensitive)",
    )
    parser.add_argument(
        "-t",
        "--topics",
        action="extend",
        nargs="*",
        default=[],
        type=str,
        help="Filter questions by choosing 1 or more topics",
    )
    parser.add_argument(
        "-d",
        "--difficulties",
        action="extend",
        nargs="*",
        default=[],
        type=str,
        choices=["easy", "medium", "hard"],
        help="Filter questions by choosing 1 or more levels of difficulty",
    )
    parser.add_argument(
        "-n",
        "--limit-results",
        action="store",
        help="Limit the number of results",
        type=int,
    )
    parser.add_argument(
        "--summary",
        action="store_true",
        help="Display statistics about Leetcode questions",
    )
    parser.add_argument(
        "-l",
        "--list-topics",
        action="store_true",
        help="Display the list of Leetcode topics",
    )
    args = parser.parse_args()

    # Load metadata
    metadata: MetaData = json.loads(resource_string(__name__, "info/meta.json"))

    # Show summary statistics
    if args.summary:
        total_questions = metadata["question_count"]
        paid_questions = metadata["paid_count"]
        free_questions = total_questions - paid_questions

        rich_print("Number of questions =", total_questions)
        rich_print("Number of free questions =", free_questions)
        rich_print("Number of paid only questions =", paid_questions)
        rich_print("")

        for difficulty, count in metadata["difficulty_count"].items():
            rich_print(f"Number of [green]{difficulty}[/] questions =", count)

        exit(0)

    # Show the list of topics
    if args.list_topics:
        formatted_result = [f"[bold magenta]{topic}[/]" for topic in metadata["topics"]]
        rich_print(" * ".join(formatted_result))

        exit(0)

    # Search with the given params
    if args.search or args.topics or args.difficulties or args.limit_results:
        # Set default value of args.limit_results
        if args.limit_results == None:
            args.limit_results = 10_000
        # Clean up topics
        if args.topics:
            args.topics = [
                topic.title()
                for topic in args.topics
                if topic.title() in metadata["topics"]
            ]

        search_and_display(
            args.search, args.topics, args.difficulties, args.limit_results
        )

        exit(0)

    parser.print_help()
