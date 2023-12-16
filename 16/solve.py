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

def solve_for(initial_state: tuple[int, int, int, int]):
    SIZE = len(data[0])
    assert len(data) == SIZE
    state = [[set() for _ in range(SIZE)] for _ in range(SIZE)]
    pending = [initial_state]
    while len(pending) > 0:
        cr, cc, dr, dc = pending.pop()
        if not (0 <= cr < SIZE and 0 <= cc < SIZE): continue
        if (dr, dc) in state[cr][cc]: continue
        state[cr][cc].add((dr, dc))
        if data[cr][cc] == ".":
            pending.append((cr + dr, cc + dc, dr, dc))
        elif data[cr][cc] == "/":
            dr, dc = -dc, -dr
            pending.append((cr + dr, cc + dc, dr, dc))
        elif data[cr][cc] == "\\":
            dr, dc = dc, dr
            pending.append((cr + dr, cc + dc, dr, dc))
        elif data[cr][cc] == "|":
            if dc == 0:
                pending.append((cr + dr, cc + dc, dr, dc))
            else:
                dr, dc = 1, 0
                pending.append((cr + dr, cc + dc, dr, dc))
                dr, dc = -1, 0
                pending.append((cr + dr, cc + dc, dr, dc))
        elif data[cr][cc] == "-":
            if dr == 0:
                pending.append((cr + dr, cc + dc, dr, dc))
            else:
                dr, dc = 0, 1
                pending.append((cr + dr, cc + dc, dr, dc))
                dr, dc = 0, -1
                pending.append((cr + dr, cc + dc, dr, dc))
        else:
            assert False
    ans = sum(sum(1 if len(s) > 0 else 0 for s in row) for row in state)
    return ans

def part1():
    ans = solve_for((0, 0, 0, 1))
    print(f"Part 1: {ans}")
    copy_to_clipboard(str(ans))

def part2():
    SIZE = len(data[0])
    assert len(data) == SIZE
    ans = 0
    for i in range(SIZE):
        ans = max(ans, solve_for((i, 0, 0, 1)))
        ans = max(ans, solve_for((i, SIZE - 1, 0, -1)))
        ans = max(ans, solve_for((0, i, 1, 0)))
        ans = max(ans, solve_for((SIZE - 1, i, -1, 0)))
    print(f"Part 2: {ans}")
    copy_to_clipboard(str(ans))

if __name__ == "__main__":
    part1()
    part2()
