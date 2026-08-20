#!/usr/bin/env python3
import argparse, json
from pathlib import Path
from collections import defaultdict

def load_jsons(d):
    rows=[]
    for p in Path(d).rglob("*.json"):
        try:
            x=json.loads(p.read_text(encoding="utf-8"))
            rows.extend(x if isinstance(x,list) else [x])
        except Exception:
            pass
    return rows

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--normalized-dir", required=True)
    ap.add_argument("--diff-dir", required=False)
    ap.add_argument("--output", required=True)
    args=ap.parse_args()

    rows=load_jsons(args.normalized_dir)
    nodes=[]; edges=[]
    by_table=defaultdict(list); by_ref=defaultdict(list); by_stem=defaultdict(list)
    for i,r in enumerate(rows):
        nid=f"N{i:05d}"
        nodes.append({"id":nid,"path":r.get("path"),"file_type":r.get("file_type"),
                      "tables":r.get("tables",[]),"fields":r.get("fields",[]),
                      "actions":r.get("actions",[]),"pages":r.get("pages",[])})
        for t in r.get("tables",[]): by_table[t].append(nid)
        for ref in r.get("references",[]): by_ref[ref].append(nid)
        stem=Path(r.get("path","")).stem.lower()
        if stem: by_stem[stem].append(nid)

    seen=set()
    def link(group, reason, value):
        ids=list(dict.fromkeys(group))
        for a_i in range(len(ids)):
            for b_i in range(a_i+1,len(ids)):
                a,b=ids[a_i],ids[b_i]
                key=(a,b,reason,value)
                if key not in seen:
                    seen.add(key); edges.append({"source":a,"target":b,"reason":reason,"value":value})
    for k,v in by_table.items():
        if len(v)>1: link(v,"shared_table",k)
    for k,v in by_ref.items():
        if len(v)>1: link(v,"shared_reference",k)
    for k,v in by_stem.items():
        if len(v)>1: link(v,"same_stem",k)

    out={"nodes":nodes,"edges":edges}
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    Path(args.output).write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding="utf-8")
    print(args.output)

if __name__=="__main__":
    main()
