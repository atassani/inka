import pytest

test_cases = {
    (
        "Deck: Abraham\n"
        "\n"
        "Tags: one two-three\n"
        "\n"
        "1. Some question?\n"
        "\n"
        "> Some answer"
    ): "Some answer",
    # HTML Code is not escaped
    (
        "Deck: Abraham\n"
        "\n"
        "Tags: one two-three\n"
        "\n"
        "1. Some question?\n"
        "\n"
        "> Some answer <div>with HTML code</div>"
    ): "Some answer <div>with HTML code</div>",
    # A list is returned as is
    (
        "Deck: Abraham\n"
        "\n"
        "Tags: one two-three\n"
        "\n"
        "1. Some question?\n"
        "\n"
        "> - Item1\n"
        "> - Item2"
    ): "- Item1\n"
       "- Item2",
    # An ordered list is returned as is
    (
        "Deck: Abraham\n"
        "\n"
        "Tags: one two-three\n"
        "\n"
        "1. Some question?\n"
        "\n"
        "> 1. Item1\n"
        "> 2. Item2"
    ): "1. Item1\n"
       "2. Item2",       
    # Lists combined with text
    (
        "Deck: Abraham\n"
        "\n"
        "Tags: one two-three\n"
        "\n"
        "1. Some question?\n"
        "\n"
        "> Some text before\n"
        "> - Item1\n"
        "> - Item2\n"
        "> Some text after\n"
        "> 1. Item1\n"
        "> 2. Item2"
    ):  "Some text before\n\n"
        "- Item1\n"
        "- Item2\n"
        "Some text after\n\n"
        "1. Item1\n"
        "2. Item2",       
    # A table is respected
    (
        "Deck: Abraham\n"
        "\n"
        "Tags: one two-three\n"
        "\n"
        "1. Some question?\n"
        "\n"
        "> Some text before\n"
        "> | Header 1 | Header 2 |\n"
        "> |----------|----------|\n"
        "> |  Row 1   |   Row 1  |\n"
        "> |  Row 2   |   Row 2  |\n"
        "> Some text after\n"
        "> Last text"
    ):  "Some text before\n\n"
        "| Header 1 | Header 2 |\n"
        "|----------|----------|\n"
        "|  Row 1   |   Row 1  |\n"
        "|  Row 2   |   Row 2  |\n"
        "Some text after\n\n"
        "Last text",
    # Empty lines are respected
    (
        "Deck: Abraham\n"
        "\n"
        "Tags: one two-three\n"
        "\n"
        "1. Some question?\n"
        "\n"
        "> Answer line 1\n"
        ">\n"
        ">\n"
        "> Answer line 2"
    ):  "Answer line 1\n\n"
        "\n\n"
        "\n\n"
        "Answer line 2",
    (
        "Deck: Abraham\n"
        "\n"
        "1. Some question?\n"
        "\n"
        "> Answer\n"
        "> Additional info\n"
        "> \n"
        "> And more to it"
    ): "Answer\n\nAdditional info\n\n\n\nAnd more to it",
    "Deck: Abraham\n\n1. Some question?\n\n> > Answer\n": "> Answer",
    (
        "Deck: Abraham\n"
        "\n"
        "Tags: one two-three\n"
        "\n"
        "<!--ID:123456-->\n"
        "1. Some question?\n"
        "\n"
        "> Answer"
    ): "Answer",
    (
        "Deck: Abraham\n"
        "\n"
        "Tags: one two-three\n"
        "\n"
        "1. A little bit of python code...\n"
        "\n"
        "> ```python\n"
        "> def hello(name: str) -> str:\n"
        ">     return f'Hello, {name}!'\n"
        "> if __name__ == '__main__':\n"
        ">     print(hello('bro'))\n"
        "> ```\n"
        "> some text"
    ): (
        "```python\n"
        "def hello(name: str) -> str:\n"
        "    return f'Hello, {name}!'\n"
        "if __name__ == '__main__':\n"
        "    print(hello('bro'))\n"
        "```\n\n"
        "some text"
    ),
    (
        "Deck: Abraham\n"
        "\n"
        "Tags: one two-three\n"
        "\n"
        "1. A little bit of python code...\n"
        "\n"
        "> Some text before:\n"
        "> ```python\n"
        "> def hello(name: str) -> str:\n"
        ">     return f'Hello, {name}!'\n"
        ">\n"
        "> if __name__ == '__main__':\n"
        ">     print(hello('bro'))\n"
        "> ```\n"
        "> text in between\n"
        "> ```python\n"
        "> def hello(name: str) -> str:\n"
        ">     return f'Hello, {name}!\n"
        "> ```\n"
        "> text after\n"
        ">\n"
        "> ```commandline\n"
        "> inka collect -u path/to/file.md\n"
        "> ```\n"
    ): (
        "Some text before:\n\n"
        "```python\n"
        "def hello(name: str) -> str:\n"
        "    return f'Hello, {name}!'\n"
        "\n"
        "if __name__ == '__main__':\n"
        "    print(hello('bro'))\n"
        "```\n\n"
        "text in between\n\n"
        "```python\n"
        "def hello(name: str) -> str:\n"
        "    return f'Hello, {name}!\n"
        "```\n\n"
        "text after\n\n"
        "\n\n"
        "```commandline\n"
        "inka collect -u path/to/file.md\n"
        "```"
    ),
    # inline mathjax
    "> $\n> X^{2}\n> $": "$\n\nX^{2}\n\n$",
    "> \\$\n> X^{2}\n> $": "\\$\n\nX^{2}\n\n$",
    "> $\n> X^{2}\n> \\$": "$\n\nX^{2}\n\n\\$",
    # mathjax blocks
    "> $$\n> X^{2}\n> $$": "$$\nX^{2}\n$$",
    "> \\$$\n> X^{2}\n> $$": "\\$$\n\nX^{2}\n\n$$",
    "> $\\$\n> X^{2}\n> $$": "$\\$\n\nX^{2}\n\n$$",
    "> $$\n> X^{2}\n> \\$$": "$$\n\nX^{2}\n\n\\$$",
    "> $$\n> X^{2}\n> $\\$": "$$\n\nX^{2}\n\n$\\$",
    "> \\$\\$\n> X^{2}\n> $$": "\\$\\$\n\nX^{2}\n\n$$",
    "> \\$$\n> X^{2}\n> \\$$": "\\$$\n\nX^{2}\n\n\\$$",
    "> \\$$\n> X^{2}\n> $\\$": "\\$$\n\nX^{2}\n\n$\\$",
    "> $\\$\n> X^{2}\n> \\$$": "$\\$\n\nX^{2}\n\n\\$$",
    "> $\\$\n> X^{2}\n> $\\$": "$\\$\n\nX^{2}\n\n$\\$",
    "> \\$\\$\n> X^{2}\n> \\$$": "\\$\\$\n\nX^{2}\n\n\\$$",
    "> \\$\\$\n> X^{2}\n> $\\$": "\\$\\$\n\nX^{2}\n\n$\\$",
    "> $\\$\n> X^{2}\n> \\$\\$": "$\\$\n\nX^{2}\n\n\\$\\$",
    "> \\$\\$\n> X^{2}\n> \\$\\$": "\\$\\$\n\nX^{2}\n\n\\$\\$",
    # If no answer
    "Some text": None,
}


@pytest.mark.parametrize("text, expected", test_cases.items())
def test_get_answer(fake_parser, text, expected):
    answer = fake_parser._get_cleaned_answer(text)

    assert answer == expected
