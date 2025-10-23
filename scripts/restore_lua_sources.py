#!/usr/bin/env python3
import os
import re
from datetime import datetime

ROOT = "/workspace/final_lua_project"

# 需要处理的模块及其 src 目录
MODULES = [
    ("Core", os.path.join(ROOT, "Core", "src")),
    ("DFMGameHud", os.path.join(ROOT, "DFMGameHud", "src")),
    ("DFMAbility", os.path.join(ROOT, "DFMAbility", "src")),
    ("UI", os.path.join(ROOT, "UI", "src")),
    ("Other", os.path.join(ROOT, "Other", "src")),
]

FUNC_SIG_RE = re.compile(r"^--\s*(?:蓝图系统函数|事件系统函数|C\+\+方法):\s*([A-Za-z0-9_:]+)", re.M)
CONST_RE = re.compile(r"^--\s*local\s+([A-Za-z0-9_]+)$", re.M)

HEADER = """-- 由工具自动生成函数桩于 {ts}
-- 注意：以下为基于字节码信息推断的函数/常量桩，需要按业务补全
"""


def build_function_stub(name: str) -> str:
    if "::" in name:
        cls, method = name.split("::", 1)
        sig = f"function {cls}:{method}()"
    else:
        sig = f"function {name}()"
    body = [
        sig,
        "    -- TODO: 根据业务逻辑补全实现",
        "    return nil",
        "end",
        "",
    ]
    return "\n".join(body)


def transform_file(path: str) -> bool:
    # 仅处理 *_decoded.lua
    if not path.endswith("_decoded.lua"):
        return False
    changed = False
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # 收集常量名
    consts = CONST_RE.findall(content)
    # 收集函数签名名
    funcs = FUNC_SIG_RE.findall(content)

    # 如果已经存在实际 function 关键字实现，避免重复生成
    has_real_funcs = re.search(r"^function\s+", content, re.M) is not None

    out_lines = []
    out_lines.append(HEADER.format(ts=datetime.now()))

    # 原文件头保留注释首段（最多前30行注释）
    lines = content.splitlines()
    for i, line in enumerate(lines[:30]):
        if line.strip().startswith("--"):
            out_lines.append(line)
        else:
            break
    out_lines.append("")

    # 常量局部占位
    if consts:
        out_lines.append("-- 常量占位")
        for c in sorted(set(consts))[:50]:
            out_lines.append(f"local {c} = nil")
        out_lines.append("")

    # 函数桩
    if not has_real_funcs and funcs:
        out_lines.append("-- 函数桩")
        for fn in sorted(set(funcs))[:50]:
            out_lines.append(build_function_stub(fn))
        changed = True

    # 若没有任何可生成的结构，则不修改
    if not changed and not consts:
        return False

    new_content = "\n".join(out_lines).rstrip() + "\n"

    with open(path, "w", encoding="utf-8") as f:
        f.write(new_content)
    return True


def enable_requires(init_path: str, module_src_dir: str):
    # 启用 init.lua 的 require 行，改为无注释形式
    if not os.path.exists(init_path):
        return False
    with open(init_path, "r", encoding="utf-8") as f:
        init_content = f.read()

    lines = init_content.splitlines()
    new_lines = []
    changed = False
    for line in lines:
        m = re.match(r"^\s*--\s*require\s*'([^']+)'\s*$", line)
        if m:
            base = m.group(1)  # e.g., file_10_decoded
            # 只启用对应文件实际存在时
            lua_path = os.path.join(module_src_dir, base + ".lua")
            if os.path.exists(lua_path):
                new_lines.append(f"require '{base}'")
                changed = True
            else:
                new_lines.append(line)
        else:
            new_lines.append(line)

    if changed:
        with open(init_path, "w", encoding="utf-8") as f:
            f.write("\n".join(new_lines) + "\n")
    return changed


def main():
    total_changed = 0
    # 1) 生成函数桩/常量占位
    for module, src in MODULES:
        if not os.path.isdir(src):
            continue
        for name in sorted(os.listdir(src)):
            if name.endswith(".lua"):
                p = os.path.join(src, name)
                if transform_file(p):
                    total_changed += 1

    # 2) 启用各模块 init.lua 的 require 行
    init_changes = 0
    for module, src in MODULES:
        init_path = os.path.join(src, "init.lua")
        if enable_requires(init_path, src):
            init_changes += 1

    print(f"transformed files: {total_changed}")
    print(f"updated inits: {init_changes}")

if __name__ == "__main__":
    main()
