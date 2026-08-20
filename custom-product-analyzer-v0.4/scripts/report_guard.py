#!/usr/bin/env python3
"""
校验最终报告“产品经理决策区”是否仍混入技术语言。
失败时退出码 2，Agent 必须重写报告后再次运行。
"""
import argparse, re
from pathlib import Path

START="<!-- PM_DECISION_START -->"
END="<!-- PM_DECISION_END -->"

FORBIDDEN = [
    (r"\bconfiguration_candidate\b","内部枚举 configuration_candidate"),
    (r"\bproductization_candidate\b","内部枚举 productization_candidate"),
    (r"\bstrong_productization_candidate\b","内部枚举 strong_productization_candidate"),
    (r"\bkeep_custom\b","内部枚举 keep_custom"),
    (r"\bobserve\b","内部枚举 observe"),
    (r"\.(?:java|epm|epmx|edm|edmx|eda|epg|jsp)\b","技术文件后缀"),
    (r"\bhutool\b","工具库 hutool"),
    (r"\b(?:controller|service|dao|jar|sdk)\b","技术实现词"),
    (r"\bhash\b","hash 技术词"),
    (r"版本漂移项","“版本漂移项”不是产品问题"),
    (r"\bCU-\d+\b","Change Unit 编号"),
    (r"\bF-\d+\b","Feature 编号"),
]

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--report", required=True)
    args=ap.parse_args()
    text=Path(args.report).read_text(encoding="utf-8", errors="ignore")

    if START not in text or END not in text:
        print("FAIL: 缺少 PM_DECISION_START / PM_DECISION_END 标记。")
        raise SystemExit(2)

    section=text.split(START,1)[1].split(END,1)[0]
    errors=[]
    for pat,msg in FORBIDDEN:
        for m in re.finditer(pat, section, flags=re.I):
            line=section.count("\n",0,m.start())+1
            errors.append(f"line {line}: {msg}: {m.group(0)}")

    required=["标品当前行为","客户版本行为","用户感知差异"]
    for r in required:
        if r not in section:
            errors.append(f"缺少必要产品栏目：{r}")

    if errors:
        print("FAIL: 产品经理决策区仍不符合产品语言要求：")
        for e in errors[:50]:
            print(" -",e)
        print("\n请重写决策区，不要删除技术附录；技术信息移到 PM_DECISION_END 之后。")
        raise SystemExit(2)

    print("PASS: 产品经理决策区通过语言门槛。")

if __name__=="__main__":
    main()
