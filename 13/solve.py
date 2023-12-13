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

patterns = []
cur_pat = []
for line in data:
    if line == "":
        patterns.append(cur_pat)
        cur_pat = []
    else:
        cur_pat.append(line)
patterns.append(cur_pat)

def row_compare(x, y):
    return all(i == j for i, j in zip(x, y))

def part1():
    ans = 0
    for pattern in patterns:
        for i in range(len(pattern) - 1):
            for j in range(min(i + 1, len(pattern) - 1 - i)):
                if not row_compare(pattern[i - j], pattern[i + 1 + j]):
                    break
            else:
                ans += (i + 1) * 100
        for i in range(len(pattern[0]) - 1):
            for j in range(min(i + 1, len(pattern[0]) - 1 - i)):
                if not row_compare((r[i - j] for r in pattern), (r[i + 1 + j] for r in pattern)):
                    break
            else:
                ans += (i + 1)
    print(f"Part 1: {ans}")
    copy_to_clipboard(str(ans))

def part2():
    ans = 0
    for pattern in patterns:
        pat1 = None
        for i in range(len(pattern) - 1):
            for j in range(min(i + 1, len(pattern) - 1 - i)):
                if not row_compare(pattern[i - j], pattern[i + 1 + j]):
                    break
            else:
                pat1 = (i + 1) * 100
        for i in range(len(pattern[0]) - 1):
            for j in range(min(i + 1, len(pattern[0]) - 1 - i)):
                if not row_compare((r[i - j] for r in pattern), (r[i + 1 + j] for r in pattern)):
                    break
            else:
                pat1 = (i + 1)
        assert pat1 is not None
        found = False
        for i in range(len(pattern)):
            for j in range(len(pattern[i])):
                orig = pattern[i][j]
                pattern[i] = pattern[i][:j] + ("." if orig == "#" else "#") + pattern[i][j+1:]
                pat2 = None
                for k in range(len(pattern) - 1):
                    for l in range(min(k + 1, len(pattern) - 1 - k)):
                        if not row_compare(pattern[k - l], pattern[k + 1 + l]):
                            break
                    else:
                        if (k + 1) * 100 != pat1:
                            pat2 = (k + 1) * 100
                for k in range(len(pattern[0]) - 1):
                    for l in range(min(k + 1, len(pattern[0]) - 1 - k)):
                        if not row_compare((r[k - l] for r in pattern), (r[k + 1 + l] for r in pattern)):
                            break
                    else:
                        if (k + 1) != pat1:
                            pat2 = (k + 1)
                if pat2 is not None:
                    ans += pat2
                    break
                pattern[i] = pattern[i][:j] + orig + pattern[i][j+1:]
            else:
                continue
            break
    print(f"Part 2: {ans}")
    copy_to_clipboard(str(ans))

if __name__ == "__main__":
    part1()
    part2()
