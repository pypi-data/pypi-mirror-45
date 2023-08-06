#!/usr/bin/env python3

from secrets import choice

from typing import Optional


def randrange(start: int, stop=Optional[int], step: int = 1) -> int:
    """
    Return a randomly selected element from range(start, stop, step).
    This is equivalent to choice(range(start, stop, step)),
    but doesn’t actually build a range object.
    :param start: int: Start number.
    :param stop: Stop number. (Default value = Optional[int])
    :param step: int: Step (Default value = 1)

    """
    return choice(range(start, stop, step))
