#!/usr/bin/env python3
from sys import stdin, exit
from copy import *
from heapq import *
from collections import *
from itertools import *
from functools import *
from math import *
from bisect import *
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

parsed = [(r.group(1), int(r.group(2)), int(r.group(3), 16), int(r.group(4))) for r in [re.fullmatch(r"(\w) (\d+) \(#([0-9a-f]{5})(\d)\)", s) for s in data]] # type: ignore

def part1():
    m: defaultdict[tuple[int, int], bool] = defaultdict(lambda: False)
    cur: tuple[int, int] = (0, 0)
    min_r, max_r, min_c, max_c = 0, 0, 0, 0
    m[cur] = True
    def walk_delta(dr: int, dc: int):
        nonlocal cur, min_r, min_c, max_r, max_c
        cur = (cur[0] + dr, cur[1] + dc)
        if cur[0] < min_r: min_r = cur[0]
        if cur[0] > max_r: max_r = cur[0]
        if cur[1] < min_c: min_c = cur[1]
        if cur[1] > max_c: max_c = cur[1]
        m[cur] = True
    for dir, cnt, _, _ in parsed:
        match dir:
            case "U":
                dr, dc = -1, 0
            case "D":
                dr, dc = 1, 0
            case "L":
                dr, dc = 0, -1
            case "R":
                dr, dc = 0, 1
            case _:
                assert False
        for _ in range(cnt):
            walk_delta(dr, dc)
    # for i in range(min_r, max_r + 1):
    #     for j in range(min_c, max_c + 1):
    #         if m[(i, j)]:
    #             print("#", end="")
    #         else:
    #             print(" ", end="")
    #     print()
    outside: defaultdict[tuple[int, int], bool] = defaultdict(lambda: False)
    to_explore = [(min_r - 1, min_c - 1)]
    cnt = 0
    while len(to_explore) > 0:
        r, c = to_explore.pop()
        if outside[(r, c)]: continue
        outside[(r, c)] = True
        cnt += 1
        def explore(dr, dc):
            nr = r + dr
            nc = c + dc
            if m[(nr, nc)]: return
            if not (min_r - 1 <= nr <= max_r + 1 and min_c - 1 <= nc <= max_c + 1): return
            to_explore.append((nr, nc))
        explore(1, 0)
        explore(-1, 0)
        explore(0, 1)
        explore(0, -1)
    # print(cnt)
    # print(min_r, max_r, min_c, max_c)
    ans = (max_r - min_r + 3) * (max_c - min_c + 3) - cnt
    print(f"Part 1: {ans}")
    copy_to_clipboard(str(ans))

def part2():
    r_list = [-1, 0, 1]
    c_list = [-1, 0, 1]
    cur: tuple[int, int] = (0, 0)
    for _, _, cnt, dir in parsed:
        match dir:
            case 0:
                dr, dc = 0, 1
            case 1:
                dr, dc = 1, 0
            case 2:
                dr, dc = 0, -1
            case 3:
                dr, dc = -1, 0
            case _:
                assert False
        cur = (cur[0] + dr * cnt, cur[1] + dc * cnt)
        r_list.append(cur[0] - dr)
        c_list.append(cur[1] - dc)
        r_list.append(cur[0])
        c_list.append(cur[1])
        r_list.append(cur[0] + dr)
        c_list.append(cur[1] + dc)
    r_list = list(sorted(set(r_list)))
    c_list = list(sorted(set(c_list)))
    m: defaultdict[tuple[int, int], bool] = defaultdict(lambda: False)
    def zr(r: int):
        i = bisect_left(r_list, r)
        assert r_list[i] == r
        return i
    def zc(c: int):
        i = bisect_left(c_list, c)
        assert c_list[i] == c
        return i
    cur = zr(0), zc(0)
    m[cur] = True
    for _, _, cnt, dir in parsed:
        match dir:
            case 0:
                dr, dc = 0, 1
                dst = zc(c_list[cur[1]] + cnt)
                for c in range(cur[1], dst + 1):
                    m[(cur[0], c)] = True
                cur = (cur[0], dst)
            case 1:
                dr, dc = 1, 0
                dst = zr(r_list[cur[0]] + cnt)
                for r in range(cur[0], dst + 1):
                    m[(r, cur[1])] = True
                cur = (dst, cur[1])
            case 2:
                dr, dc = 0, -1
                dst = zc(c_list[cur[1]] - cnt)
                for c in range(dst, cur[1] + 1):
                    m[(cur[0], c)] = True
                cur = (cur[0], dst)
            case 3:
                dr, dc = -1, 0
                dst = zr(r_list[cur[0]] - cnt)
                for r in range(dst, cur[0] + 1):
                    m[(r, cur[1])] = True
                cur = (dst, cur[1])
            case _:
                assert False

    # for i, r in enumerate(r_list):
    #     for j, c in enumerate(c_list):
    #         if m[(i, j)]:
    #             print("#", end="")
    #         else:
    #             print(" ", end="")
    #     print("")

    outside: defaultdict[tuple[int, int], bool] = defaultdict(lambda: False)
    to_explore = [(0, 0)]
    cnt = 0
    while len(to_explore) > 0:
        r, c = to_explore.pop()
        if outside[(r, c)]: continue
        outside[(r, c)] = True
        cnt += 1
        def explore(dr, dc):
            nr = r + dr
            nc = c + dc
            if m[(nr, nc)]: return
            if not (0 <= nr < len(r_list) and 0 <= nc < len(c_list)): return
            to_explore.append((nr, nc))
        explore(1, 0)
        explore(-1, 0)
        explore(0, 1)
        explore(0, -1)
    ans = 0
    for r in range(len(r_list)):
        for c in range(len(c_list)):
            if not outside[(r, c)]:
                ans += (r_list[r + 1] - r_list[r]) * (c_list[c + 1] - c_list[c])
    print(f"Part 2: {ans}")
    copy_to_clipboard(str(ans))

if __name__ == "__main__":
    part1()
    part2()
