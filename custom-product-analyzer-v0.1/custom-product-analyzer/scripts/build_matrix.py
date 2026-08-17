#!/usr/bin/env python3
import argparse, json, csv
from pathlib import Path

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--features-dir", required=True)
    ap.add_argument("--output", required=True)
    args=ap.parse_args()

    rows=[]
    for p in Path(args.features_dir).rglob("*.json"):
        try:
            x=json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            continue
        items=x if isinstance(x,list) else x.get("feature_variants",[x])
        for r in items:
            if not isinstance(r,dict): continue
            if "feature_id" not in r or "customer" not in r: continue
            rows.append({
                "customer":r.get("customer",""),
                "actual_app":r.get("actual_app",""),
                "feature_id":r.get("feature_id",""),
                "feature_name":r.get("feature_name",""),
                "variant_name":r.get("variant_name",""),
                "presence":r.get("presence",True),
                "confidence":r.get("confidence",""),
                "baseline_quality":r.get("baseline_quality","")
            })
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    with open(args.output,"w",newline="",encoding="utf-8-sig") as f:
        w=csv.DictWriter(f,fieldnames=["customer","actual_app","feature_id","feature_name","variant_name","presence","confidence","baseline_quality"])
        w.writeheader(); w.writerows(rows)
    print(args.output)

if __name__=="__main__":
    main()
