#!/usr/bin/env python3
"""数一遍全书在用的 Artifacts 标签，按类别列出。改完标签用它复查词表有没有又散开。"""
import json
import os
import re
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FAM = [("img", "图像"), ("txt", "文本"), ("code", "代码"),
       ("run", "可运行件"), ("asset", "资产"), ("meta", "结构化字段")]


def collect():
    fam = defaultdict(lambda: defaultdict(int))
    for f in os.listdir(os.path.join(ROOT, "data")):
        if not f.endswith(".json"):
            continue
        try:
            d = json.load(open(os.path.join(ROOT, "data", f), encoding="utf-8"))
        except Exception:
            continue
        for r in d if isinstance(d, list) else []:
            for it in (r or {}).get("artifacts") or []:
                k, _, v = it.partition(":")
                fam[k][v] += 1
    for sub in ("web", "3d", "video"):
        d = os.path.join(ROOT, "parts", sub)
        for f in (os.listdir(d) if os.path.isdir(d) else []):
            if not f.endswith(".md"):
                continue
            for k, v in re.findall(r'class="art a-(\w+)">([^<]*)<',
                                   open(os.path.join(d, f), encoding="utf-8").read()):
                fam[k][v] += 1
    return fam


if __name__ == "__main__":
    fam, total = collect(), 0
    for key, cn in FAM:
        vs = sorted(fam.get(key, {}).items(), key=lambda kv: -kv[1])
        total += len(vs)
        print(f"\n{cn}（{key}）— {len(vs)} 个标签")
        for v, n in vs:
            print(f"    {n:>3} ×  {v}")
    extra = set(fam) - {k for k, _ in FAM}
    if extra:
        print("\n[warn] 不在六类里的家族:", extra)
    print(f"\n合计 {total} 个标签")

