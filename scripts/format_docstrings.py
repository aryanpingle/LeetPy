"""Formats the docstrings in a file."""

import ast
from rich import prompt
from typing import List, Tuple
import sys
import re

MAX_LINE_LENGTH = 90
DEFAULT_INDENT = 4


def format_paragraph(
    paragraph: str,
    max_line_length: int,
    indent: int = 0,
    additional_indent: int = 0,
) -> List[str]:
    """
    Break a single line of multiple sentences into a list of lines that fit into a certain
    number of characters.

    Args:
        indent: The number of spaces to indent each line.
        additional_indent: Lines after the first will be further indented by this number
            of spaces.
    """

    assert max_line_length >= 0
    assert indent >= 0
    assert additional_indent >= 0

    result: List[str] = [""]
    if indent:
        # Start off with indentation
        result = [" " * (indent - 1)]

    for word in paragraph.split():
        # Try to add this word to the last line
        # If it can't fit, create a new line and put it there

        if len(result[-1]) + 1 + len(word) > max_line_length:
            # `word` can't fit, add it to a new line
            result.append((" " * indent) + (" " * additional_indent) + word)
        else:
            # word can fit
            if len(result[-1]) == 0:  # first word of the line
                result[-1] += word
            else:
                result[-1] += " " + word

    return result


def format_docstring(docstring: str, code_indent: int) -> List[str]:
    # Remove leading and trailing spaces and newlines
    # print(f"/*/*/*/*/*/*/*")
    # print(docstring)
    docstring = docstring.lstrip("\n ")

    # split by newlines
    og_docstring_lines: List[str] = docstring.splitlines()

    # Remove unnecessary leading spaces caused by code-level indentation
    # Some mf's might screw up the indentation *within* the docstring,
    # so remove all leading spaces if it's lesser than the code-level indent.
    for i in range(len(og_docstring_lines)):
        og_line = og_docstring_lines[i]
        leading_space_count = 0
        for c in og_line:
            if c != " ":
                break
            leading_space_count += 1
            if leading_space_count == code_indent:
                break
        og_docstring_lines[i] = og_line[leading_space_count:]
    og_docstring_lines.append("")

    for i in range(len(og_docstring_lines)):
        og_docstring_lines[i] = og_docstring_lines[i].rstrip()

    flattened = "\n".join(og_docstring_lines)

    formatted_docstring = ""

    # regex__normal = r"((?:.+\n)+\n)"
    regex__normal = r"((?:.+\n)+\n*)"
    regex__section = r"^(([\s\w]+):\n+(?:\s{4,}.+\n+)+)"
    regex__blank = r"\n+"

    i = 0
    while i < len(flattened):
        substring = flattened[i:]
        # rich_print(f"[cyan]Searching '{substring[:10]}...':")

        # Blank Lines
        matched = re.match(regex__blank, substring, re.MULTILINE)
        if matched:
            i += matched.end()
            continue

        # Entire sections
        matched = re.match(regex__section, substring, re.MULTILINE)
        if matched:
            # rich_print("[green]Section")

            section_name = matched.groups()[-1]

            if section_name.lower() == "args" or section_name.lower() == "raises":
                formatted_docstring += f"\n{section_name}:\n"

                bruh = "\n".join(matched.group(0).split("\n")[1:])
                paras = re.split(r"\s{4}(?=\w+:)", bruh, re.MULTILINE)

                output = ""
                for para in paras:
                    if para.strip() == "":
                        continue
                    output += (
                        "\n".join(
                            format_paragraph(
                                para,
                                MAX_LINE_LENGTH - code_indent,
                                DEFAULT_INDENT,
                                DEFAULT_INDENT,
                            )
                        )
                        + "\n"
                    )
                output = output.rstrip("\n ")

                formatted_docstring += output + "\n\n"
            else:
                formatted_docstring += f"\n{section_name}:\n"

                bruh = "\n".join(matched.group(0).split("\n")[1:])
                paras = re.split(r"\n{2,}", bruh, re.MULTILINE)

                output = ""
                for para in paras:
                    if para.strip() == "":
                        continue
                    output += (
                        "\n".join(
                            format_paragraph(
                                para, MAX_LINE_LENGTH - code_indent, DEFAULT_INDENT, 0
                            )
                        )
                        + "\n\n"
                    )
                output = output.rstrip("\n ").lstrip("\n")

                formatted_docstring += output + "\n\n"

            i += matched.end()
            continue

        # Normal paragraphs
        matched = re.match(regex__normal, substring, re.MULTILINE)
        if matched:
            # rich_print("[green]Normal line")

            paragraph = matched.group().replace("\n", " ")
            formatted_para = format_paragraph(
                paragraph, MAX_LINE_LENGTH - code_indent, 0, 0
            )
            formatted_docstring += "\n".join(formatted_para) + "\n\n"

            i += matched.end()
            continue

        print(f"Can't match anything")
        print(substring)
        break

    formatted_docstring = formatted_docstring.rstrip("\n ")
    formatted_docstring = re.sub(r"\n{3,}", "\n\n", formatted_docstring)
    formatted_docstring = [
        " " * code_indent + line for line in formatted_docstring.splitlines()
    ]
    formatted_docstring = list(map(str.rstrip, formatted_docstring))
    return formatted_docstring


