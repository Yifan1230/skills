#!/usr/bin/env python3
import argparse, json, re
from pathlib import Path
import xml.etree.ElementTree as ET

EXCLUDE_PARTS = {".svn","ROOT","server","lib",".sonar","classes","pub_classes","node_modules"}
DEPRECATED_WORDS = ["已合并","勿用","backup","bak","old","deprecated"]

def safe_text(root, names):
    for e in root.iter():
        tag = e.tag.split("}")[-1].lower()
        if tag in names and e.text:
            return e.text.strip()
    return None

def read_app_info(app_dir):
    p = app_dir / "app_info.xml"
    out = {"application_version":None,"emap_version":None,"identity":None}
    if not p.exists():
        return out
    try:
        root = ET.parse(p).getroot()
        out["application_version"] = safe_text(root, {"version"})
        out["emap_version"] = safe_text(root, {"emap_version","emapversion"})
        out["identity"] = safe_text(root, {"identity","id"})
    except Exception:
        pass
    return out

def read_change_refs(app_dir):
    refs = set()
    for name in ("version.json","version.txt"):
        p = app_dir / name
        if not p.exists(): continue
        try:
            text = p.read_text(encoding="utf-8", errors="ignore")
            for m in re.findall(r"(?<!\d)(?:jz)?\d{5,}(?!\d)", text, flags=re.I):
                refs.add(m)
        except Exception:
            pass
    return sorted(refs)

def iter_dirs(root, max_depth=5):
    root = Path(root)
    for p in root.rglob("*"):
        if not p.is_dir(): continue
        rel = p.relative_to(root)
        if len(rel.parts) > max_depth: continue
        if any(part in EXCLUDE_PARTS for part in rel.parts): continue
        yield p

def classify(canonical, p, product_identity=None):
    name = p.name
    lname = name.lower()
    can = canonical.lower()
    evidence = []
    typ = None
    conf = "low"
    if name == canonical:
        typ, conf = "standard-name", "high"; evidence.append("exact_name")
    elif name == canonical + "$A":
        typ, conf = "$A-extension", "high"; evidence.append("dollar_a_pattern")
    elif lname.startswith(can) and lname != can:
        suffix = lname[len(can):]
        if suffix and re.fullmatch(r"[a-z0-9_-]+", suffix):
            typ, conf = "school-suffix-copy", "medium"; evidence.append("suffix_pattern")
    if re.search(r"R\d+_", str(p.parent), flags=re.I):
        evidence.append("r_directory")
        typ = "r-directory-customization" if typ else "r-directory-customization"
        conf = "high" if name == canonical else conf
    info = read_app_info(p)
    if product_identity and info.get("identity") == product_identity:
        evidence.append("identity_match")
        if not typ:
            typ, conf = "identity-matched", "high"
    if not typ:
        return None
    if any(w.lower() in str(p).lower() for w in DEPRECATED_WORDS):
        conf = "low"
        evidence.append("deprecated_marker")
    return typ, conf, evidence, info

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--app", required=True)
    ap.add_argument("--product-root", required=True)
    ap.add_argument("--school-root", required=True)
    ap.add_argument("--output", required=True)
    args = ap.parse_args()

    product_app = Path(args.product_root) / args.app
    pinfo = read_app_info(product_app)
    product_identity = pinfo.get("identity")

    variants = []
    for school_dir in sorted(Path(args.school_root).iterdir()):
        if not school_dir.is_dir(): continue
        customer = school_dir.name.replace("gsapp_DZ_","").replace("gsapp_","")
        for p in iter_dirs(school_dir, max_depth=6):
            hit = classify(args.app, p, product_identity)
            if not hit: continue
            typ, conf, evidence, info = hit
            variants.append({
                "canonical_app": args.app,
                "customer": customer,
                "actual_app": p.name,
                "path": str(p),
                "application_version": info.get("application_version"),
                "emap_version": info.get("emap_version"),
                "identity": info.get("identity"),
                "change_reference_ids": read_change_refs(p),
                "variant_type": typ,
                "match_evidence": evidence,
                "match_confidence": conf
            })

    out = {
        "canonical_app": args.app,
        "product_app": str(product_app),
        "product_info": pinfo,
        "variant_count": len(variants),
        "variants": variants
    }
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    Path(args.output).write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(args.output)

if __name__ == "__main__":
    main()
