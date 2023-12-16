#!/usr/bin/env python3
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

def make_matrix(r: int, c: int, default: T) -> list[list[T]]:
    return [[default for _ in range(c)] for _ in range(r)]

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

SIZE = len(data)
assert len(data[0]) == SIZE

def do_north(data: list[list[str]]) -> list[list[str]]:
    result = make_matrix(SIZE, SIZE, ".")
    for c in range(SIZE):
        cur = 0
        for r in range(SIZE):
            match data[r][c]:
                case "O":
                    result[cur][c] = "O"
                    cur += 1
                case "#":
                    result[r][c] = "#"
                    cur = r + 1
                case ".":
                    pass
                case _:
                    assert False
    return result

def calc_north(data: list[list[str]]) -> int:
    result = 0
    for i, row in enumerate(data):
        for c in row:
            if c == "O":
                result += SIZE - i
    return result

def part1():
    ans = calc_north(do_north(list(list(s) for s in data)))
    print(f"Part 1: {ans}")
    copy_to_clipboard(str(ans))

def rotate(data: list[list[str]]) -> list[list[str]]:
    result = make_matrix(SIZE, SIZE, ".")
    for r in range(SIZE):
        for c in range(SIZE):
            result[c][SIZE - 1 - r] = data[r][c]
    return result

def do_cycle(data: list[list[str]]) -> list[list[str]]:
    for _ in range(4):
        data = do_north(data)
        data = rotate(data)
    return data

def part2():
    cur = list(list(s) for s in data)
    hist = [cur]
    count = 0
    while not any(all(all(x == y for x, y in zip(r1, r2)) for r1, r2 in zip(last, cur)) for last in hist[:-1]):
        cur = do_cycle(cur)
        hist.append(cur)
        count += 1
    print([calc_north(x) for x in hist])
    for i, last in enumerate(hist):
        if all(all(x == y for x, y in zip(r1, r2)) for r1, r2 in zip(last, cur)):
            period = count - i
            print(i, len(hist) - 1)

            assert (count - i) % period == 0
            ans = calc_north(hist[i + (1000000000 - count) % period])
            break
    else:
        assert False
    print(f"Part 2: {ans}")
    copy_to_clipboard(str(ans))

if __name__ == "__main__":
    part1()
    part2()
