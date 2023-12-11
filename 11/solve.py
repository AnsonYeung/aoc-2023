#!/usr/bin/env pypy3
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

def copy_to_clipboard(s: str):
    # Copy to clipboard using OSC52
    print(f"\x1b]52;c;{b64encode(s.encode()).decode()}\x07", end="")

def ints(l: list[str]) -> list[int]:
    return [int(s) for s in l]

def str_to_ints(s: str) -> list[int]:
    return ints(re.findall(r"-?\d+", s))

if stdin.isatty():
    with open("input.txt", "r") as f:
        data = f.read().split('\n')[:-1]
else:
    data = stdin.read().split('\n')[:-1]

positions = []
for i, row in enumerate(data):
    for j, x in enumerate(row):
        if x != ".":
            positions.append((i, j))

def part1():
    row_deltas = [2 if all(x == "." for x in data[i]) else 1 for i in range(len(data))]
    col_deltas = [2 if all(data[j][i] == "." for j in range(len(data))) else 1 for i in range(len(data[0]))]

    ans = 0
    for i in range(len(positions)):
        for j in range(i + 1, len(positions)):
            [pos1x, pos1y] = positions[i]
            [pos2x, pos2y] = positions[j]
            x1, x2 = min(pos1x, pos2x), max(pos1x, pos2x)
            y1, y2 = min(pos1y, pos2y), max(pos1y, pos2y)
            ans += sum(row_deltas[x1:x2]) + sum(col_deltas[y1:y2])
    print(f"Part 1: {ans}")
    copy_to_clipboard(str(ans))

def part2():
    row_deltas = [1000000 if all(x == "." for x in data[i]) else 1 for i in range(len(data))]
    col_deltas = [1000000 if all(data[j][i] == "." for j in range(len(data))) else 1 for i in range(len(data[0]))]

    ans = 0
    for i in range(len(positions)):
        for j in range(i + 1, len(positions)):
            [pos1x, pos1y] = positions[i]
            [pos2x, pos2y] = positions[j]
            x1, x2 = min(pos1x, pos2x), max(pos1x, pos2x)
            y1, y2 = min(pos1y, pos2y), max(pos1y, pos2y)
            ans += sum(row_deltas[x1:x2]) + sum(col_deltas[y1:y2])
    print(f"Part 2: {ans}")
    copy_to_clipboard(str(ans))

if __name__ == "__main__":
    part1()
    part2()
