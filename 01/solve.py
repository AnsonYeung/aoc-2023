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
import requests

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from init import get_session # type: ignore

def submit(part: int, ans):
    res = input(f"Submit answer {ans}? [Y/n]")
    if 'N' in res or 'n' in res: return
    day = int(os.path.basename(os.path.dirname(os.path.realpath(__file__))))
    r = requests.post(f"https://adventofcode.com/2023/day/{day}/answer", data={"level": part, "answer": ans}, cookies={"session": get_session()})
    res = r.text
    main = re.search(r"(?s)<main>(.*)</main>", res)
    if main:
        print(main.group(1))
    else:
        print(res)

with open("input.txt", "r") as f:
    data = f.read().split('\n')[:-1]

def part1():
    ans = 0
    for s in data:
        d1 = 0
        d2 = 0
        for c in s:
            if '0' <= c <= '9':
                d1 = int(c)
        for c in list(reversed(list(s))):
            if '0' <= c <= '9':
                d2 = int(c)
        ans += d1 + d2 * 10
    submit(1, ans)

def part2():
    ans = 0
    numbers = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
    for s in data:
        for i, c in enumerate(s):
            if '0' <= c <= '9':
                d1 = int(c)
            for j, n in enumerate(numbers):
                if str(s[:i + 1]).endswith(n):
                    d1 = j + 1
        for i, c in enumerate(list(reversed(list(s)))):
            if '0' <= c <= '9':
                d2 = int(c)
            for j, n in enumerate(numbers):
                if str(s[:len(s) - i]).endswith(n):
                    d2 = j + 1
        ans += d1 + d2 * 10
    submit(2, ans)

if __name__ == "__main__":
    part1()
    part2()
