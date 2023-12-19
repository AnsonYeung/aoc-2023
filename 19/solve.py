#!/usr/bin/env python3
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
from typing import Any, Callable, Literal, TypeVar, Union
T = TypeVar("T")

def copy_to_clipboard(s: str):
    # Copy to clipboard using OSC52
    print(f"\x1b]52;c;{b64encode(s.encode()).decode()}\x07", end="")

def ints(l: list[str]) -> list[int]:
    return [int(s) for s in l]

def str_to_ints(s: str) -> list[int]:
    return ints(re.findall(r"-?\d+", s))

def make_matrix(r: int, c: int, default: Callable[[], T]) -> list[list[T]]:
    return [[default() for _ in range(c)] for _ in range(r)]

def print_matrix(data: list[list[Any]]):
    for r in data:
        for x in r:
            print(x, end="")
        print()
    print()

if stdin.isatty():
    with open("input.txt", "r") as f:
        data = f.read().split('\n')[:-1]
else:
    data = stdin.read().split('\n')[:-1]

key_to_int = {"x": 0, "m": 1, "a": 2, "s": 3}
workflows: dict[str, list[tuple[Union[Literal[True], tuple[int, bool, int]], str]]] = {}
i = 0
while data[i] != "":
    m = re.fullmatch(r"(.*)\{(.*)\}", data[i])
    assert m is not None
    name = m.group(1)
    content = m.group(2).split(",")
    cur = []
    for c in content:
        match c.split(":"):
            case [s]:
                cur.append((True, s))
            case [cond, s]:
                m = re.fullmatch(r"([xmas])([<>])(\d+)", cond)
                assert m is not None
                cur.append(((key_to_int[m.group(1)], m.group(2) == "<", int(m.group(3))), s))
    workflows[name] = cur
    i += 1

parts = []
i += 1
while i < len(data):
    ma = re.fullmatch(r"\{x=(\d+),m=(\d+),a=(\d+),s=(\d+)\}", data[i])
    assert ma is not None
    x = int(ma.group(1))
    m = int(ma.group(2))
    a = int(ma.group(3))
    s = int(ma.group(4))
    parts.append((x, m, a, s))
    i += 1

def part1():
    ans = 0
    for part in parts:
        cur_wf = "in"
        while cur_wf not in ["A", "R"]:
            wf = workflows[cur_wf]
            for cond, s in wf:
                if cond == True:
                    cur_wf = s
                    break
                k, is_lt, n = cond
                if is_lt and part[k] < n:
                    cur_wf = s
                    break
                if not is_lt and part[k] > n:
                    cur_wf = s
                    break
            else:
                print(wf)
                assert False
        if cur_wf == "A":
            ans += sum(part)
    print(f"Part 1: {ans}")
    copy_to_clipboard(str(ans))

