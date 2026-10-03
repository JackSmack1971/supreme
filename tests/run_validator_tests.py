import json, subprocess, sys, tempfile
from pathlib import Path

VALIDATOR = Path(__file__).resolve().parents[1] / "scripts" / "validate_repo.py"
TODAY = "2026-10-02"
FM = '''---\ntitle: T\nsummary: Test fixture\nas_of: 2026-10-02\nlast_verified: 2026-10-02\nreverify_by: 2026-11-01\nstatus: verified\nconfidence: high\nvolatility: volatile\nsources:\n- id: S1\n  url: https://example.test\n  accessed: 2026-10-02\n  locator: section\ntags: []\naliases: []\nrelated: []\n---\n## Answer\nClaim [VERIFIED 2026-10-02 S1]\n## Conditions\nScope [VERIFIED 2026-10-02 S1]\n## Detail\n## Dead Ends\n## Open Questions\n'''
PARTIAL = '''---\ntitle: T\nsummary: Imported legacy text\nas_of: 2026-10-02\nlast_verified: none\nreverify_by: 2026-11-01\nstatus: partial\nconfidence: low\nvolatility: volatile\nsources:\n- id: S0\n  url: legacy/source.md\n  accessed: 2026-10-02\n  locator: imported text\ntag_default: UNVERIFIED\norigin: legacy/source.md#Heading\ntags: []\naliases: []\nrelated: []\n---\n## Answer\nImported text\n## Conditions\nImported scope\n## Detail\n'''

def run(root, *args):
    return subprocess.run([sys.executable, str(VALIDATOR), str(root), "--today", TODAY, "--json", *args], text=True, capture_output=True)

def setup(root, knowledge=True):
    for name in ("INDEX.md", "CHANGELOG.md", "BACKLOG.md", "TOOLS.md"):
        (root/name).write_text("", encoding="utf-8")
    if knowledge:
        (root/"knowledge").mkdir(); (root/"knowledge"/"good.md").write_text(FM, encoding="utf-8")
    (root/"CONFIG.md").write_text("knowledge_root: knowledge/\nlegacy_root: legacy/\n", encoding="utf-8")

