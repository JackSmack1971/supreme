#!/usr/bin/env python3
"""Validate Caretaker knowledge scope and migration integrity."""
import argparse, datetime as dt, json, re, sys
from collections import Counter
from pathlib import Path
import yaml

REGISTERS = {"INDEX.md", "CHANGELOG.md", "BACKLOG.md", "TOOLS.md", "CONFIG.md"}
REQUIRED = ["title", "summary", "as_of", "last_verified", "reverify_by", "status", "confidence", "volatility", "sources", "tags", "aliases", "related"]
STATUS = {"verified", "partial", "stale", "deprecated"}
CONFIDENCE = {"high", "medium", "low"}
VOLATILITY = {"volatile": 30, "semi-stable": 90, "stable": 365}
HEADINGS = ["Answer", "Conditions", "Detail", "Dead Ends", "Open Questions"]
TAG_RE = re.compile(r"\[(VERIFIED|REPORTED|ESTIMATED|UNVERIFIED|UNKNOWN|DEPRECATED)\b([^\]]*)\]")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
ABS_DATE = re.compile(r"\d{4}-\d{2}-\d{2}")
REL_RE = re.compile(r"\b(recent(ly)?|latest|currently|now|today|newest)\b", re.I)
SECRET_RE = re.compile(r"(AKIA[0-9A-Z]{16}|-----BEGIN [A-Z ]*PRIVATE KEY-----|(api[_-]?key|secret|token|password)\s*[:=]\s*['\"]?[A-Za-z0-9_\-]{16,})", re.I)
SOFT_TOKENS, HARD_TOKENS = 1500, 4000

def parse_date(s):
    if isinstance(s, dt.date): return s
    if isinstance(s, str) and DATE_RE.match(s):
        try: return dt.date.fromisoformat(s)
        except ValueError: pass
    return None

def split_front(text):
    if not text.startswith("---"): return None, text
    parts = text.split("\n---", 1)
    if len(parts) < 2: return None, text
    try: fm = yaml.safe_load(parts[0][3:])
    except yaml.YAMLError: return "YAMLERR", text
    return fm, parts[1].lstrip("\n")

def config(root):
    cfg = {}
    p = root / "CONFIG.md"
    if p.exists():
        for line in p.read_text(encoding="utf-8").splitlines():
            if ":" in line and not line.lstrip().startswith("#"):
                k,v=line.split(":",1); cfg[k.strip()]=v.strip()
    return cfg

def paths(root, cfg):
    kr=Path(cfg.get("knowledge_root","knowledge/")); lr=Path(cfg.get("legacy_root","legacy/"))
    ignored=[x.strip().rstrip("/") for x in cfg.get("ignore","README.md, AGENTS.md, CLAUDE.md, caretaker_audit_and_delta.md, reports/, scripts/, tests/").split(",")]
    allmd=sorted(root.rglob("*.md"))
    def ignored_path(rel):
        return any(rel==i or rel.startswith(i+"/") for i in ignored) or ".git" in Path(rel).parts or rel in REGISTERS
    knowledge=[p for p in allmd if Path(p.relative_to(root)).is_relative_to(kr)]
    legacy=[p for p in allmd if Path(p.relative_to(root)).is_relative_to(lr)]
    other=[p for p in allmd if p not in knowledge and p not in legacy and not ignored_path(p.relative_to(root).as_posix())]
    return knowledge,legacy,other

def index_rows(root):
    idx=root/"INDEX.md"
    if not idx.exists(): return {}
    result={}
    for line in idx.read_text(encoding="utf-8").splitlines():
        if line.startswith("|"):
            cells=[c.strip().replace("\\|","|") for c in line.strip("|").split("|")]
            if len(cells)>=6 and cells[0].endswith(".md"): result[cells[0]]=cells
    return result

