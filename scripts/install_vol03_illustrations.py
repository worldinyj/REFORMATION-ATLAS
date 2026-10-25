#!/usr/bin/env python3
"""Verify and optionally install the six staged VOL-03 AI illustrations.

Default mode is read-only. --install writes WebP files and updates the asset registry.
The ZIP is supplied by a human locally; the script NEVER fetches from the network.
"""
import argparse
import hashlib
import json
from pathlib import Path
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[1]
STAGE = ROOT / "assets/illustrations/vol03/ILLUSTRATION_STAGE.json"
MANIFEST = ROOT / "assets/asset_manifest.json"
ARCHIVE_PREFIX = "VOL03_ILLUSTRATIONS_V01/"


def sha256_bytes(data):
    return hashlib.sha256(data).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archive", type=Path, help="Downloaded REFORMATION_ATLAS_VOL03_ILLUSTRATIONS_V01.zip")
    parser.add_argument("--install", action="store_true", help="Copy checked WebP assets into the repository")
    parser.add_argument("--include-png", action="store_true", help="Also copy original cropped PNGs")
    args = parser.parse_args()

    stage = json.loads(STAGE.read_text(encoding="utf-8"))
    archive = args.archive.expanduser().resolve()
    if not archive.is_file():
        parser.error(f"Archive does not exist: {archive}")
    actual_zip_sha = hashlib.sha256(archive.read_bytes()).hexdigest()
    expected_zip_sha = stage["zip_sha256"]
    if actual_zip_sha != expected_zip_sha:
        raise SystemExit("FAIL: ZIP SHA256 mismatch; wrong or modified source archive")

    pending = []
    with zipfile.ZipFile(archive, "r") as z:
        if z.testzip():
            raise SystemExit("FAIL: ZIP internal CRC verification failed")
        for item in stage["assets"]:
            if item["status"] not in ("PENDING_BINARY_COMMIT", "IN_WORKTREE_PENDING_GIT_COMMIT"):
                raise SystemExit(f"FAIL: unexpected source status for {item['id']}")
            webp = item["file"]
            src = ARCHIVE_PREFIX + webp
            if src not in z.namelist():
                raise SystemExit(f"FAIL: missing entry {src}")
            content = z.read(src)
            if sha256_bytes(content) != item["webp_sha256"]:
                raise SystemExit(f"FAIL: checksum mismatch in {webp}")
            dst = ROOT / item["relative_path"]
            if not dst.resolve().is_relative_to(ROOT.resolve()):
                raise SystemExit(f"FAIL: unsafe output path {dst}")
            if dst.exists() and sha256_bytes(dst.read_bytes()) != item["webp_sha256"]:
                raise SystemExit(f"FAIL: existing different local image {dst}; refusing overwrite")
            pending.append((dst, content))
            if args.include_png:
                png = webp.replace(".webp", ".png")
                png_src = ARCHIVE_PREFIX + png
                if png_src not in z.namelist():
                    raise SystemExit(f"FAIL: missing {png_src}")
                png_content = z.read(png_src)
                pending.append((dst.with_suffix(".png"), png_content))

    print(f"PASS: verified ZIP checksum and {len(stage['assets'])} WebP assets")
    if not args.install:
        print("READ-ONLY check. Re-run with --install to copy files.")
        return 0

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    ids = {item["asset_id"] for item in manifest}
    for dst, data in pending:
        dst.parent.mkdir(parents=True, exist_ok=True)
        if not dst.exists():
            dst.write_bytes(data)
            print(f"INSTALLED {dst.relative_to(ROOT)}")
        elif sha256_bytes(dst.read_bytes()) != sha256_bytes(data):
            raise SystemExit(f"FAIL: a local file changed while verifying {dst}")
    for item in stage["assets"]:
        if item["id"] not in ids:
            manifest.append({
                "asset_id": item["id"],
                "type": item["type"],
                "title_ko": item["description_ko"],
                "relative_path": item["relative_path"],
                "linked_entity_ids": item["linked_entity_ids"],
                "creator_method": "ai_generated_original_cropped_from_contact_sheet",
                "tool": "OpenAI ImageGen",
                "created_date": stage["created_at"],
                "rights_status": "ai_generated_original_draft",
                "ai_disclosure": stage["ai_disclosure"],
                "historical_accuracy_note": item["historical_limitation_ko"],
                "source_ids": item["source_ids"],
                "review_status": "DRAFT",
                "historical_likeness_verified": False,
                "source_sha256": item["webp_sha256"],
            })
    MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    stage["state"] = "BINARY_INSTALLED_LOCALLY_AWAITING_GIT_COMMIT"
    for item in stage["assets"]:
        item["status"] = "IN_WORKTREE_PENDING_GIT_COMMIT"
    STAGE.write_text(json.dumps(stage, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("PASS: installed WebP files, updated asset_manifest.json and staging state")
    print("NEXT: run python scripts/validate_vol03.py and review git diff before committing")
    print("The images remain DRAFT even after Git commit; human historical/visual review is still required.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
