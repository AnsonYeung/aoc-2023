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
    bag_content = (12, 13, 14)
    for row in data:
        id = re.findall(r"\d+", row.split(":")[0])[0]
        rest = row.split(":")[1]
        ok = True
        for content in rest.split(";"):
            red = re.findall(r"\d+ red", content)
            if len(red) > 0 and int(red[0][:-4]) > bag_content[0]:
                ok = False
                break
            green = re.findall(r"\d+ green", content)
            if len(green) > 0 and int(green[0][:-6]) > bag_content[1]:
                ok = False
                break
            blue = re.findall(r"\d+ blue", content)
            if len(blue) > 0 and int(blue[0][:-5]) > bag_content[2]:
                ok = False
                break
        if ok:
            ans += int(id)
    submit(1, ans)

def part2():
    ans = 0
    for row in data:
        id = re.findall(r"\d+", row.split(":")[0])[0]
        rest = row.split(":")[1]
        ok = True
        r_max = 0
        g_max = 0
        b_max = 0
        for content in rest.split(";"):
            red = re.findall(r"\d+ red", content)
            r_num = 0 if len(red) == 0 else int(red[0][:-4])
            green = re.findall(r"\d+ green", content)
            g_num = 0 if len(green) == 0 else int(green[0][:-6])
            blue = re.findall(r"\d+ blue", content)
            b_num = 0 if len(blue) == 0 else int(blue[0][:-5])
            r_max = max(r_max, r_num)
            g_max = max(g_max, g_num)
            b_max = max(b_max, b_num)
        ans += r_max * g_max * b_max
    submit(2, ans)

if __name__ == "__main__":
    part1()
    part2()
