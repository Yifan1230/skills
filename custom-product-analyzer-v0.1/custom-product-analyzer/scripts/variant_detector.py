#!/usr/bin/env python3
"""
兼容入口：V0.1 中 Variant Detection 已由 inventory.py 完成。
保留此脚本作为稳定命令入口，后续可扩展结构相似度匹配。
"""
import subprocess, sys
if __name__ == "__main__":
    cmd=[sys.executable, str(__import__("pathlib").Path(__file__).with_name("inventory.py"))] + sys.argv[1:]
    raise SystemExit(subprocess.call(cmd))
