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

sys.setrecursionlimit(100000)

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

grid = [list(s) for s in data]
SIZE = len(grid)
assert SIZE == len(grid[0])

def search_longest(cur: tuple[int, int], vis: list[tuple[int, int]], part2: bool) -> int:
    if not (0 <= cur[0] < SIZE and 0 <= cur[1] < SIZE): return 0
    if cur in vis: return 0
    if cur == (SIZE - 1, SIZE - 2): return len(vis)
    vis.append(cur)
    mx = 0
    if not part2:
        match grid[cur[0]][cur[1]]:
            case ">":
                mx = max(mx, search_longest((cur[0], cur[1] + 1), vis, part2))
            case "<":
                mx = max(mx, search_longest((cur[0], cur[1] - 1), vis, part2))
            case "v":
                mx = max(mx, search_longest((cur[0] + 1, cur[1]), vis, part2))
            case "^":
                mx = max(mx, search_longest((cur[0] - 1, cur[1]), vis, part2))
            case ".":
                mx = max(mx, search_longest((cur[0], cur[1] + 1), vis, part2))
                mx = max(mx, search_longest((cur[0], cur[1] - 1), vis, part2))
                mx = max(mx, search_longest((cur[0] + 1, cur[1]), vis, part2))
                mx = max(mx, search_longest((cur[0] - 1, cur[1]), vis, part2))
    else:
        mx = max(mx, search_longest((cur[0], cur[1] + 1), vis, part2))
        mx = max(mx, search_longest((cur[0], cur[1] - 1), vis, part2))
        mx = max(mx, search_longest((cur[0] + 1, cur[1]), vis, part2))
        mx = max(mx, search_longest((cur[0] - 1, cur[1]), vis, part2))
    vis.pop()
    return mx

def part1():
    prev = []
    ans = search_longest((0, 1), prev, False)
    print(f"Part 1: {ans}")
    copy_to_clipboard(str(ans))

def grid_get(r: int, c: int) -> str:
    if not (0 <= r < SIZE and 0 <= c < SIZE): return "#"
    return grid[r][c]

DELTAS = [(0, 1), (0, -1), (1, 0), (-1, 0)]
def part2():
    decision_pt = []
    for r in range(SIZE):
        for c in range(SIZE):
            cnt = sum(1 if grid_get(d[0] + r, d[1] + c) != "#" else 0 for d in DELTAS)
            if grid[r][c] != "#" and cnt > 2:
                decision_pt.append((r, c))
    decision_pt.append((0, 1))
    decision_pt.append((SIZE - 1, SIZE - 2))
    adj_list = [[] for _ in decision_pt]
    for i, (r, c) in enumerate(decision_pt):
        for d in DELTAS:
            if grid_get(d[0] + r, d[1] + c) != "#":
                prev = (r, c)
                cur = (r + d[0], c + d[1])
                cnt = 0
                while cur not in decision_pt:
                    cnt += 1
                    for d2 in DELTAS:
                        nxt = (cur[0] + d2[0], cur[1] + d2[1])
                        if grid_get(nxt[0], nxt[1]) != "#" and prev != nxt:
                            prev = cur
                            cur = nxt
                            break
                    else:
                        assert False
                adj_list[i].append((decision_pt.index(cur), cnt))
    print(adj_list)
    def search_longest(cur: int, vis: list[int]) -> int:
        if cur in vis: return -2 ** 32
        if cur == len(decision_pt) - 1: return 0
        mx = -2 ** 32
        vis.append(cur)
        for nxt, l in adj_list[cur]:
            mx = max(mx, search_longest(nxt, vis) + l + 1)
        vis.pop()
        return mx
    prev = []
    ans = search_longest(len(decision_pt) - 2, prev)
    print(f"Part 2: {ans}")
    copy_to_clipboard(str(ans))

if __name__ == "__main__":
    part1()
    part2()
