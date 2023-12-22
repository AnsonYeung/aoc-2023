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
from typing import Any, Callable, TypeVar
T = TypeVar("T")

def copy_to_clipboard(s: str):
    # Copy to clipboard using OSC52
    print(f"\x1b]52;c;{b64encode(s.encode()).decode()}\x07", end="")

def ints(l: list[str]) -> list[int]:
    return [int(s) for s in l]

def str_to_ints(s: str) -> list[int]:
    return ints(re.findall(r"-?\d+", s))

def make_matrix(r: int, c: int, default: Callable[[], T]) -> list[list[T]]:
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

Coord = tuple[int, int, int]

parsed: list[tuple[Coord, Coord]] = []
for line in data:
    x1, y1, z1, x2, y2, z2 = str_to_ints(line)
    parsed.append(((x1, y1, z1), (x2, y2, z2)))

fallen: list[tuple[Coord, Coord]] = copy(parsed)
falled: defaultdict[int, bool] = defaultdict(lambda: False)
supported_by: defaultdict[int, list[int]] = defaultdict(lambda: [])

def between(x: int, y: int):
    if x > y: x, y = y, x
    for i in range(x, y + 1):
        yield i

def coords(c1: Coord, c2: Coord):
    for x in between(c1[0], c2[0]):
        for y in between(c1[1], c2[1]):
            for z in between(c1[2], c2[2]):
                yield (x, y, z)

def fall(i: int):
    if falled[i]: return
    c1, c2 = fallen[i]
    for c in coords(parsed[i][0], parsed[i][1]):
        for j, l in enumerate(parsed):
            for lc in coords(l[0], l[1]):
                if i != j and lc[0] == c[0] and lc[1] == c[1] and lc[2] < c[2]:
                    fall(j)
    final_min_z = 1
    supported: set[int] = set()
    for c in coords(c1, c2):
        for j, l in enumerate(fallen):
            for lc in coords(l[0], l[1]):
                if i != j and lc[0] == c[0] and lc[1] == c[1] and lc[2] < c[2]:
                    # print(i, c, j, lc)
                    # print(lc[2], final_min_z + 1)
                    if lc[2] + 1 > final_min_z:
                        final_min_z = lc[2] + 1
                        supported = {j}
                    elif lc[2] + 1 == final_min_z:
                        supported.add(j)
    supported_by[i] = list(supported)
    fall_dist = min(c1[2], c2[2]) - final_min_z
    fallen[i] = ((c1[0], c1[1], c1[2] - fall_dist), (c2[0], c2[1], c2[2] - fall_dist))
    falled[i] = True

for i in range(len(parsed)):
    fall(i)

def part1():
    ans = 0
    for i in range(len(parsed)):
        for j in range(len(parsed)):
            if i in supported_by[j] and len(supported_by[j]) == 1:
                # crucial support
                break
        else:
            # can be removed
            ans += 1
    print(f"Part 1: {ans}")
    copy_to_clipboard(str(ans))

def part2():
    ans = 0
    for i in range(len(parsed)):
        f = defaultdict(lambda: False)
        to_fall = [i]
        while len(to_fall) > 0:
            x = to_fall.pop()
            if f[x]: continue
            f[x] = True
            ans += 1
            for j in range(len(parsed)):
                if len(supported_by[j]) == 0: continue
                for k in supported_by[j]:
                    if not f[k]:
                        break
                else:
                    to_fall.append(j)
        ans -= 1
    print(f"Part 2: {ans}")
    copy_to_clipboard(str(ans))

if __name__ == "__main__":
    part1()
    part2()
