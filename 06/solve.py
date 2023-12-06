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
    return ints(re.findall(r"\d+", s))

with open("input.txt", "r") as f:
    data = f.read().split('\n')[:-1]

def part1():
    ans = 1
    time = str_to_ints(data[0])
    distance = str_to_ints(data[1])
    for i in range(len(time)):
        # (t - x) * x
        a = -1
        b = time[i]
        c = -distance[i]
        assert b * b - 4 * a * c >= 0
        mn = ceil((-b + sqrt(b * b - 4 * a * c)) / (2 * a))
        mx = floor((-b - sqrt(b * b - 4 * a * c)) / (2 * a))
        if (time[i] - mn) * mn == distance[i]:
            mn += 1
        if (time[i] - mx) * mx == distance[i]:
            mx -= 1
        ans *= mx - mn + 1
    print(f"Part 1: {ans}")
    copy_to_clipboard(str(ans))

def part2():
    time = int(''.join(re.findall(r"\d+", data[0])))
    distance = int(''.join(re.findall(r"\d+", data[1])))
    a = -1
    b = time
    c = -distance
    assert b * b - 4 * a * c >= 0
    mn = ceil((-b + sqrt(b * b - 4 * a * c)) / (2 * a))
    mx = floor((-b - sqrt(b * b - 4 * a * c)) / (2 * a))
    if (time - mn) * mn == distance:
        mn += 1
    if (time - mx) * mx == distance:
        mx -= 1
    ans = mx - mn + 1
    print(f"Part 2: {ans}")
    copy_to_clipboard(str(ans))

if __name__ == "__main__":
    part1()
    part2()
