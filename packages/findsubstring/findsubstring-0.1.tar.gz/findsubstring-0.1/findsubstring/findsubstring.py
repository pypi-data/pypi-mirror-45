#!/usr/bin/env python3

from typing import Generator


def find_all(
    str_: str,
    substring: str,
    overlapping: bool = False
        ) -> Generator[int, str, None]:
    """
    Function to find all occurrences of a substring in a string.
    :param str_: str: String where you want to find a substring.
    :param substring: str: Substring you want to find.
    :param overlapping: bool: Set to True if you want to find
        overlapping values. (Default value = False)

    """

    start = 0
    while True:
        start = str_.find(substring, start)

        if start == -1:
            return None
        yield start

        if overlapping:
            start += 1
        else:
            start += len(substring)
