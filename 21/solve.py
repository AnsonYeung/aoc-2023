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

SIZE = len(data)
assert SIZE == len(data[0])

def gen_pos_lst(start: tuple[int, int]) -> list[set[tuple[int, int]]]:
    cur = {start}
    pos_lst = [cur]
    for _ in range(SIZE * SIZE):
        nxt: set[tuple[int, int]] = set()
        for r, c in cur:
            def try_pos(nr, nc):
                if not (0 <= nr < SIZE and 0 <= nc < SIZE): return
                if data[nr][nc] == "#": return
                nxt.add((nr, nc))
            try_pos(r - 1, c)
            try_pos(r + 1, c)
            try_pos(r, c - 1)
            try_pos(r, c + 1)
        if len(pos_lst) > 2 and nxt == pos_lst[-2]: break
        cur = nxt
        pos_lst.append(cur)
    return pos_lst

def part1():
    start = None
    for r, row in enumerate(data):
        for c, x in enumerate(row):
            if x == "S":
                assert start is None
                start = (r, c)
    assert start is not None
    pos_lst = gen_pos_lst(start)
    ans = len(pos_lst[64])
    print(f"Part 1: {ans}")
    copy_to_clipboard(str(ans))

def part2():
    assert SIZE % 2 == 1
    start = None
    for r, row in enumerate(data):
        for c, x in enumerate(row):
            if x == "S":
                assert start is None
                start = (r, c)
    assert start is not None
    # best path should be walk to the "main walkways", then walk from corner to the individual cells, may have parity issues
    TL = gen_pos_lst((0, 0))
    TR = gen_pos_lst((0, SIZE - 1))
    BR = gen_pos_lst((SIZE - 1, SIZE - 1))
    BL = gen_pos_lst((SIZE - 1, 0))
    CORNERS = [TL, TR, BR, BL]
    LEN_CORN = len(TL)
    BUFFER = 4
    assert LEN_CORN < 2 * SIZE
    for l in CORNERS:
        assert len(l) == LEN_CORN
        while len(l) < (BUFFER + 2) * SIZE * 2:
            l.append(l[-2])
    STEP = 100 # FIXME
    if stdin.isatty():
        STEP = 26501365
    parity_fix = lambda n: -1 if n % 2 == 1 else -2
    top_parity = 0
    for k, l in enumerate(TL):
        if start in l:
            top_parity = k % 2
            break
    else:
        assert False
    assert top_parity == 0
    initial = len(TL[parity_fix(STEP + top_parity)])
    print(initial)
    # add odd parity and even parity, taxicab dist < (STEP - BUFFER * SIZE) // SIZE
    inner = 0
    for i in range(1, STEP // SIZE - BUFFER):
        inner += len(TL[parity_fix(STEP - i * SIZE + top_parity)]) * i * 4
    print(inner)
    # handle taxicab dist on awkward dist, exclude those directly on axis
    outer_diag = 0
    for i in range(STEP // SIZE - BUFFER, STEP // SIZE + 4):
        if i < 2:
            print("WARN: TOO SMALL")
            continue
        for j, corner in enumerate(CORNERS):
            # count of this is only (i - 1)
            start_cnt = None
            for k, l in enumerate(corner):
                if start in l:
                    start_cnt = k
                    break
            assert start_cnt is not None
            remaining_step = STEP - start_cnt - 2 - (i - 2) * SIZE
            # print(i, remaining_step)
            print(i, start_cnt, remaining_step, len(CORNERS[(j + 2) % 4][remaining_step]))
            if remaining_step >= 0:
                outer_diag += len(CORNERS[(j + 2) % 4][remaining_step]) * (i - 1)
            # print(i, STEP - start_cnt - 2 - i * SIZE, CORNERS[(j + 2) % 4][STEP - start_cnt - 2 - i * SIZE], len(CORNERS[(j + 2) % 4][STEP - start_cnt - 2 - i * SIZE]))
    print(outer_diag)
    # special handling for directly on axis ones, since they can be accessed in 2 ways...
    outer_axis = 0
    MID = SIZE // 2
    EDGES = [gen_pos_lst((0, MID)), gen_pos_lst((MID, SIZE - 1)), gen_pos_lst((SIZE - 1, MID)), gen_pos_lst((MID, 0))]
    for l in EDGES:
        while len(l) < (BUFFER + 2) * SIZE * 2:
            l.append(l[-2])
    for i in range(4):
        for cur_dist in range(STEP // SIZE - BUFFER, STEP // SIZE + 4):
            if cur_dist < 1:
                print("WARN: TOO SMALL")
                continue
            if stdin.isatty():
                # Real input
                remaining_step = STEP - MID - 1 - (cur_dist - 1) * SIZE
                if remaining_step >= 0:
                    outer_axis += len(EDGES[i][remaining_step])
            else:
                # ToT
                reachable: set[tuple[int, int]] = set()
                for j in range(2):
                    corner = (i + j) % 4
                    cur_corn = CORNERS[corner]
                    start_cnt = None
                    for k, l in enumerate(cur_corn):
                        if start in l:
                            start_cnt = k
                            break
                    assert start_cnt is not None
                    remaining_step = STEP - start_cnt - 1 - (cur_dist - 1) * SIZE
                    # print(cur_dist, remaining_step)
                    if remaining_step >= 0:
                        # print(STEP - start_cnt - 1 - cur_dist * SIZE)
                        reachable = reachable.union(CORNERS[(i + 1 - j) % 4][remaining_step])
                # print(len(reachable))
                outer_axis += len(reachable)
                print(i, cur_dist, len(reachable))
    print(outer_axis)
    ans = initial + inner + outer_diag + outer_axis
    print(f"Part 2: {ans}")
    copy_to_clipboard(str(ans))

if __name__ == "__main__":
    # part1()
    part2()