def is_inline_string(ast_node: ast.AST) -> bool:
    if not isinstance(ast_node, ast.Expr):
        return False
    if not isinstance(ast_node.value, ast.Constant):
        return False
    if not type(ast_node.value.value) == str:
        return False
    return True


if __name__ == "__main__":
    filepath = sys.argv[1]

    with open(filepath, encoding="utf-8") as f:
        code = f.read()

    code_lines = code.split("\n")

    root_node = ast.parse(code)

    # with open("temp.txt", "w", encoding="utf-8") as f:
    #     f.write(ast.dump(root_node, include_attributes=True, indent=2))

    # with open("walk.txt", "w") as f:
    #     for x in ast.walk(root_node):
    #         f.write(str(x))
    #         f.write("\n")

    docstring_nodes = []

    # If the first node in the AST is a string, it is a docstring
    first_statement = True
    for ast_node in ast.walk(root_node):
        # Ignore the root module node
        if isinstance(ast_node, ast.Module):
            continue

        # Match a module docstring
        if first_statement and is_inline_string(ast_node):
            print(
                f">> Matched module docstring (line {ast_node.lineno} - {ast_node.end_lineno})"
            )
            docstring_nodes.append(ast_node.value)
        # Match a function docstring
        elif isinstance(ast_node, ast.FunctionDef) and is_inline_string(
            ast_node.body[0]
        ):
            print(
                f">> Matched function docstring (line {ast_node.lineno} - {ast_node.end_lineno})"
            )
            docstring_nodes.append(ast_node.body[0].value)
        # Match a class docstring
        elif isinstance(ast_node, ast.ClassDef) and is_inline_string(ast_node.body[0]):
            print(
                f">> Matched class docstring (line {ast_node.lineno} - {ast_node.end_lineno})"
            )
            docstring_nodes.append(ast_node.body[0].value)

        first_statement = False

    # Format docstrings and queue them for insertion
    insertion_queue: List[Tuple[List[str], ast.AST]] = []  # (formatted, docstring_node)
    for docstring_node in docstring_nodes:
        code_indent = docstring_node.col_offset
        docstring = docstring_node.value

        formatted = format_docstring(docstring, code_indent)

        insertion_queue.append((formatted, docstring_node))

    # Insert formatted docstrings in reverse order
    # (because the insertion changes the indices of subsequent lines)
    for formatted, docstring_node in insertion_queue[::-1]:
        col_offset = docstring_node.col_offset
        start_lineno = docstring_node.lineno
        end_lineno = docstring_node.end_lineno

        # Make line numbers 0-based
        start_lineno -= 1
        end_lineno -= 1

        # Delete all lines of the original docstring (including quotations)
        lineno = start_lineno
        while lineno <= end_lineno:
            del code_lines[start_lineno]
            lineno += 1

        TRIPLE_QUOTES = '"""'

        # Check if it's possible to put the docstring in a single line
        if (len(formatted) == 1) and ('\"' not in formatted[0]) and (
            col_offset + 3 + len(formatted[0].strip()) + 3 <= MAX_LINE_LENGTH
        ):
            print("SINGLE LINE!")
            code_lines.insert(
                start_lineno,
                (
                    (" " * col_offset)
                    + TRIPLE_QUOTES
                    + formatted[0].strip()
                    + TRIPLE_QUOTES
                ),
            )
        else:
            # Opening quotes
            code_lines.insert(start_lineno, (" " * col_offset) + TRIPLE_QUOTES)
            for lineno in range(len(formatted)):
                code_lines.insert(start_lineno + 1 + lineno, formatted[lineno])
            # Closing quotes
            code_lines.insert(
                start_lineno + 1 + len(formatted), (" " * col_offset) + TRIPLE_QUOTES
            )

    # with open("formatted.py", "w", encoding="utf-8") as f:
    #     f.write("\n".join(code_lines))

    if prompt.Confirm.ask(f"Overwrite {filepath}?"):
        with open(filepath, "w", encoding="utf-8") as f:
            f.write("\n".join(code_lines))
