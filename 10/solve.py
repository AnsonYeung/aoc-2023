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

# "." and "S" not included
deltas = {
    "|": [(0, 1), (0, -1)],
    "-": [(-1, 0), (1, 0)],
    "L": [(0, -1), (1, 0)],
    "J": [(0, -1), (-1, 0)],
    "7": [(-1, 0), (0, 1)],
    "F": [(1, 0), (0, 1)],
}

def add_delta(x, d):
    return (x[0] + d[0], x[1] + d[1])

def get(x):
    if 0 <= x[1] < len(data) and 0 <= x[0] < len(data[x[1]]):
        return data[x[1]][x[0]]
    return "."

path = []
start = None
for i, line in enumerate(data):
    for j, c in enumerate(line):
        if c == 'S':
            start = (j, i)
assert start is not None
prev = None
cur = start
while len(path) == 0 or cur != start:
    path.append(cur)
    if cur == start:
        prev = start
        for delta in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            n = get(add_delta(start, delta))
            if n == ".": continue
            assert n != "S", "init problem"
            for x in deltas[n]:
                f = add_delta(delta, x)
                if f[0] == 0 and f[1] == 0:
                    cur = add_delta(start, delta)
        assert prev != cur
        continue
    assert prev is not None
    for x in deltas[get(cur)]:
        f = add_delta(cur, x)
        if f[0] == prev[0] and f[1] == prev[1]:
            continue
        prev = cur
        cur = f
        break
    else:
        assert False
print(path)
k = set(path)
for i, line in enumerate(data):
    for j, c in enumerate(line):
        if (j, i) in k:
            print(c, end="")
        else:
            print(" ", end="")
    print()
for i, line in enumerate(data):
    for j, c in enumerate(line):
        if (j, i) in k:
            print("W", end="")
        else:
            print(" ", end="")
    print()
print(len(path))

transformed_map = [["."] * (len(data[0]) * 2 + 4) for _ in range(len(data) * 2 + 4)]

for x in k:
    transformed_map[x[1] * 2 + 2][x[0] * 2 + 2] = "M"
    if get(x) == "S":
        for d in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            for k in deltas[get(add_delta(x, d))]:
                a = add_delta(d, k)
                if a[0] == 0 and a[1] == 0:
                    f = add_delta((x[0] * 2 + 2, x[1] * 2 + 2), d)
                    transformed_map[f[1]][f[0]] = "M"
        continue
    for d in deltas[get(x)]:
        f = add_delta((x[0] * 2 + 2, x[1] * 2 + 2), d)
        transformed_map[f[1]][f[0]] = "M"

def get_in_transformed(x):
    return transformed_map[x[1]][x[0]]

to_explore = [(0, 0)]
while len(to_explore) > 0:
    coord = to_explore.pop()
    if coord[0] < 0 or coord[1] < 0 or coord[0] >= len(data[0]) * 2 + 4 or coord[1] >= len(data[0]) * 2 + 4:
        continue
    if get_in_transformed(coord) != ".":
        continue
    transformed_map[coord[1]][coord[0]] = "O"
    for d in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        to_explore.append(add_delta(coord, d))

# for i, line in enumerate(transformed_map):
#     for j, c in enumerate(line):
#         print(c, end="")
#     print()

def part1():
    ans = len(path) // 2
    print(f"Part 1: {ans}")
    copy_to_clipboard(str(ans))

def part2():
    ans = 0
    for i in range(len(data[0])):
        for j in range(len(data)):
            if transformed_map[j * 2 + 2][i * 2 + 2] == ".":
                ans += 1
    print(f"Part 2: {ans}")
    copy_to_clipboard(str(ans))

if __name__ == "__main__":
    part1()
    part2()
