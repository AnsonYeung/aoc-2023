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

m = {}
for line in data[2:]:
    result = re.fullmatch(r"(\w{3}) = \((\w{3}), (\w{3})\)", line)
    assert result is not None
    m[result.group(1)] = (result.group(2), result.group(3))

seq = [0 if x == "L" else 1 for x in data[0]]

def part1():
    cur = "AAA"
    i = 0
    while cur != "ZZZ":
        cur = m[cur][seq[i % len(seq)]]
        i += 1
    print(f"Part 1: {i}")
    copy_to_clipboard(str(i))

def part2():
    ans = 1
    for x in m:
        if x.endswith("A"):
            cur = x
            i = 0
            while not cur.endswith("Z"):
                cur = m[cur][seq[i % len(seq)]]
                i += 1
            ans = ans * i // gcd(ans, i)
            print(i)
    print(f"Part 2: {ans}")
    copy_to_clipboard(str(ans))

if __name__ == "__main__":
    part1()
    part2()
