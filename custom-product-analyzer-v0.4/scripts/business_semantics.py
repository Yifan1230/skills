#!/usr/bin/env python3
"""
从“已发生变化的文本文件”中抽取业务语义线索，供 Product Analyst Pass 使用。
不会判断产品问题，只负责收集用户可见中文、标签、提示语、注释等证据。
"""
import argparse, json, re
from pathlib import Path

SAFE_EXTS = {".epg",".epm",".epmx",".edm",".edmx",".eda",".dic",".xml",".java",".jsp",".js",".html",".txt"}
EXCLUDE_PARTS = {".svn","ROOT","server","lib",".sonar","classes","pub_classes","node_modules"}
SENSITIVE = re.compile(r"(password|passwd|pwd|secret|token|private.?key|jdbc|certificate|cer\b)", re.I)
CHINESE = re.compile(r"[\u4e00-\u9fff][\u4e00-\u9fffA-Za-z0-9（）()、，。；：:._\-/\s]{1,80}")

def extract_file(p):
    try:
        text = p.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return []
    rows=[]
    for i,line in enumerate(text.splitlines(),1):
        if SENSITIVE.search(line):
            continue
        for m in CHINESE.finditer(line):
            s=" ".join(m.group(0).split()).strip(" ,，;；:：")
            if len(s) < 2:
                continue
            if len(s) > 100:
                s=s[:100]
            rows.append({"line":i,"text":s})
    seen=set(); out=[]
    for r in rows:
        key=r["text"]
        if key not in seen:
            seen.add(key); out.append(r)
    return out[:300]

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--input", required=True, help="单文件、目录，或 file_diff.json")
    ap.add_argument("--variant-root", help="当 input 为 diff.json 时必填")
    ap.add_argument("--output", required=True)
    args=ap.parse_args()

    inp=Path(args.input)
    files=[]
    if inp.is_file() and inp.suffix.lower()==".json":
        try:
            d=json.loads(inp.read_text(encoding="utf-8"))
            paths=(d.get("added",[])+d.get("modified",[]))
            if args.variant_root:
                root=Path(args.variant_root)
                files=[root/p for p in paths]
        except Exception:
            pass
    elif inp.is_file():
        files=[inp]
    else:
        for p in inp.rglob("*"):
            if p.is_file():
                files.append(p)

    result=[]
    for p in files:
        if not p.exists() or p.suffix.lower() not in SAFE_EXTS:
            continue
        if any(part in EXCLUDE_PARTS for part in p.parts):
            continue
        clues=extract_file(p)
        if clues:
            result.append({
                "path":str(p),
                "business_clues":clues
            })

    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    Path(args.output).write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding="utf-8")
    print(args.output)

if __name__=="__main__":
    main()
