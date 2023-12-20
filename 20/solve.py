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
from typing import Any, Callable, TypeVar
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

module_type: dict[str, int] = {}
for line in data:
    name = line.split(" ")[0]
    match name[0]:
        case "b":
            assert name == "broadcaster"
            module_type[name] = 2
        case "%":
            module_type[name[1:]] = 0
        case "&":
            module_type[name[1:]] = 1
        case _:
            assert False

output_link: dict[str, list[str]] = {}
input_link: defaultdict[str, list[str]] = defaultdict(lambda: [])
input_mem: defaultdict[str, dict[str, bool]] = defaultdict(lambda: {})
state: dict[str, bool] = {}

def reset():
    global output_link, input_link, input_mem, state
    output_link = {}
    input_link = defaultdict(lambda: [])
    input_mem = defaultdict(lambda: {})
    state = {}
    for line in data:
        [name, output] = line.split(" -> ")
        if name[0] != "b": name = name[1:]
        if module_type[name] == 0:
            state[name] = False
        outputs = output.split(", ")
        output_link[name] = outputs
        for o in outputs:
            input_link[o].append(name)
            if o in module_type and module_type[o] == 1:
                input_mem[o][name] = False

def part1():
    reset()
    lo_cnt = 0
    hi_cnt = 0
    for _ in range(1000):
        pending: list[tuple[str, bool, str]] = [("broadcaster", False, "button")]
        while len(pending) > 0:
            name, val, sender = pending[0]
            if val:
                hi_cnt += 1
            else:
                lo_cnt += 1
            pending = pending[1:]
            if name not in module_type:
                assert name == "rx"
                continue
            match module_type[name]:
                case 0:
                    if val == False:
                        state[name] = not state[name]
                        for x in output_link[name]:
                            pending.append((x, state[name], name))
                case 1:
                    assert sender in input_mem[name]
                    input_mem[name][sender] = val
                    val = False
                    for x in input_mem[name]:
                        if input_mem[name][x] == False:
                            val = True
                    for x in output_link[name]:
                        pending.append((x, val, name))
                case 2:
                    for x in output_link[name]:
                        pending.append((x, val, name))
    ans = lo_cnt * hi_cnt
    print(f"Part 1: {ans}")
    copy_to_clipboard(str(ans))

def part2():
    reset()
    counters = [[start] for start in output_link["broadcaster"]]
    for l in counters:
        while True:
            n = None
            for k in output_link[l[-1]]:
                if k in module_type and module_type[k] == 0:
                    assert n is None
                    # all counter should be disjoint
                    for c in counters:
                        assert n not in c
                    n = k
            if n is not None:
                l.append(n)
            else:
                break
    print(counters)
    digits: dict[str, tuple[int, int]] = {}
    for x in module_type:
        if module_type[x] == 0:
            for i, l in enumerate(counters):
                if x not in l: continue
                j = l.index(x)
                assert x not in digits
                digits[x] = (i, j)
                break
            else:
                assert False
    print(digits)
    target = None
    for x in module_type:
        if module_type[x] == 1:
            if output_link[x] == ["rx"]:
                assert target is None
                target = x
    assert target is not None
    ans = 1
    assert len(input_link[target]) == len(counters)
    counter_len = len(counters[0])
    for l in counters:
        assert len(l) == counter_len

    for k in input_link[target]:
        # k should output HIGH
        assert module_type[k] == 1
        assert len(input_link[k]) == 1
        assert output_link[k] == [target]
        # j should output LOW
        [j] = input_link[k]
        ins = [digits[x] for x in input_link[j]]
        outs = [digits[x] for x in output_link[j] if x != k]
        assert len(ins) + len(outs) == counter_len + 1
        assert module_type[j] == 1
        cycle = 0
        for i in input_link[j]:
            # i should output HIGH
            assert module_type[i] == 0
            d = digits[i]
            print(d)
            cycle |= 2 ** d[1]
        print(cycle)
        ans = ans * cycle // gcd(ans, cycle)
    print(f"Part 2: {ans}")
    copy_to_clipboard(str(ans))

if __name__ == "__main__":
    part1()
    part2()
