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
import z3
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

parsed: list[list[int]] = []
for line in data:
    parsed.append(str_to_ints(line))

def intersect_xy(l1, l2) -> bool:
    x1, y1, _, vx1, vy1, _ = l1
    x2, y2, _, vx2, vy2, _ = l2
    # x1 + t1 vx1 = x2 + t2 vx2
    # y1 + t1 vy1 = y2 + t2 vy2

    # t1 vx1 - t2 vx2 = x2 - x1
    # t1 vy1 - t2 vy2 = y2 - y1
    # vx1 -vx2
    # vy1 -vy2
    determinant = -vy2 * vx1 + vx2 * vy1
    if determinant == 0:
        # parallel
        c1 = (y2 - y1) / (x2 - x1)
        c2 = vy2 / vx2
        c3 = vy1 / vx1
        print("parallel", c1, c2, c3)
        return c1 == c2
    else:
        # solve for t1 and t2
        # inv / det:
        # -vy2 vx2
        # -vy1 vx1
        t1 = (x2 - x1) / determinant * -vy2 + (y2 - y1) / determinant * vx2
        t2 = (x2 - x1) / determinant * -vy1 + (y2 - y1) / determinant * vx1
        print("not parallel", t1, t2)
        if t1 >= 0 and t2 >= 0:
            ix = x1 + t1 * vx1
            iy = y1 + t1 * vy1
            if 200000000000000 <= ix <= 400000000000000 and 200000000000000 <= iy <= 400000000000000:
                return True
        return False

def part1():
    ans = 0
    for i in range(len(parsed)):
        for j in range(i + 1, len(parsed)):
            if intersect_xy(parsed[i], parsed[j]):
                ans += 1
    print(f"Part 1: {ans}")
    copy_to_clipboard(str(ans))

def collide(vx, vy, vz, l1, l2) -> tuple[int, int, int]:
    x1, y1, z1, vx1, vy1, vz1 = l1
    x2, y2, z2, vx2, vy2, vz2 = l2
    vx1 -= vx
    vx2 -= vx
    vy1 -= vy
    vy2 -= vy
    vz1 -= vz
    vz2 -= vz
    # x1 + t1 vx1 = x2 + t2 vx2
    # y1 + t1 vy1 = y2 + t2 vy2

    # t1 vx1 - t2 vx2 = x2 - x1
    # t1 vy1 - t2 vy2 = y2 - y1
    # vx1 -vx2
    # vy1 -vy2
    determinant = -vy2 * vx1 + vx2 * vy1
    swapped = False
    if determinant == 0:
        # x, y parallel
        x1, z1 = z1, x1
        vx1, vz1 = vz1, vx1
        x2, z2 = z2, x2
        vx2, vz2 = vz2, vx2
        swapped = True
    determinant = -vy2 * vx1 + vx2 * vy1
    if determinant == 0:
        return (-2 ** 64, -2 ** 64, -2 ** 64)
    # solve for t1 and t2
    # inv / det:
    # -vy2 vx2
    # -vy1 vx1
    t1 = (x2 - x1) / determinant * -vy2 + (y2 - y1) / determinant * vx2
    t2 = (x2 - x1) / determinant * -vy1 + (y2 - y1) / determinant * vx1
    if t1 >= 0 and t2 >= 0:
        t1 = round(t1)
        t2 = round(t2)
        ix = x1 + t1 * vx1
        iy = y1 + t1 * vy1
        iz = z1 + t1 * vz1
        if swapped:
            ix, iz = iz, ix
        return (ix, iy, iz)
    else:
        return (-2 ** 64, -2 ** 64, -2 ** 64)

def part2():
    ans = 0
    # a big system of equations
    # variables: x, y, z, vx, vy, vz, t1, ..., t300
    # 300 * 3 = 900 equations
    # only need 306, so just first 102 pts

    # consider subtract v from all velocity, then everything will collide at starting loc
    # since velocity is somewhat small, I guess the v might turn out to be small as well...?
    # stored = None
    # success = False
    # xl = []
    # yl = []
    # zl = []
    # vxl = []
    # vyl = []
    # vzl = []
    # ax = plt.axes(projection='3d')
    # t = 100000000000
    # k = 2 ** 64
    # ki = None
    # for i, (x, y, z, vx, vy, vz) in enumerate(parsed):
    #     l = vx * vx + vy * vy + vz * vz
    #     if l < k:
    #         ki = i
    #         k = l
    #     xl.append(x)
    #     yl.append(y)
    #     zl.append(z)
    #     ax.plot([x, x + t * vx], [y, y + t * vy], zs=[z, z + t * vz])
    # assert ki is not None
    # ax.scatter3D(xl, yl, zl)
    # ax.scatter3D(vxl, vyl, vzl, color="red")
    # ax.scatter3D(parsed[ki][0], parsed[ki][1], parsed[ki][2], color="green")
    # t = 10000000000000
    # ax.plot([parsed[ki][0], parsed[ki][0] + t * parsed[ki][3]], [parsed[ki][1], parsed[ki][1] + t * parsed[ki][4]], zs=[parsed[ki][2], parsed[ki][2] + t * parsed[ki][5]], color="green")
    # # plt.scatter(vxl, vyl, color="blue")
    # plt.show()
    # p = list(sorted(parsed, key=lambda k: k[3] * k[3] + k[4] * k[4] + k[5] * k[5]))
    # print(p)
    # exit(0)
    # for vx in tqdm(range(-200, 200)):
    #     for vy in range(-200, 200):
    #         for vz in range(-200, 200):
    #             stored = None
    #             fail = False
    #             for i in range(len(parsed)):
    #                 for j in range(i + 1, len(parsed)):
    #                     coord = collide(vx, vy, vz, parsed[i], parsed[j])
    #                     if stored is None:
    #                         stored = coord
    #                     elif stored != coord:
    #                         fail = True
    #                         break
    #                 if fail:
    #                     break
    #             if not fail:
    #                 success = True
    #             if success:
    #                 break
    #         if success:
    #             break
    #     if success:
    #         break
    # assert success
    # assert stored is not None
    # ans = stored[0] + stored[1] + stored[2]
    x, y, z, vx, vy, vz = z3.Int("x"), z3.Int("y"), z3.Int("z"), z3.Int("vx"), z3.Int("vy"), z3.Int("vz")
    t = [z3.Int(f"t{i}") for i in range(len(parsed))]
    s = z3.Solver()
    for i in range(len(parsed)):
        x1, y1, z1, vx1, vy1, vz1 = parsed[i]
        # x + t1 vx = x1 + t1 vx1
        # x + t1 vx = x1 + t1 vx1
        s.add(x + t[i] * vx == z3.IntVal(x1) + t[i] * z3.IntVal(vx1))
        s.add(y + t[i] * vy == z3.IntVal(y1) + t[i] * z3.IntVal(vy1))
        s.add(z + t[i] * vz == z3.IntVal(z1) + t[i] * z3.IntVal(vz1))
    print(s)
    print(s.check())
    m = s.model()
    print(m)
    ans = m.evaluate(x + y + z)
    print(f"Part 2: {ans}")
    copy_to_clipboard(str(ans))

if __name__ == "__main__":
    part1()
    part2()
