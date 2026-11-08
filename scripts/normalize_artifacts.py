#!/usr/bin/env python3
"""把 Artifacts 标签收进一套固定词表。

规范：
  一个标签 = 一个物件名。同义词归一，限定语写进括号，文件类型直接用扩展名。
  六个类别（颜色见 template.html 的 .a-*）：
    img   图像      渲染出来的画面，是比对的那一端
    txt   文本      人写或模型写的自然语言
    code  代码      要再经一道工具才出画面的源码与中间表示
    run   可运行件  跑一次就出画面的整件
    asset 资产      几何与贴图，不含代码
    meta  结构化字段 可逐项比对的机器可读字段

跑完用 inventory_artifacts.py 复查词表大小。幂等：已经归一过的再跑一次不变。
"""
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")

# 旧标签 -> 新标签。键是「家族:旧名」，值是「家族:新名」（家族也可以改）
MAP = {
    # ---- 图像 ----
    "img:image": "img:截图", "img:GUI 截图": "img:截图", "img:渲染结果": "img:截图",
    "img:富文本图": "img:截图", "img:多状态截图": "img:截图（多状态）",
    "img:交互前后截图": "img:截图（交互前后）",
    "img:图表": "img:图表图", "img:真实图表": "img:图表图",
    "img:设计图": "img:设计稿", "img:草图": "img:手绘草图",
    "img:4 视角图": "img:多视角图",
    "img:截图断言": "img:截图",          # 断言那一半拆到 code
    # ---- 文本 ----
    "txt:title": "txt:标题", "txt:desc": "txt:描述", "txt:desc 9%": "txt:描述（9%）",
    "txt:text": "txt:描述", "txt:text 多级": "txt:描述（多级）", "txt:caption": "txt:描述",
    "txt:意图": "txt:描述", "txt:固定指令": "txt:指令（固定）", "txt:编辑指令": "txt:指令（编辑）",
    "txt:多轮": "txt:指令（多轮）", "txt:QA": "txt:问答", "txt:网页 QA": "txt:问答",
    "txt:问题": "txt:问题描述", "txt:文字答案": "txt:答案",
    "txt:多步 agent 轨迹": "txt:轨迹（agent）", "txt:多轮修复轨迹": "txt:轨迹（多轮修复）",
    "txt:生成→诊断→修复轨迹": "txt:轨迹（修复）", "txt:设计推理": "txt:推理过程",
    # ---- 代码 ----
    "code:CadQuery 代码": "code:CadQuery .py", "code:分部件 bpy .py": "code:bpy .py（分部件）",
    "code:编辑后 bpy .py": "code:bpy .py（编辑后）", "code:插件 .py": "code:.py（插件）",
    "code:起始脚本": "code:.py（起始）", "code:原代码": "code:源码",
    "code:代码": "code:源码", "code:多域代码": "code:源码（多域）",
    "code:12 语言可视化代码": "code:绘图代码（12 语言）", "code:渲染代码": "code:绘图代码",
    "code:脚本片段": "code:代码片段", "code:片段链接": "code:代码片段",
    "code:组件代码": "code:源码", "code:交互代码": "code:源码（交互）",
    "code:p5 草图 .js": "code:.js（p5 草图）", "code:GLSL 片段着色器": "code:GLSL",
    "code:patch": "code:补丁", "code:.ts¹": "code:.ts",
    "code:CAD 构造序列": "code:CAD 序列（构造）", "code:CAD 命令序列": "code:CAD 序列（命令）",
    # ---- 可运行件 ----
    "run:three.js .html": "run:.html", "run:交互 .html": "run:.html",
    "run:线上 .html": "run:.html", "run:HTML 文档": "run:.html",
    "run:.html Tailwind": "run:.html（Tailwind）",
    "run:多文件网站": "run:多文件工程", "run:多文件静态站": "run:多文件工程",
    "run:多文件前端工程": "run:多文件工程",
    "run:少量 .blend": "run:.blend（少量）",
    # ---- 资产 ----
    "asset:网格文件": "asset:网格", "asset:模型": "asset:网格", "asset:3D 模型": "asset:网格",
    "asset:GLB 资产": "asset:网格（GLB）", "asset:OBJ / USD": "asset:网格（OBJ / USD）",
    # ---- 结构化字段 ----
    "meta:包围盒": "meta:布局框", "meta:元素": "meta:布局框",
    "meta:checklist": "meta:评分项", "meta:简化 HTML 解析": "meta:简化解析树",
}

# 这些行要把一个标签拆成两个（原标签把两件事写在一起了）
SPLIT = {"img:截图断言": ["img:截图", "code:断言"]}


def norm(items):
    out = []
    for it in items or []:
        for x in SPLIT.get(it, [MAP.get(it, it)]):
            if x not in out:
                out.append(x)
    return out


def main():
    changed = 0
    for f in ("pipe_meta_web.json", "repo_meta_web.json", "site_meta_web.json",
              "pipe_meta_3dgame.json", "repo_meta_3d.json", "site_meta_3d.json"):
        p = os.path.join(DATA, f)
        if not os.path.isfile(p):
            continue
        d = json.load(open(p, encoding="utf-8"))
        for r in d:
            if "artifacts" in r:
                new = norm(r["artifacts"])
                changed += new != r["artifacts"]
                r["artifacts"] = new
        json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=2)

    # markdown 里手写的标签
    for f in ("parts/web/verified.md", "parts/3d/verified.md"):
        p = os.path.join(ROOT, f)
        t = open(p, encoding="utf-8").read()

        def repl(m):
            tag = f"{m.group(1)}:{m.group(2)}"
            outs = SPLIT.get(tag, [MAP.get(tag, tag)])
            return "".join(f'<span class="art a-{o.split(":")[0]}">{o.split(":", 1)[1]}</span>' for o in outs)
        t2 = re.sub(r'<span class="art a-(\w+)">([^<]*)</span>', repl, t)
        changed += t2 != t
        open(p, "w", encoding="utf-8").write(t2)

    print(f"归一完成，{changed} 处有改动" if changed else "已经是规范词表，没有改动")
    return 0


if __name__ == "__main__":
    sys.exit(main())

