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

with open("input.txt", "r") as f:
    data = f.read().split('\n')[:-1]

def part1():
    ans = 0
    bag_content = {"red": 12, "green": 13, "blue": 14}
    for row in data:
        row_match = re.fullmatch(r"Game (\d+): (.*)", row)
        assert row_match is not None
        id = int(row_match.group(1))
        rest = row_match.group(2)
        ok = True
        for round in rest.split(";"):
            round_content = defaultdict(lambda: 0)
            for x in re.finditer(r"(\d+) (\w+)", round):
                round_content[x.group(2)] = int(x.group(1))
            for color in bag_content:
                if round_content[color] > bag_content[color]:
                    ok = False
        if ok:
            ans += int(id)
    print(f"Part 1: {ans}")

def part2():
    ans = 0
    for row in data:
        row_match = re.fullmatch(r"Game \d+: (.*)", row)
        assert row_match is not None
        rest = row_match.group(1)
        bag_content = {"red": 0, "green": 0, "blue": 0}
        for round in rest.split(";"):
            for x in re.finditer(r"(\d+) (\w+)", round):
                bag_content[x.group(2)] = max(bag_content[x.group(2)], int(x.group(1)))
        round_result = 1
        for c in bag_content:
            round_result *= bag_content[c]
        ans += round_result
    print(f"Part 2: {ans}")

if __name__ == "__main__":
    part1()
    part2()
