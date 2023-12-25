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
from typing import Any, Callable, TypeVar, Union
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

def min_cut(adj, start: str, e: str) -> Union[None, int]:
    edge_graph = defaultdict(lambda: {})
    for n1 in adj:
        for n2 in adj[n1]:
            edge_graph[n1][n2] = 1
    f = 0
    while True:
        vis = {}
        to_visit = {start: []}
        while len(to_visit) > 0:
            cur, prev = next(iter(to_visit.items()))
            to_visit.pop(cur)
            if cur in vis: continue
            prev = copy(prev)
            prev.append(cur)
            vis[cur] = prev
            for nxt in edge_graph[cur]:
                if edge_graph[cur][nxt] > 0:
                    to_visit[nxt] = prev
        if e in vis:
            for i in range(len(vis[e]) - 1):
                edge_graph[vis[e][i]][vis[e][i + 1]] -= 1
                edge_graph[vis[e][i + 1]][vis[e][i]] += 1
            f += 1
        else:
            break
    if f <= 3:
        comp = set()
        to_visit = {start}
        while len(to_visit) > 0:
            cur = to_visit.pop()
            if cur in comp: continue
            comp.add(cur)
            for nxt in edge_graph[cur]:
                if edge_graph[cur][nxt] > 0:
                    to_visit.add(nxt)
        return len(comp) * (len(adj) - len(comp))
    else:
        return None

def part1():
    adj = defaultdict(lambda: set())
    for line in data:
        name, neigh = line.split(": ")
        neigh_list = neigh.split(" ")
        for x in neigh_list:
            adj[x].add(name)
            adj[name].add(x)
    for n1 in adj:
        for n2 in adj:
            if n1 == n2: continue
            result = min_cut(adj, n1, n2)
            if result is not None:
                ans = result
                print(f"Part 1: {ans}")
                copy_to_clipboard(str(ans))

if __name__ == "__main__":
    part1()
