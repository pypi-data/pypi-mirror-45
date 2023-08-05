#!/usr/bin/env python3


def case_insensitive_replace(text: str, old: str, new: str) -> str:
    """
    Case insensitive string replace.

    :param text: str: Text where string will be replaced.
    :param old: str: String to be replaced.
    :param new: str: Replaced string.

    """
    idx = 0
    while idx < len(text):
        index_l = text.lower().find(old.lower(), idx)
        if index_l == -1:
            return text
        text = f"{text[:index_l]}{new}{text[index_l + len(old):]}"
        idx = index_l + len(new)
    return text
