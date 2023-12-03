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

with open("input.txt", "r") as f:
    data = f.read().split('\n')[:-1]
    m_data = ["." * len(data[0])] + data + ["." * len(data[0])]
    m_data = ["." + s + "." for s in m_data]

def is_sym(s):
    return not s.isdigit() and s != "."

def part1():
    ans = 0
    for i in range(1, len(data) + 1):
        for num_match in re.finditer(r"\d+", m_data[i]):
            val = int(num_match.group(0))
            if is_sym(m_data[i][num_match.start() - 1]) or is_sym(m_data[i][num_match.end()]):
                ans += val
            else:
                for j in range(num_match.start() - 1, num_match.end() + 1):
                    if is_sym(m_data[i - 1][j]) or is_sym(m_data[i + 1][j]):
                        ans += val
                        break
    print(f"Part 1: {ans}")
    copy_to_clipboard(str(ans))

def part2():
    ans = 0
    gear_num = defaultdict(lambda: [])
    for i in range(1, len(data) + 1):
        for num_match in re.finditer(r"\d+", m_data[i]):
            val = int(num_match.group(0))
            add_gear = lambda x, y: gear_num[(x, y)].append(val)
            add_gear(i, num_match.start() - 1)
            add_gear(i, num_match.end())
            for j in range(num_match.start() - 1, num_match.end() + 1):
                add_gear(i - 1, j)
                add_gear(i + 1, j)
    for x, y in gear_num:
        if m_data[x][y] == '*' and len(gear_num[(x, y)]) == 2:
            ans += gear_num[(x, y)][0] * gear_num[(x, y)][1]
    print(f"Part 2: {ans}")
    copy_to_clipboard(str(ans))

if __name__ == "__main__":
    part1()
    part2()
