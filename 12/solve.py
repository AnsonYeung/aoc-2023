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

parsed = []
for line in data:
    parsed.append((line.split(" ")[0], str_to_ints(line.split(" ")[1])))

def check(cur: list[int], req: str):
    assert len(req) == len(cur)
    for i, x in enumerate(req):
        if x == "?": continue
        if x == "." and cur[i] == 1: return False
        if x == "#" and cur[i] == 0: return False
    return True

def gen_perm(l: int, rem: list[int], req: str):
    if l < 0: return
    assert len(req) == l
    if len(rem) == 0:
        assert False
#        if check([0] * l, req):
#            yield [0] * l
#        return
    for i in range(l - rem[0] + 1):
        if len(rem) == 1:
            if check([0] * i + [1] * rem[0] + [0] * (l - rem[0] - i), req):
                yield [0] * i + [1] * rem[0] + [0] * (l - rem[0] - i)
        else:
            if i == l - rem[0]: break
            if check([0] * i + [1] * rem[0] + [0], req[:i+rem[0]+1]):
                for p in gen_perm(l - rem[0] - i - 1, rem[1:], req[i+rem[0]+1:]):
                    yield [0] * i + [1] * rem[0] + [0] + p

def solve(s, req):
    # count for s[:j] with last set using a prefix
    assert len(req) > 1
    cur = []
    for j in range(len(s) + 1):
        if j < req[0]:
            cur.append(0)
        elif check([0] * (j - req[0]) + [1] * req[0], s[:j]):
            cur.append(1)
        else:
            cur.append(0)
    for x in req[1:]:
        last = cur
        cur = []
        for j in range(len(s) + 1):
            count = 0
            for pref_len in range(j - x):
                if check([0] * (j - x - pref_len) + [1] * x, s[pref_len:j]):
                    count += last[pref_len]
            cur.append(count)
    cnt = 0
    for i, x in enumerate(cur):
        if check([0] * (len(s) - i), s[i:]):
            cnt += x
    return cnt

def part1():
    ans = 0
#    for s, req in parsed:
#        for p in gen_perm(len(s), req, s):
#            assert check(p, s)
#            ans += 1
    for s, req in parsed:
        ans += solve(s, req)
    print(f"Part 1: {ans}")
    copy_to_clipboard(str(ans))

def part2():
    ans = 0
    for s, req in parsed:
        req = req * 5
        s = (s + "?") * 4 + s
        ans += solve(s, req)
    print(f"Part 2: {ans}")
    copy_to_clipboard(str(ans))

if __name__ == "__main__":
    part1()
    part2()
