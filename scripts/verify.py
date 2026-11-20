#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
校验 Telegram 语言包

用法：
    python scripts/verify.py pack/tg-zh-hans-v0.1.json

检查项：
    1. 编码为 UTF-8 且不含 BOM
    2. 顶层字段齐全：name / version / updated / strings
    3. strings 内无重复键（JSON 默认静默覆盖，这里会报错）
    4. 所有键与值为非空字符串
    5. 输出体积与 SHA-256，便于与发布页比对

退出码：0 通过，1 失败。
"""
import hashlib
import json
import os
import sys

REQUIRED = ("name", "version", "updated", "strings")
MAX_SIZE = 200 * 1024
BOM = b"\xef\xbb\xbf"


def main(path):
    ok = True

    def fail(msg):
        print("  x " + msg)
        return False

    if not os.path.exists(path):
        print("文件不存在：" + path)
        return 1

    raw = open(path, "rb").read()
    size = len(raw)
    sha = hashlib.sha256(raw).hexdigest()
    has_bom = raw.startswith(BOM)

    print("file      " + path)
    print("size      " + str(size) + " B")
    print("sha256    " + sha)

    if has_bom:
        ok = fail("文件带 BOM，客户端可能解析失败")

    try:
        text = raw.decode("utf-8-sig")
    except UnicodeDecodeError as e:
        fail("不是合法 UTF-8：" + str(e))
        return 1

    dups = []

    def hook(pairs):
        seen = {}
        for k, v in pairs:
            if k in seen:
                dups.append(k)
            seen[k] = v
        return seen

    try:
        data = json.loads(text, object_pairs_hook=hook)
    except json.JSONDecodeError as e:
        fail("JSON 解析失败：" + str(e))
        return 1

    if dups:
        ok = fail("存在重复键：" + ", ".join(sorted(set(dups))))

    if not isinstance(data, dict):
        fail("顶层必须是对象")
        return 1

    for k in REQUIRED:
        if k not in data:
            ok = fail("缺字段：" + k)

    strings = data.get("strings", {})
    if not isinstance(strings, dict):
        ok = fail("strings 必须是对象")
        strings = {}

    print("keys      " + str(len(strings)))
    if not strings:
        ok = fail("strings 为空")

    bad = []
    for k, v in strings.items():
        if not isinstance(k, str) or not k.strip() or not isinstance(v, str) or not v.strip():
            bad.append(str(k))
    if bad:
        ok = fail(str(len(bad)) + " 条键或值为空/非字符串：" + ", ".join(bad[:5]))

    if size > MAX_SIZE:
        ok = fail("体积 " + str(size) + " B 超过 200 KB，语言包不应这么大")

    enc = "utf-8 (with BOM)" if has_bom else "utf-8"
    print("encoding  " + enc)
    print("version   " + str(data.get("version", "-")) + "   updated " + str(data.get("updated", "-")))
    print("result    " + ("OK" if ok else "FAILED"))
    return 0 if ok else 1


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(1)
    sys.exit(main(sys.argv[1]))
