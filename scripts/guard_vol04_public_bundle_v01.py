#!/usr/bin/env python3
"""VOL-04 public web bundle leak guard.

Standalone safety net for a *built static* site. This does NOT grant release
permission and cannot detect visual rights violations or unmarked paraphrases.
Run --self-test in repository CI; later pass --bundle path/to/dist in web CI.
"""
from __future__ import annotations
import argparse
from pathlib import Path
import tempfile

SCAN_EXTENSIONS = {".html", ".js", ".mjs", ".cjs", ".jsx", ".ts", ".tsx",
                   ".json", ".css", ".map", ".txt", ".md"}
FORBIDDEN = (
    b"VOL04-CMP-", b"CMP-SRC-PROP-", b"WORK-PROP-V04-",
    b"DOC-PROP-V04-", b"EDN-PROP-V04-",
    b"RESEARCH_PROVENANCE_GRAPH_ONLY", b"RESEARCH_REVIEW_ONLY",
    b"source_links_review_only", b"proposal_key_review_only",
    b"vol04_comparison_provenance_crosswalk_v01.json",
    b"vol04_edition_comparison_v01.json",
)
MAX_FILE_BYTES = 20 * 1024 * 1024

def inspect_bundle(path: Path) -> list[str]:
    """Return violations; a non-existent, empty, or symlinked bundle is unsafe."""
    root = Path(path).expanduser().absolute()
    errors: list[str] = []
    if not root.exists() or not root.is_dir() or root.is_symlink():
        return ["bundle root missing/not directory/symlinked"]
    found = 0
    for file in root.rglob("*"):
        if file.is_symlink():
            errors.append(f"symbolic link disallowed: {file.relative_to(root)}")
            continue
        if not file.is_file():
            continue
        found += 1
        if file.suffix.lower() not in SCAN_EXTENSIONS:
            continue
        rel = file.relative_to(root)
        try:
            if file.stat().st_size > MAX_FILE_BYTES:
                errors.append(f"too large to inspect safely: {rel}")
                continue
            content = file.read_bytes()
        except OSError as err:
            errors.append(f"unable to inspect {rel}: {err}")
            continue
        for needle in FORBIDDEN:
            if needle in content:
                errors.append(f"research token found in {rel}: {needle.decode('ascii')}")
        if "data/deep/vol04_" in str(rel).replace("\\", "/"):
            errors.append(f"research-only path in public bundle: {rel}")
    if found == 0:
        errors.append("bundle contains no files; cannot assert a valid web build")
    return errors

def self_test() -> None:
    with tempfile.TemporaryDirectory() as temporary:
        root = Path(temporary)
        (root / "index.html").write_text("<h1>승인된 판본 비교 자료가 없습니다.</h1>", encoding="utf-8")
        assert inspect_bundle(root) == []
        (root / "app.js").write_text("const id='VOL04-CMP-002';", encoding="utf-8")
        assert any("VOL04-CMP-" in msg for msg in inspect_bundle(root))
        (root / "app.js").unlink()
        (root / "research.json").write_text('{"kind":"RESEARCH_PROVENANCE_GRAPH_ONLY"}')
        assert inspect_bundle(root)
        (root / "research.json").unlink()
        assert inspect_bundle(root / "missing")
        (root / "deep-link").symlink_to(root / "index.html")
        assert any("symbolic link" in msg for msg in inspect_bundle(root))
    print("PASS: public bundle scanner clean, leak, missing bundle and symlink cases")

def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--self-test", action="store_true")
    g.add_argument("--bundle", type=Path, help="Built, static public site directory")
    args = p.parse_args()
    if args.self_test:
        self_test()
        return 0
    errors = inspect_bundle(args.bundle)
    for error in errors:
        print("FAIL:", error)
    if errors:
        return 1
    print("PASS: scanned web bundle has no detected VOL-04 research markers")
    print("NOTICE: not evidence of publication, scholarly, or media rights approval")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
