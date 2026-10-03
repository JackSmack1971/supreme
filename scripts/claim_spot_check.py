#!/usr/bin/env python3
"""Prepare a reproducible sample of VERIFIED claims for source re-fetch review."""
import argparse
import datetime as dt
import json
import random
import re
from pathlib import Path

import yaml

TAG = re.compile(r"\[VERIFIED\s+(\d{4}-\d{2}-\d{2})\s+([S\d, ]+)\]")
CODE = re.compile(r"```.*?```", re.S)
REGISTERS = {"INDEX.md", "CHANGELOG.md", "BACKLOG.md", "TOOLS.md", "CONFIG.md"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("root", nargs="?", default=".")
    ap.add_argument("--sample-size", type=int, default=5)
    ap.add_argument("--seed", default=dt.date.today().isoformat())
    args = ap.parse_args()
    if args.sample_size < 1:
        ap.error("--sample-size must be at least 1")
    root = Path(args.root)
    claims = []
    for path in sorted(root.rglob("*.md")):
        relpath = path.relative_to(root)
        if path.name in REGISTERS or "reports" in relpath.parts or ".git" in relpath.parts:
            continue
        text = path.read_text(encoding="utf-8")
        chunks = text.split("\n---", 1)
        if len(chunks) < 2 or not chunks[0].startswith("---"):
            continue
        try:
            fm = yaml.safe_load(chunks[0][3:])
        except yaml.YAMLError:
            continue
        if not isinstance(fm, dict):
            continue
        body = CODE.sub("", chunks[1])
        sources = {str(src.get("id")): src for src in (fm.get("sources") or []) if isinstance(src, dict)}
        for line_no, line in enumerate(body.splitlines(), 1):
            mt = TAG.search(line)
            if not mt:
                continue
            source_ids = [sid.strip() for sid in mt.group(2).split(",")]
            claims.append({
                "file": str(relpath),
                "line": line_no,
                "claim": line[:line.rfind("[VERIFIED")].strip(),
                "verified_date": mt.group(1),
                "sources": [sources[sid] for sid in source_ids if sid in sources],
            })
    sample = random.Random(str(args.seed)).sample(claims, min(args.sample_size, len(claims)))
    print(json.dumps({
        "requested": args.sample_size,
        "available": len(claims),
        "selected": len(sample),
        "seed": str(args.seed),
        "claims": sample,
        "instruction": "Re-fetch each cited source, inspect its locator, and report supported, contradicted, or unresolved with evidence.",
    }, indent=2, default=str))


if __name__ == "__main__":
    main()
