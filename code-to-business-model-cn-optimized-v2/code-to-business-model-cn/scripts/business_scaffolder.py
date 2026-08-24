#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""快速生成 business-analysis/ 目录。"""
import argparse
from pathlib import Path

FILES = {
    "README.md": "# 现状业务模型\n\n## 系统定位\n\n## 核心业务域\n\n## 核心业务对象\n\n## 核心流程\n\n## 覆盖情况\n",
    "01-系统模块地图.md": "# 系统模块地图\n\n",
    "02-业务对象模型.md": "# 业务对象模型\n\n",
    "03-生命周期.md": "# 生命周期\n\n",
    "04-业务规则与决策表.md": "# 业务规则与决策表\n\n",
    "05-业务场景库.md": "# 业务场景库\n\n",
    "06-完整业务流程.md": "# 完整业务流程\n\n",
    "07-角色与权限.md": "# 角色与权限\n\n",
    "08-配置模型.md": "# 配置模型\n\n",
    "09-异常与特殊流程.md": "# 异常与特殊流程\n\n",
    "10-页面与业务映射.md": "# 页面与业务映射\n\n",
    "11-业务规则证据表.md": "# 业务规则证据表\n\n",
    "12-覆盖检查.md": "# 覆盖检查\n\n",
    "13-待确认问题.md": "# 待确认问题\n\n",
    "_progress.md": "# 分析进度\n\n## 已完成模块\n\n## 当前模块\n\n## 待分析模块\n\n## 编号进度\n\n## 待确认问题\n"
}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("project")
    ap.add_argument("-o", "--output", default=None)
    args = ap.parse_args()
    project = Path(args.project).resolve()
    out = Path(args.output).resolve() if args.output else project / "business-analysis"
    out.mkdir(parents=True, exist_ok=True)
    for name, content in FILES.items():
        p = out / name
        if not p.exists():
            p.write_text(content, encoding="utf-8")
    print(f"已生成业务分析目录: {out}")

if __name__ == "__main__":
    main()