# class Bound:
#     def __init__(self, bound: list[list[tuple[int, int]]]):
#         self.bound: list[list[tuple[int, int]]] = bound
# 
#     def __repr__(self):
#         return f"Bound({{x={self.bound[0]},m={self.bound[1]},a={self.bound[2]},s={self.bound[3]}}})"
# 
#     @staticmethod
#     def empty() -> "Bound":
#         return Bound([[] for _ in range(4)])
# 
#     @staticmethod
#     def all() -> "Bound":
#         return Bound([[(1, 4000)] for _ in range(4)])
# 
#     def unify(self, cond: tuple[int, bool, int]) -> "Bound":
#         b = Bound(deepcopy(self.bound))
#         k, is_lt, n = cond
#         if is_lt:
#             for i in range(len(self.bound[k])):
#                 l, u = self.bound[k][i]
#                 if l > n - 1:
#                     b.bound[k] = self.bound[k][:i]
#                     break
#                 if u > n - 1:
#                     b.bound[k][i] = (l, n - 1)
#         else:
#             for i in range(len(self.bound[k]) - 1, -1, -1):
#                 l, u = self.bound[k][i]
#                 if u < n + 1:
#                     b.bound[k] = self.bound[k][i + 1:]
#                     break
#                 if l < n + 1:
#                     b.bound[k][i] = (n + 1, u)
#         return b
# 
#     def __or__(self, other: "Bound") -> "Bound":
#         b = Bound.empty()
#         for i in range(4):
#             if len(self.bound[i]) == 0:
#                 b.bound[i] = copy(other.bound[i])
#                 continue
#             if len(other.bound[i]) == 0:
#                 b.bound[i] = copy(self.bound[i])
#                 continue
#             cur_s = 0
#             cur_o = 0
#             cur = cur_l = min(self.bound[i][0][0], other.bound[i][0][0])
#             while cur_s < len(self.bound[i]) and cur_o < len(other.bound[i]):
#                 if self.bound[i][cur_s][0] - 1 <= cur <= self.bound[i][cur_s][1]:
#                     cur = self.bound[i][cur_s][1]
#                     cur_s += 1
#                 elif self.bound[i][cur_s][1] < cur:
#                     cur_s += 1
#                 elif other.bound[i][cur_o][0] - 1 <= cur <= other.bound[i][cur_o][1]:
#                     cur = other.bound[i][cur_o][1]
#                     cur_o += 1
#                 elif other.bound[i][cur_o][1] < cur:
#                     cur_o += 1
#                 else:
#                     b.bound[i].append((cur_l, cur))
#                     cur = cur_l = min(self.bound[i][cur_s][0], other.bound[i][cur_o][0])
#             if cur_s < len(self.bound[i]):
#                 if self.bound[i][cur_s][0] - 1 <= cur <= self.bound[i][cur_s][1]:
#                     b.bound[i].append((cur_l, self.bound[i][cur_s][1]))
#                     cur_s += 1
#                 else:
#                     while cur_s < len(self.bound[i]) and self.bound[i][cur_s][0] <= cur:
#                         cur_s += 1
#                     b.bound[i].append((cur_l, cur))
#                 b.bound[i] = b.bound[i] + self.bound[i][cur_s:]
#             if cur_o < len(other.bound[i]):
#                 if other.bound[i][cur_o][0] - 1 <= cur <= other.bound[i][cur_o][1]:
#                     b.bound[i].append((cur_l, other.bound[i][cur_o][1]))
#                     cur_o += 1
#                 else:
#                     while cur_o < len(other.bound[i]) and other.bound[i][cur_o][0] <= cur:
#                         cur_o += 1
#                     b.bound[i].append((cur_l, cur))
#                 b.bound[i] = b.bound[i] + other.bound[i][cur_o:]
#         return b
# 
#     def is_possible(self) -> bool:
#         return all(len(c) > 0 for c in self.bound)
# 
#     def count(self) -> int:
#         result = 1
#         for i in range(4):
#             cnt = 0
#             for l, u in self.bound[i]:
#                 cnt += u - l + 1
#             result *= cnt
#         return result
# 
# solved = {"A": Bound.all(), "R": Bound.empty()}
# def solve_cond(cur_s: str) -> Bound:
#     if cur_s in solved: return solved[cur_s]
#     b = Bound.empty()
#     precond = []
#     for c, s in workflows[cur_s]:
#         solve_cond(s)
#         cs = solved[s]
#         for pc in precond:
#             cs = cs.unify(pc)
#         if c != True:
#             cs = cs.unify(c)
#         if cur_s == "qs":
#             print()
#             print("qs", b)
#         b = b | cs
#         if cur_s == "qs":
#             print("qs", cs)
#             print("qs", b)
#             print()
#         if c != True:
#             k, is_lt, n = c
#             if is_lt:
#                 precond.append((k, not is_lt, n - 1))
#             else:
#                 precond.append((k, not is_lt, n + 1))
#     print(cur_s, b)
#     solved[cur_s] = b
#     return b

class Bound:
    def __init__(self, lo: int, hi: int):
        self.lo = lo
        self.hi = hi

    def __repr__(self):
        return f"Bound([{self.lo}, {self.hi}])"

    def intersect(self, other: "Bound") -> "Bound":
        return Bound(max(self.lo, other.lo), min(self.hi, other.hi))

    def possible(self) -> bool:
        return self.lo <= self.hi

    def count(self) -> int:
        if not self.possible(): return 0
        return self.hi - self.lo + 1

class Box:
    def __init__(self, bound: list[Bound]):
        assert len(bound) == 4
        self.bound = bound

    def __repr__(self):
        return f"Box({{x={self.bound[0]},m={self.bound[1]},a={self.bound[2]},s={self.bound[3]}}})"

    @staticmethod
    def all() -> "Box":
        return Box([Bound(1, 4000) for _ in range(4)])

    def intersect(self, other: "Box") -> "Box":
        return Box([x.intersect(y) for x, y in zip(self.bound, other.bound)])

    def area(self) -> int:
        return reduce(lambda x, y: x * y, map(lambda x: x.count(), self.bound))

    def possible(self) -> bool:
        return all(b.possible() for b in self.bound)

solved = {"A": [Box.all()], "R": []}

def solve(name: str) -> list[Box]:
    if name in solved: return solved[name]
    result: list[Box] = []
    cur_precond = Box.all()
    for cond, cond_next in workflows[name]:
        next_accepts = [box.intersect(cur_precond) for box in solve(cond_next)]
        if cond == True:
            result += next_accepts
            continue
        k, is_lt, v = cond
        cond_box = Box.all()
        not_cond_box = Box.all()
        if is_lt:
            cond_box.bound[k] = Bound(1, v - 1)
            not_cond_box.bound[k] = Bound(v, 4000)
        else:
            cond_box.bound[k] = Bound(v + 1, 4000)
            not_cond_box.bound[k] = Bound(1, v)
        result += [box.intersect(cond_box) for box in next_accepts]
        cur_precond = cur_precond.intersect(not_cond_box)
    solved[name] = result
    return result

def part2():
    result = solve("in")
    ans = sum(box.area() for box in result)
    print(f"Part 2: {ans}")
    copy_to_clipboard(str(ans))

if __name__ == "__main__":
    part1()
    part2()
