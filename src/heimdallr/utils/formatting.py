"""
Formatting utilities.
"""
import re
from re import sub


def to_camel(s: str) -> str:
    """
    Translates a string to camel case.

    Args:
        s (str): The string to translate.
    """
    s = sub(r"(_|-)+", " ", s).title().replace(" ", "")
    return "".join([s[0].lower(), s[1:]])


def contains_letters_or_numbers(text: str):
    """
    Checks if a paragraph contains letters or numbers.

    Args:
        text (str): A paragraph of text.

    Returns:
        bool: True if the paragraph contains letters or numbers, False otherwise.
    """
    pattern = re.compile(r"[a-zA-Z0-9]")
    return bool(pattern.search(text))


def normalize_sentence(text: str) -> str:
    """
    Normalizes a sentence that has been split into multiple lines, matching the following criteria:

    * If the first character of a line is lowercase, it is part of the previous sentence.
    * Else the line is part of the next sentence.


    Args:
        text (str): A text to be normalized.

    Returns:
        str: The formatted text.
    """
    splits = text.split("\n")

    normalized_sentence = ""

    for split in splits:
        line = split.strip()

        if line:
            if line[0].islower():
                normalized_sentence += line + " "
            else:
                normalized_sentence = normalized_sentence.strip() + "\n" + line + " "

    return normalized_sentence.strip()
