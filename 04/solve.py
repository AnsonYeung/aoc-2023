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

def part1():
    ans = 0
    for line in data:
        parts = line.split("|")
        win = set(int(s) for s in re.findall(r"\d+", parts[0].split(":")[1]))
        have = [int(s) for s in re.findall(r"\d+", parts[1])]
        cnt = 0
        for x in have:
            if x in win:
                cnt += 1
        if cnt >= 1:
            ans += 2 ** (cnt - 1)
    print(f"Part 1: {ans}")
    copy_to_clipboard(str(ans))

def part2():
    ans = 0
    cards = [0] * len(re.findall(r"\d+", data[0].split("|")[0].split(":")[1]))
    for line in data:
        parts = line.split("|")
        win = set(int(s) for s in re.findall(r"\d+", parts[0].split(":")[1]))
        have = [int(s) for s in re.findall(r"\d+", parts[1])]
        cnt = 0
        for x in have:
            if x in win:
                cnt += 1
        cur = cards[0] + 1
        ans += cur
        cards = cards[1:] + [0]
        for i in range(cnt):
            cards[i] += cur
    print(f"Part 2: {ans}")
    copy_to_clipboard(str(ans))

if __name__ == "__main__":
    part1()
    part2()
