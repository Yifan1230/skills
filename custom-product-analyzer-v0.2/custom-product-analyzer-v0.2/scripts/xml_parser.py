#!/usr/bin/env python3
import argparse, json, re
from pathlib import Path
import xml.etree.ElementTree as ET

SENSITIVE = re.compile(r"(password|passwd|pwd|secret|token|private.?key|jdbc|cer$)", re.I)

def local(tag):
    return tag.split("}")[-1]

def classify(path):
    s=path.suffix.lower()
    n=path.name.lower()
    if s==".eda": return "eda"
    if s==".epg": return "epg"
    if s in {".epm",".epmx"}: return "epm"
    if s in {".edm",".edmx"}: return "edm"
    if s==".dic": return "dic"
    if n=="permission.xml": return "permission"
    if re.match(r"version\d*\.xml$", n): return "version"
    return "xml"

def parse_file(path):
    result={"path":str(path),"file_type":classify(path),"parse_status":"ok",
            "entities":[],"references":[],"tables":[],"fields":[],"actions":[],
            "pages":[],"permissions":[],"db_changes":[]}
    try:
        root=ET.parse(path).getroot()
    except Exception as e:
        result["parse_status"]="failed"; result["error"]=str(e)[:300]; return result

    for e in root.iter():
        tag=local(e.tag)
        ltag=tag.lower()
        attrs={k:v for k,v in e.attrib.items() if not SENSITIVE.search(k)}
        text=(e.text or "").strip()
        if SENSITIVE.search(ltag):
            text="[REDACTED]"
        ent={"tag":tag,"attrs":attrs}
        if text and len(text)<500:
            ent["text"]=text
        result["entities"].append(ent)

        vals=list(attrs.values())
        joined=" ".join(vals+[text])
        # Heuristic extraction; EMAP variants differ.
        if any(k in ltag for k in ["action","service"]):
            name=attrs.get("name") or attrs.get("id") or text
            if name: result["actions"].append(name)
        if any(k in ltag for k in ["page","view","menu"]):
            name=attrs.get("name") or attrs.get("id") or text
            if name: result["pages"].append(name)
        if "table" in ltag:
            name=attrs.get("name") or attrs.get("table") or text
            if name: result["tables"].append(name)
        if any(k in ltag for k in ["field","column","property"]):
            name=attrs.get("name") or attrs.get("column") or attrs.get("field") or text
            if name: result["fields"].append(name)
        if "permission" in ltag or "auth" in ltag:
            name=attrs.get("name") or attrs.get("id") or text
            if name: result["permissions"].append(name)
        if result["file_type"]=="version" and any(k in joined.lower() for k in ["alter table","create table","add column","drop column","index"]):
            result["db_changes"].append(joined[:1000])

        # Common table names and references from text/attrs
        for m in re.findall(r"\bT_[A-Z0-9_$]+\b", joined):
            result["tables"].append(m)
        for m in re.findall(r"[\w$.-]+\.(?:eda|epg|epm|epmx|edm|edmx|dic)\b", joined, flags=re.I):
            result["references"].append(m)

    for k in ["references","tables","fields","actions","pages","permissions","db_changes"]:
        result[k]=sorted(set(x for x in result[k] if x))
    if len(result["entities"])>2000:
        result["entities"]=result["entities"][:2000]
        result["parse_status"]="partial"
    return result

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--output", required=True)
    args=ap.parse_args()
    inp=Path(args.input)
    files=[inp] if inp.is_file() else [p for p in inp.rglob("*") if p.is_file() and p.suffix.lower() in {".eda",".epg",".epm",".epmx",".edm",".edmx",".dic",".xml"}]
    rows=[parse_file(p) for p in files if "ROOT" not in p.parts and ".svn" not in p.parts]
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    Path(args.output).write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding="utf-8")
    print(args.output)

if __name__=="__main__":
    main()
