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

def simplify(l: list) -> list:
    tmp = list(sorted(l))
    result = []
    prev_start = 0
    prev_end = 0
    for start, end in tmp:
        if start < prev_end:
            prev_end = end
        else:
            result.append((prev_start, prev_end))
            prev_start = start
            prev_end = end
    result.append((prev_start, prev_end))
    assert result[0] == (0, 0)
    result = result[1:]
    return result


with open("input.txt", "r") as f:
    data = f.read().split('\n')[:-1]
    seeds = [int(x) for x in re.findall(r"\d+", data[0])]
    step_map = []
    cur_line = 2
    for i in range(7):
        cur_line += 1
        cur_map = []
        while cur_line < len(data) and len(l := [int(x) for x in re.findall(r"\d+", data[cur_line])]) == 3:
            cur_map.append((l[1], l[1] + l[2], l[0]))
            cur_line += 1
        step_map.append(list(sorted(cur_map)))
        cur_line += 1

def part1():
    ans = 2 ** 32 - 1
    for x in seeds:
        for step in step_map:
            for start, end, dest in step:
                if start <= x < end:
                    x = x - start + dest
                    break
        if x < ans:
            ans = x
    print(f"Part 1: {ans}")
    copy_to_clipboard(str(ans))

def part2():
    cur_state = []
    for i in range(0, len(seeds), 2):
        cur_state.append((seeds[i], seeds[i] + seeds[i + 1]))
    for step in step_map:
        new_state = []
        for cur_start, cur_end in cur_state:
            cur = cur_start
            for start, end, dest in step:
                if cur < start:
                    new_state.append((cur, start))
                    cur = start
                if cur >= end: continue
                if cur_end <= end:
                    new_state.append((cur - start + dest, cur_end - start + dest))
                    break
                new_state.append((cur - start + dest, end - start + dest))
                cur = end
        cur_state = simplify(new_state)
    ans = cur_state[0][0]
    print(f"Part 2: {ans}")
    copy_to_clipboard(str(ans))

if __name__ == "__main__":
    part1()
    part2()