def write_index(root):
    cfg=config(root); knowledge,legacy,_=paths(root,cfg); old=index_rows(root); rows=["# Knowledge Index","","| path | summary | tags | status | last_verified | reverify_by |","|---|---|---|---|---|---|"]
    for p in sorted(knowledge+legacy):
        rel=p.relative_to(root).as_posix(); fm,_=split_front(p.read_text(encoding="utf-8")); fm=fm if isinstance(fm,dict) else {}
        status=(old.get(rel,[None,None,None,None])[3] if p in legacy and old.get(rel,[None]*4)[3] in ("migrated","unmigrated") else ("unmigrated" if p in legacy else str(fm.get("status",""))))
        vals=[rel,str(fm.get("summary",old.get(rel,[None,""])[1])),",".join(map(str,fm.get("tags") or [])),status,str(fm.get("last_verified","")),str(fm.get("reverify_by",""))]
        rows.append("| "+" | ".join(v.replace("|","\\|").replace("\n"," ") for v in vals)+" |")
    (root/"INDEX.md").write_text("\n".join(rows)+"\n",encoding="utf-8")

def normalize_source(line):
    s=re.sub(r"^\s*#+\s*", "", line.strip())
    return s

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("root"); ap.add_argument("--today",default=dt.date.today().isoformat()); ap.add_argument("--json",action="store_true"); ap.add_argument("--write-index",action="store_true"); ap.add_argument("--check-migration")
    a=ap.parse_args(); root=Path(a.root); today=parse_date(a.today)
    if a.write_index: write_index(root)
    cfg=config(root); knowledge,legacy,other=paths(root,cfg); errors=[]; warnings=[]
    E=lambda f,c,m:errors.append({"file":f,"code":c,"msg":m}); W=lambda f,c,m:warnings.append({"file":f,"code":c,"msg":m})
    if a.check_migration:
        src=(root/a.check_migration).resolve()
        if not src.is_file() or not src.is_relative_to((root/Path(cfg.get("legacy_root","legacy/"))).resolve()): E(a.check_migration,"MIGRATION_SOURCE","source must exist under legacy_root")
        else:
            lines={normalize_source(x) for x in src.read_text(encoding="utf-8").splitlines() if normalize_source(x)}
            covered=set()
            for p in knowledge:
                fm,body=split_front(p.read_text(encoding="utf-8"))
                if isinstance(fm,dict) and str(fm.get("origin","")).split("#",1)[0].replace("\\","/")==Path(a.check_migration).as_posix():
                    covered.update(normalize_source(x) for x in body.splitlines() if normalize_source(x))
            missing=sorted(lines-covered)
            for line in missing: E(a.check_migration,"MIGRATION_UNCOVERED",line)
        out={"today":str(today),"errors":errors,"warnings":warnings,"metrics":{"error_count":len(errors)}}
        print(json.dumps(out,indent=2) if a.json else ("\n".join("ERROR "+x["msg"] for x in errors) or "RESULT PASS")); sys.exit(1 if errors else 0)
    for reg in ("INDEX.md","CHANGELOG.md","BACKLOG.md","TOOLS.md"):
        if not (root/reg).exists(): E(reg,"REGISTER_MISSING","register absent")
    indexed=index_rows(root); legacy_files=sum(1 for p in legacy if indexed.get(p.relative_to(root).as_posix(),[None]*4)[3]=="unmigrated")
    metrics=dict(files=len(knowledge),legacy_files=legacy_files,legacy_tokens=sum(len(p.read_text(encoding="utf-8"))//4 for p in legacy),unverified_files=0,overdue=0,claims=0,verified_claims=0,tokens=0,fm_complete=0,untagged_lines=0)
    for p in other: W(p.relative_to(root).as_posix(),"UNSCOPED","Markdown file is outside knowledge and legacy roots")
    for p in [x for x in root.rglob("reports/*.md") if re.fullmatch(r"\d{4}-\d{2}-\d{2}",x.stem)]:
        if not p.with_suffix(".metrics.json").exists(): E(p.relative_to(root).as_posix(),"REPORT_METRICS_MISSING","dated report lacks sibling metrics JSON")
    for p in knowledge:
        rel=p.relative_to(root).as_posix(); text=p.read_text(encoding="utf-8"); tok=len(text)//4; metrics["tokens"]+=tok
        if SECRET_RE.search(text): E(rel,"SECRET","possible credential or key")
        if tok>HARD_TOKENS:E(rel,"SIZE_HARD",f"~{tok} tokens > {HARD_TOKENS}; split")
        elif tok>SOFT_TOKENS:W(rel,"SIZE_SOFT",f"~{tok} tokens > {SOFT_TOKENS}")
        fm,body=split_front(text)
        if fm is None or fm=="YAMLERR" or not isinstance(fm,dict): E(rel,"FRONTMATTER","missing or unparsable frontmatter"); continue
        unv=fm.get("tag_default")=="UNVERIFIED"
        if unv and (fm.get("status")!="partial" or fm.get("confidence")!="low"):E(rel,"UNVERIFIED_STATE","tag_default requires partial status and low confidence")
        if unv: metrics["unverified_files"]+=1
        missing=[k for k in REQUIRED if not (unv and k=="last_verified" and fm.get(k)=="none") and (k not in fm or fm[k] in (None,"") and k not in ("aliases","related"))]
        if missing:E(rel,"FM_FIELDS",f"missing: {missing}")
        else:metrics["fm_complete"]+=1
        if len(str(fm.get("summary","")).split())>25:W(rel,"SUMMARY_LEN","summary > 25 words")
        file_line_metrics={"lines_verified":0,"lines_unverified":0,"lines_refuted_corrected":0}
        for k in ("as_of","last_verified","reverify_by"):
            if unv and k=="last_verified" and fm.get(k)=="none": continue
            if k in fm and parse_date(fm[k]) is None:E(rel,"DATE_FORMAT",f"{k} not YYYY-MM-DD")
        if fm.get("status") not in STATUS:E(rel,"STATUS",f"status must be one of {sorted(STATUS)}")
        if fm.get("confidence") not in CONFIDENCE:E(rel,"CONFIDENCE",f"must be one of {sorted(CONFIDENCE)}")
        if fm.get("volatility") not in VOLATILITY:E(rel,"VOLATILITY",f"must be one of {sorted(VOLATILITY)}")
        ids=set(); srcs=fm.get("sources") or []
        if not isinstance(srcs,list):E(rel,"SOURCES","sources must be a list");srcs=[]
        for s in srcs:
            if not isinstance(s,dict) or not all(k in s for k in ("id","url","accessed","locator")):E(rel,"SOURCE_FIELDS",f"source needs id,url,accessed,locator: {s}");continue
            if s["id"] in ids:E(rel,"SOURCE_DUP",f"duplicate id {s['id']}")
            ids.add(s["id"]); url=str(s["url"])
            if s["id"]=="S0" and fm.get("origin") and not url.startswith(("http://","https://")):
                target=(root/url).resolve()
                if not target.is_file() or not target.is_relative_to((root/Path(cfg.get("legacy_root","legacy/"))).resolve()):E(rel,"SOURCE_URL","S0 path must name existing file under legacy_root")
            elif not url.startswith(("http://","https://")):E(rel,"SOURCE_URL",f"{s['id']} url not http(s)")
            if parse_date(s["accessed"]) is None:E(rel,"SOURCE_DATE",f"{s['id']} accessed not YYYY-MM-DD")
        if fm.get("status")=="verified" and not ids:E(rel,"VERIFIED_NO_SOURCE","status verified with no sources")
        heads=[h.strip() for h in re.findall(r"^##\s+(.+)$",body,re.M)]
        for need in ("Answer","Conditions"):
            if need not in heads:E(rel,"HEADING_MISSING",f"## {need} required")
        known=[h for h in heads if h in HEADINGS]
        if known!=sorted(known,key=HEADINGS.index):E(rel,"HEADING_ORDER",f"headings out of order: {known}")
        in_fence=False
        for ln in body.splitlines():
            if re.match(r"^\s*(```|~~~)",ln):
                in_fence=not in_fence
                continue
            if in_fence: continue
            tagged=bool(TAG_RE.search(ln))
            stripped=ln.strip()
            # Headings and Markdown table separators are excluded from the rule.
            factual=bool(len(ln.split())>=5 and not stripped.startswith(("#","|","<")) and not re.fullmatch(r"\|?\s*:?-{3,}:?\s*(?:\|\s*:?-{3,}:?\s*)*\|?", stripped))
            if factual:
                if tagged:
                    if re.search(r"\[VERIFIED\b",ln): file_line_metrics["lines_verified"]+=1
                    elif re.search(r"\[UNVERIFIED\b",ln): file_line_metrics["lines_unverified"]+=1
                    elif re.search(r"\[(?:REPORTED|ESTIMATED|UNKNOWN|DEPRECATED)\b",ln): pass
                    # Correction is a prose marker, separate from the line's single claim tag.
                    if ln.lstrip().startswith(("Corrected:", "**Corrected:**")): file_line_metrics["lines_refuted_corrected"]+=1
                elif unv:
                    file_line_metrics["lines_unverified"]+=1
                else:
                    E(rel,"UNTAGGED_FACT","factual line lacks a claim tag")
            if TAG_RE.search(ln):
                for mt in TAG_RE.finditer(ln):
                    metrics["claims"]+=1;kind,rest=mt.groups();refs=set(re.findall(r"\bS\d+\b",rest))
                    if kind=="VERIFIED":metrics["verified_claims"]+=1
                    if kind in ("VERIFIED","REPORTED") and not refs:E(rel,"TAG_SOURCE",f"{kind} needs source id")
                    if kind=="VERIFIED" and not ABS_DATE.search(rest):E(rel,"TAG_DATE","VERIFIED needs date")
                    if refs-ids:E(rel,"TAG_REF",f"unknown source id {sorted(refs-ids)}")
        metrics.setdefault("per_file",{})[rel]=file_line_metrics
    for rel in sorted({p.relative_to(root).as_posix() for p in knowledge+legacy}-set(indexed)):E("INDEX.md","INDEX_MISSING",f"not indexed: {rel}")
    for rel in sorted(set(indexed)-{p.relative_to(root).as_posix() for p in knowledge+legacy}):E("INDEX.md","INDEX_ORPHAN",f"indexed but absent: {rel}")
    for p in legacy:
        rel=p.relative_to(root).as_posix(); row=indexed.get(rel)
        if row and row[3] not in ("unmigrated","migrated"):E("INDEX.md","INDEX_STATUS",f"legacy status must be unmigrated or migrated: {rel}")
    if metrics["untagged_lines"]:W("*","UNTAGGED",f"{metrics['untagged_lines']} body lines look factual but carry no claim tag")
    metrics.update(frontmatter_complete_pct=round(100*metrics["fm_complete"]/metrics["files"],1) if metrics["files"] else None,overdue_files=metrics.pop("overdue"),claim_tags=metrics.pop("claims"),verified_claim_tags=metrics.pop("verified_claims"),avg_tokens=round(metrics["tokens"]/metrics["files"]) if metrics["files"] else None,error_count=len(errors),warning_count=len(warnings),errors_by_code=dict(Counter(e["code"] for e in errors)))
    metrics["legacy_remaining"] = metrics["legacy_files"]
    out={"today":str(today),"errors":errors,"warnings":warnings,"metrics":metrics}
    print(json.dumps(out,indent=2) if a.json else "\n".join([*(f"ERROR {e['file']}: {e['code']} {e['msg']}" for e in errors),*(f"WARN {w['file']}: {w['code']} {w['msg']}" for w in warnings),"METRICS "+json.dumps(metrics),"RESULT "+("FAIL" if errors else "PASS")]))
    sys.exit(1 if errors else 0)

if __name__=="__main__":main()
