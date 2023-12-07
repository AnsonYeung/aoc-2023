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

if stdin.isatty():
    with open("input.txt", "r") as f:
        data = f.read().split('\n')[:-1]
else:
    data = stdin.read().split('\n')[:-1]

parsed = [(line.split(" ")[0], int(line.split(" ")[1])) for line in data]

def hand_type(h) -> int:
    counts = defaultdict(lambda: 0)
    for c in h:
        counts[c] += 1
    if len(counts.keys()) == 1: return 6
    have_3 = False
    count_2 = 0
    for k in counts:
        if counts[k] == 4: return 5
        if counts[k] == 3: have_3 = True
        if counts[k] == 2: count_2 += 1
    if have_3 and count_2 == 1: return 4
    if have_3: return 3
    assert 0 <= count_2 <= 2
    return count_2

def card_to_int(c) -> int:
    if c.isdigit():
        return int(c)
    if c == "A":
        return 14
    if c == "K":
        return 13
    if c == "Q":
        return 12
    if c == "J":
        return 11
    if c == "T":
        return 10
    assert False

def compare_card(c1, c2) -> int:
    r = card_to_int(c1) - card_to_int(c2)
    if r < 0: return -1
    elif r > 0: return 1
    else: return 0

def compare_hand(h1, h2) -> int:
    assert len(h1) == 5
    assert len(h2) == 5
    # return if h1 < h2
    if hand_type(h2) > hand_type(h1): return -1
    if hand_type(h1) > hand_type(h2): return 1
    for i in range(5):
        if h1[i] != h2[i]:
            return compare_card(h1[i], h2[i])
    return 0

def part1():
    ans = 0
    result = list(sorted(parsed, key=cmp_to_key(lambda x, y: compare_hand(x[0], y[0]))))
    for i, (_, bet) in enumerate(result):
        ans += bet * (i + 1)
    print(f"Part 1: {ans}")
    copy_to_clipboard(str(ans))

def hand_type2(h) -> int:
    counts = defaultdict(lambda: 0)
    j_count = 0
    for c in h:
        if c == "J":
            j_count += 1
        else:
            counts[c] += 1
    if len(counts.keys()) <= 1: return 6
    have_3 = False
    count_2 = 0
    for k in counts:
        assert counts[k] + j_count != 5
        if counts[k] + j_count == 4: return 5
        if counts[k] + j_count == 3: have_3 = True
        if counts[k] == 2: count_2 += 1
    if have_3:
        assert j_count != 3
        if j_count == 2:
            # must be X Y Z J J or get four
            return 3
        if j_count == 1 and count_2 >= 2:
            # form J X X Y Y
            assert count_2 == 2
            return 4
        if j_count == 0 and count_2 >= 1:
            assert count_2 == 1
            return 4
        return 3
    assert j_count <= 1
    if j_count == 1:
        assert count_2 < 2
        count_2 += 1
    assert 0 <= count_2 <= 2
    return count_2

def card_to_int2(c) -> int:
    if c.isdigit():
        return int(c)
    if c == "A":
        return 14
    if c == "K":
        return 13
    if c == "Q":
        return 12
    if c == "J":
        return 1
    if c == "T":
        return 10
    assert False

def compare_card2(c1, c2) -> int:
    r = card_to_int2(c1) - card_to_int2(c2)
    if r < 0: return -1
    elif r > 0: return 1
    else: return 0

def compare_hand2(h1, h2) -> int:
    assert len(h1) == 5
    assert len(h2) == 5
    # return if h1 < h2
    if hand_type2(h2) > hand_type2(h1): return -1
    if hand_type2(h1) > hand_type2(h2): return 1
    for i in range(5):
        if h1[i] != h2[i]:
            return compare_card2(h1[i], h2[i])
    return 0

def part2():
    ans = 0
    result = list(sorted(parsed, key=cmp_to_key(lambda x, y: compare_hand2(x[0], y[0]))))
    for i, (_, bet) in enumerate(result):
        ans += bet * (i + 1)
    print(f"Part 2: {ans}")
    copy_to_clipboard(str(ans))

if __name__ == "__main__":
    part1()
    part2()
