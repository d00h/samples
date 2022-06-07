from typing import Callable


def push(value) -> Callable[int, int]:
    def fn(state):
        return (state << 2) + value
    return fn


def pop(value) -> Callable[int, int]:
    def fn(state):
        if state & 3 != value:
            raise ValueError(state)
        return state >> 2
    return fn


def check_pairs(text):
    pairs = {
        '{': push(0), '}': pop(0),
        '(': push(1), ')': pop(1),
        '<': push(2), '>': pop(2),
        '[': push(3), ']': pop(3),
    }

    state: int = 0
    for ch in text:
        action = pairs.get(ch)
        if action is None:
            continue
        state = action(state)

    if state != 0:
        raise ValueError(state)


check_pairs("({}{}<>dds)")
print("ok")

