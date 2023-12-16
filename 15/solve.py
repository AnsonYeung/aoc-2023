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

data = data[0]

def part1():
    ans = 0
    for s in data.split(","):
        h = 0
        for k in s.encode():
            h += k
            h *= 17
            h %= 256
        ans += h
    print(f"Part 1: {ans}")
    copy_to_clipboard(str(ans))

def part2():
    hmap = [[] for _ in range(256)]
    for s in data.split(","):
        m = re.fullmatch(r"(.*)(?:-|=(\d+))", s)
        assert m is not None
        h = 0
        for k in m.group(1).encode():
            h += k
            h *= 17
            h %= 256
        if m.group(2) is None:
            new_box = []
            for lens in copy(hmap[h]):
                if lens[0] != m.group(1):
                    new_box.append(lens)
            hmap[h] = new_box
        else:
            for i, lens in enumerate(hmap[h]):
                if lens[0] == m.group(1):
                    hmap[h][i][1] = int(m.group(2))
                    break
            else:
                hmap[h].append([m.group(1), int(m.group(2))])
    ans = 0
    for i, box in enumerate(hmap):
        for j, lens in enumerate(box):
            ans += (i + 1) * (j + 1) * lens[1]
    print(f"Part 2: {ans}")
    copy_to_clipboard(str(ans))

if __name__ == "__main__":
    part1()
    part2()
