#!/usr/bin/env python3
from collections.abc import Callable
from sys import stdin, exit
from copy import *
from heapq import *
from collections import *
from itertools import *
from functools import *
from math import *
from tqdm import tqdm
import re
import numpy as np
import os
import sys
from base64 import b64encode
from typing import Any, TypeVar
T = TypeVar("T")

def copy_to_clipboard(s: str):
    # Copy to clipboard using OSC52
    print(f"\x1b]52;c;{b64encode(s.encode()).decode()}\x07", end="")

def ints(l: list[str]) -> list[int]:
    return [int(s) for s in l]

def str_to_ints(s: str) -> list[int]:
    return ints(re.findall(r"-?\d+", s))

def make_matrix(r: int, c: int, default: Callable[..., T]) -> list[list[T]]:
    return [[default() for _ in range(c)] for _ in range(r)]

def print_matrix(data: list[list[Any]]):
    for r in data:
        for x in r:
            print(x, end="")
        print()
    print()

if stdin.isatty():
    with open("input.txt", "r") as f:
        data = f.read().split('\n')[:-1]
else:
    data = stdin.read().split('\n')[:-1]

parsed = [[int(s) for s in r] for r in data]
SIZE = len(parsed)
assert len(parsed[0]) == SIZE

def part1():
    min_loss = make_matrix(SIZE, SIZE, lambda: defaultdict(lambda: 2 ** 32))
    remaining = [(parsed[0][1], 0, 1, 0, 1, 1), (parsed[1][0], 1, 0, 1, 0, 1)]
    heapify(remaining)
    while len(remaining) > 0:
        loss, cr, cc, dr, dc, dt = heappop(remaining)
        if loss >= min_loss[cr][cc][(dr, dc, dt)]:
            continue
        min_loss[cr][cc][(dr, dc, dt)] = loss
        def visit(dr, dc, dt):
            if not (0 <= cr + dr < SIZE and 0 <= cc + dc < SIZE): return
            heappush(remaining, (loss + parsed[cr + dr][cc + dc], cr + dr, cc + dc, dr, dc, dt))
        if dt != 3:
            visit(dr, dc, dt + 1)
        visit(dc, dr, 1)
        if dc == 0:
            visit(dc, -dr, 1)
        else:
            visit(-dc, dr, 1)
    ans = min(min_loss[SIZE - 1][SIZE - 1].values())
    print(f"Part 1: {ans}")
    copy_to_clipboard(str(ans))

def part2():
    min_loss = make_matrix(SIZE, SIZE, lambda: defaultdict(lambda: 2 ** 32))
    remaining = [(parsed[0][1], 0, 1, 0, 1, 1), (parsed[1][0], 1, 0, 1, 0, 1)]
    heapify(remaining)
    while len(remaining) > 0:
        loss, cr, cc, dr, dc, dt = heappop(remaining)
        if loss >= min_loss[cr][cc][(dr, dc, dt)]:
            continue
        min_loss[cr][cc][(dr, dc, dt)] = loss
        def visit(dr, dc, dt):
            if not (0 <= cr + dr < SIZE and 0 <= cc + dc < SIZE): return
            heappush(remaining, (loss + parsed[cr + dr][cc + dc], cr + dr, cc + dc, dr, dc, dt))
        if dt != 10:
            visit(dr, dc, dt + 1)
        if dt >= 4:
            visit(dc, dr, 1)
            if dc == 0:
                visit(dc, -dr, 1)
            else:
                visit(-dc, dr, 1)
    ans = min(min_loss[SIZE - 1][SIZE - 1].values())
    print(f"Part 2: {ans}")
    copy_to_clipboard(str(ans))

if __name__ == "__main__":
    part1()
    part2()
