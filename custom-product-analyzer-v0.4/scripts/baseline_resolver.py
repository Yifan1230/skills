#!/usr/bin/env python3
import argparse, json, hashlib, os
from pathlib import Path
from collections import defaultdict, Counter

EXCLUDE_DIRS = {".svn","ROOT","server","lib",".sonar","classes","pub_classes","node_modules"}
INCLUDE_EXTS = {".epg",".epm",".epmx",".edm",".edmx",".eda",".dic",".xml",".java",".jsp",".js",".html",".json",".txt"}

def major_version(v):
    if not v: return "unknown"
    parts = v.split(".")
    if len(parts) >= 2 and parts[0].isdigit():
        return ".".join(parts[:2])
    return v

def safe_files(root):
    root = Path(root)
    for p in root.rglob("*"):
        if not p.is_file(): continue
        rel = p.relative_to(root)
        if any(part in EXCLUDE_DIRS for part in rel.parts): continue
        if p.suffix.lower() not in INCLUDE_EXTS: continue
        if p.name.lower() in {"jdbc.properties","emap.properties"}: continue
        yield p, rel.as_posix()

def digest(p):
    h = hashlib.sha256()
    try:
        with open(p,"rb") as f:
            for chunk in iter(lambda:f.read(1024*1024), b""):
                h.update(chunk)
        return h.hexdigest()
    except Exception:
        return None

def manifest(root):
    return {rel:digest(p) for p,rel in safe_files(root)}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--inventory", required=True)
    ap.add_argument("--product-app", required=True)
    ap.add_argument("--output-dir", required=True)
    ap.add_argument("--min-sources", type=int, default=3)
    ap.add_argument("--agreement", type=float, default=0.70)
    args=ap.parse_args()

    data=json.loads(Path(args.inventory).read_text(encoding="utf-8"))
    outdir=Path(args.output_dir); outdir.mkdir(parents=True, exist_ok=True)

    groups=defaultdict(list)
    for v in data["variants"]:
        groups[major_version(v.get("application_version"))].append(v)

    product_version=data.get("product_info",{}).get("application_version")
    product_major=major_version(product_version)
    result={"product_version":product_version,"groups":{}}

    for g,items in groups.items():
        entry={"group":g,"count":len(items),"baseline_type":"no_reliable_baseline","baseline_confidence":"low","sources":[]}
        # True baseline only when exact version equals current product version.
        exact=[x for x in items if x.get("application_version")==product_version]
        if exact and g==product_major:
            entry.update({
                "baseline_type":"true_baseline",
                "baseline_confidence":"high",
                "baseline_path":str(Path(args.product_app)),
                "sources":["current_product"]
            })
            result["groups"][g]=entry
            continue

        # Consensus pseudo-baseline via file-hash agreement.
        # Prefer same change_reference_id subgroups, otherwise entire version group.
        subgroups=defaultdict(list)
        for x in items:
            refs=x.get("change_reference_ids") or []
            key="|".join(refs) if refs else "__no_ref__"
            subgroups[key].append(x)
        best=None
        for key,sub in subgroups.items():
            if len(sub) < args.min_sources: continue
            manifests=[]
            for x in sub:
                p=Path(x["path"])
                if p.exists():
                    manifests.append((x,manifest(p)))
            if len(manifests)<args.min_sources: continue
            all_paths=set().union(*(m.keys() for _,m in manifests))
            agreed=0; considered=0
            consensus={}
            for rel in all_paths:
                vals=[m.get(rel) for _,m in manifests if m.get(rel)]
                if len(vals)<args.min_sources: continue
                considered+=1
                val,cnt=Counter(vals).most_common(1)[0]
                ratio=cnt/len(vals)
                if ratio>=args.agreement:
                    agreed+=1; consensus[rel]=val
            score=agreed/max(1,considered)
            cand=(score,key,sub,consensus,considered)
            if best is None or cand[0]>best[0]:
                best=cand
        if best and best[0]>=args.agreement:
            score,key,sub,consensus,considered=best
            manifest_path=outdir/f"{g.replace('.','_')}_consensus_manifest.json"
            manifest_path.write_text(json.dumps({
                "version_group":g,
                "change_reference_key":key,
                "agreement_score":score,
                "sources":[x["customer"] for x in sub],
                "consensus_hashes":consensus
            },ensure_ascii=False,indent=2),encoding="utf-8")
            entry.update({
                "baseline_type":"consensus_pseudo_baseline",
                "baseline_confidence":"medium",
                "baseline_manifest":str(manifest_path),
                "agreement_score":score,
                "sources":[x["customer"] for x in sub]
            })
        result["groups"][g]=entry

    (outdir/"baseline_resolution.json").write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding="utf-8")
    print(outdir/"baseline_resolution.json")

if __name__=="__main__":
    main()
