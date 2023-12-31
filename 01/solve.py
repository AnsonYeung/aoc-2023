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
    print(f"Part 1: {ans}")

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
    print(f"Part 2: {ans}")

if __name__ == "__main__":
    part1()
    part2()
