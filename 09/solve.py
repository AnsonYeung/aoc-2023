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

def extrapolate(l: list[int]):
    if all(x == 0 for x in l):
        return 0
    next_diff = extrapolate(list(l[i + 1] - l[i] for i in range(len(l) - 1)))
    return l[-1] + next_diff

def part1():
    ans = 0
    for line in data:
        l = str_to_ints(line)
        ans += extrapolate(l)
    print(f"Part 1: {ans}")
    copy_to_clipboard(str(ans))

def extrapolate_back(l: list[int]):
    if all(x == 0 for x in l):
        return 0
    diff = extrapolate_back(list(l[i + 1] - l[i] for i in range(len(l) - 1)))
    return l[0] - diff

def part2():
    ans = 0
    for line in data:
        l = str_to_ints(line)
        ans += extrapolate_back(l)
    print(f"Part 2: {ans}")
    copy_to_clipboard(str(ans))

if __name__ == "__main__":
    part1()
    part2()