def main():
    with tempfile.TemporaryDirectory() as td:
        base=Path(td)
        clean=base/"clean"; clean.mkdir(); setup(clean); subprocess.run([sys.executable,str(VALIDATOR),str(clean),"--write-index"],check=True); assert run(clean).returncode==0
        # Explicit line tags override a file-level UNVERIFIED default.
        override=base/"override"; override.mkdir(); setup(override); (override/"knowledge"/"good.md").write_text(PARTIAL.replace("- id: S0\n  url: legacy/source.md\n  accessed: 2026-10-02\n  locator: imported text","- id: S1\n  url: https://example.test\n  accessed: 2026-10-02\n  locator: section").replace("Imported text","Supported statement [VERIFIED 2026-10-02 S1]").replace("## Detail\n","## Detail\nThis is a sufficiently long factual line without a specific tag.\n"),encoding="utf-8"); subprocess.run([sys.executable,str(VALIDATOR),str(override),"--write-index"],check=True,capture_output=True); r=run(override); om=json.loads(r.stdout)["metrics"]["per_file"]["knowledge/good.md"]; assert r.returncode==0 and om["lines_verified"]==1 and om["lines_unverified"]==1
        corrected=base/"corrected"; corrected.mkdir(); setup(corrected); (corrected/"knowledge"/"good.md").write_text(FM.replace("Claim [VERIFIED 2026-10-02 S1]","**Corrected:** This is a sufficiently long corrected factual claim [VERIFIED 2026-10-02 S1]"),encoding="utf-8"); subprocess.run([sys.executable,str(VALIDATOR),str(corrected),"--write-index"],capture_output=True); r=run(corrected); cm=json.loads(r.stdout)["metrics"]["per_file"]["knowledge/good.md"]; assert r.returncode==0 and cm["lines_verified"]==1 and cm["lines_refuted_corrected"]==1
        # tag_default cannot coexist with verified status or medium/high confidence.
        for field,value in (("status","verified"),("confidence","medium"),("confidence","high")):
            invalid=base/f"invalid-{field}-{value}"; invalid.mkdir(); setup(invalid); (invalid/"knowledge"/"good.md").write_text(PARTIAL.replace("status: partial",f"status: {value}") if field=="status" else PARTIAL.replace("confidence: low",f"confidence: {value}"),encoding="utf-8"); subprocess.run([sys.executable,str(VALIDATOR),str(invalid),"--write-index"],capture_output=True); r=run(invalid); assert r.returncode==1 and "UNVERIFIED_STATE" in {e["code"] for e in json.loads(r.stdout)["errors"]}
        # Removing tag_default turns factual lines without tags into errors.
        promoted=base/"promoted"; promoted.mkdir(); setup(promoted); (promoted/"knowledge"/"good.md").write_text(FM.replace("Claim [VERIFIED 2026-10-02 S1]","This is a sufficiently long factual claim [VERIFIED 2026-10-02 S1]"),encoding="utf-8"); subprocess.run([sys.executable,str(VALIDATOR),str(promoted),"--write-index"],capture_output=True); r=run(promoted); assert r.returncode==0
        (promoted/"knowledge"/"good.md").write_text(FM.replace("Claim [VERIFIED 2026-10-02 S1]","This is a sufficiently long factual claim without a tag"),encoding="utf-8"); r=run(promoted); assert r.returncode==1 and "UNTAGGED_FACT" in {e["code"] for e in json.loads(r.stdout)["errors"]}
        # H1: any untagged body line with at least five words fails, regardless of its first character.
        conservative=base/"conservative"; conservative.mkdir(); setup(conservative); subprocess.run([sys.executable,str(VALIDATOR),str(conservative),"--write-index"],capture_output=True)
        (conservative/"knowledge"/"good.md").write_text(FM.replace("Claim [VERIFIED 2026-10-02 S1]","short note\nthis lowercase line has five words"),encoding="utf-8")
        r=run(conservative); assert r.returncode==1 and "UNTAGGED_FACT" in {e["code"] for e in json.loads(r.stdout)["errors"]}
        (conservative/"knowledge"/"good.md").write_text(FM.replace("Claim [VERIFIED 2026-10-02 S1]","short note\n```text\nthis lowercase line has five words\n```\n| a | b |\n|---|---|\n## A heading with several words"),encoding="utf-8")
        r=run(conservative); assert r.returncode==0, json.loads(r.stdout)["errors"]
        # Per-file line metrics are always emitted.
        assert set(json.loads(run(clean).stdout)["metrics"]["per_file"]["knowledge/good.md"])=={"lines_verified","lines_unverified","lines_refuted_corrected"}
        broken=base/"broken"; broken.mkdir(); setup(broken); (broken/"knowledge"/"bad.md").write_text("no frontmatter",encoding="utf-8"); subprocess.run([sys.executable,str(VALIDATOR),str(broken),"--write-index"],capture_output=True); r=run(broken); assert r.returncode==1 and "FRONTMATTER" in {e["code"] for e in json.loads(r.stdout)["errors"]}
        legacy=base/"legacyonly"; legacy.mkdir(); setup(legacy,False); (legacy/"legacy").mkdir(); (legacy/"legacy"/"source.md").write_text("# Answer\n\nImported text\n## Conditions\nImported scope\n## Detail\n",encoding="utf-8"); subprocess.run([sys.executable,str(VALIDATOR),str(legacy),"--write-index"],check=True); r=run(legacy); assert r.returncode==0 and json.loads(r.stdout)["metrics"]["legacy_files"]==1
        (legacy/"knowledge").mkdir(); (legacy/"knowledge"/"import.md").write_text(PARTIAL,encoding="utf-8"); assert run(legacy,"--check-migration","legacy/source.md").returncode==0
        (legacy/"knowledge"/"import.md").write_text(PARTIAL.replace("Imported text","missing text"),encoding="utf-8"); assert run(legacy,"--check-migration","legacy/source.md").returncode==1
        ignored=base/"ignored"; ignored.mkdir(); setup(ignored); subprocess.run([sys.executable,str(VALIDATOR),str(ignored),"--write-index"],check=True); (ignored/"README.md").write_text("not knowledge",encoding="utf-8"); assert run(ignored).returncode==0
    print("PASS: clean, broken, legacy-only, migration pass/fail, ignored-file")

if __name__=="__main__":main()
