#!/usr/bin/env python3
import argparse, json, hashlib, difflib
from pathlib import Path

EXCLUDE_DIRS={".svn","ROOT","server","lib",".sonar","classes","pub_classes","node_modules"}
TEXT_EXTS={".epg",".epm",".epmx",".edm",".edmx",".eda",".dic",".xml",".java",".jsp",".js",".html",".json",".txt",".properties"}

def excluded(rel):
    return any(p in EXCLUDE_DIRS for p in rel.parts) or rel.name.lower() in {"jdbc.properties","emap.properties"}

def collect(root):
    root=Path(root); out={}
    for p in root.rglob("*"):
        if not p.is_file(): continue
        rel=p.relative_to(root)
        if excluded(rel): continue
        if p.suffix.lower() not in TEXT_EXTS: continue
        try:
            b=p.read_bytes()
        except Exception:
            continue
        out[rel.as_posix()]={"hash":hashlib.sha256(b).hexdigest(),"size":len(b)}
    return out

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--baseline", required=True)
    ap.add_argument("--variant", required=True)
    ap.add_argument("--output", required=True)
    args=ap.parse_args()

    b=collect(args.baseline); v=collect(args.variant)
    bs=set(b); vs=set(v)
    added=sorted(vs-bs); removed=sorted(bs-vs)
    modified=sorted(p for p in bs&vs if b[p]["hash"]!=v[p]["hash"])
    out={
      "baseline":args.baseline,
      "variant":args.variant,
      "added":added,
      "removed":removed,
      "modified":modified,
      "summary":{"added":len(added),"removed":len(removed),"modified":len(modified)}
    }
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    Path(args.output).write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding="utf-8")
    print(args.output)

if __name__=="__main__":
    main()
