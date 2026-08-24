#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
业务线索盘点器。

它只帮助定位值得进一步阅读的源码文件，不直接判断业务含义。
所有输出都是候选线索，必须结合 SKILL.md 做业务分析。

用法：
    python business_inventory.py /path/to/project -o business-inventory.json
"""
import argparse
import json
from pathlib import Path
from collections import Counter, defaultdict

IGNORED = {
    ".git", "node_modules", "dist", "build", "target", ".idea", ".vscode",
    "__pycache__", ".next", ".nuxt", "coverage", "vendor", "venv", ".venv"
}
TEXT_EXTS = {
    ".java", ".kt", ".py", ".js", ".jsx", ".ts", ".tsx", ".vue", ".svelte",
    ".xml", ".yml", ".yaml", ".json", ".sql", ".properties", ".md", ".html"
}
FILE_HINTS = {
    "页面/入口": ["page", "view", "route", "router", "menu", "页面", "菜单"],
    "业务处理": ["service", "manager", "handler", "process", "workflow", "flow", "审核", "评审"],
    "业务对象": ["entity", "model", "domain", "dto", "对象", "模型"],
    "数据访问": ["mapper", "repository", "dao", "sql"],
    "状态/字典": ["enum", "constant", "dict", "status", "state", "字典", "状态"],
    "权限": ["permission", "auth", "role", "guard", "权限", "角色"],
    "配置": ["config", "setting", "properties", "yaml", "yml", "配置"],
    "自动处理": ["schedule", "scheduler", "job", "task", "listener", "event", "cron", "定时", "任务"]
}
BUSINESS_TERMS = [
    "status", "state", "stage", "type", "role", "permission", "approve", "audit", "review",
    "reject", "return", "withdraw", "cancel", "terminate", "submit", "resubmit", "timeout",
    "deadline", "config", "状态", "阶段", "类型", "角色", "权限", "审核", "评审", "驳回",
    "退回", "撤回", "取消", "终止", "提交", "重新提交", "超时", "截止", "配置", "延期", "变更", "作废"
]

def iter_files(root):
    for p in root.rglob("*"):
        if not p.is_file():
            continue
        if any(part in IGNORED for part in p.parts):
            continue
        if p.suffix.lower() in TEXT_EXTS:
            yield p

def classify(name):
    low = name.lower()
    result = []
    for cat, hints in FILE_HINTS.items():
        if any(h.lower() in low for h in hints):
            result.append(cat)
    return result

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("project")
    ap.add_argument("-o", "--output", default="business-inventory.json")
    args = ap.parse_args()

    root = Path(args.project).resolve()
    by_category = defaultdict(list)
    signal_files = []
    ext_count = Counter()
    total = 0

    for p in iter_files(root):
        total += 1
        ext_count[p.suffix.lower()] += 1
        rel = str(p.relative_to(root))
        for cat in classify(p.name):
            by_category[cat].append(rel)
        try:
            text = p.read_text(encoding="utf-8", errors="ignore").lower()
        except Exception:
            continue
        counts = {}
        for term in BUSINESS_TERMS:
            c = text.count(term.lower())
            if c:
                counts[term] = c
        score = sum(counts.values())
        if score:
            signal_files.append({
                "file": rel,
                "business_signal_score": score,
                "keywords": dict(sorted(counts.items(), key=lambda x: -x[1])[:20])
            })

    signal_files.sort(key=lambda x: -x["business_signal_score"])
    result = {
        "notice": "本结果仅为候选业务线索，不代表业务结论。",
        "project": str(root),
        "total_text_files": total,
        "file_extensions": dict(ext_count.most_common()),
        "candidate_files": {k: sorted(v) for k, v in by_category.items()},
        "business_signal_files": signal_files[:200]
    }
    Path(args.output).write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"已生成: {args.output}")
    print(f"扫描文本文件: {total}")
    print(f"业务线索文件: {len(signal_files)}")

if __name__ == "__main__":
    main()
