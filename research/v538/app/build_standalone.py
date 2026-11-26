#!/usr/bin/env python3
"""Assemble the review-only static application using the V5.37 validated builder."""
import argparse
import hashlib
from pathlib import Path
import subprocess
import sys
import tempfile
import zipfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    out = args.output.resolve()
    if out.suffix.lower() != ".zip" or out.exists():
        raise SystemExit("Provide a new ZIP path")
    out.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=out.parent) as tmp:
        tmp = Path(tmp)
        old = tmp / "base.zip"
        staged = tmp / "standalone.zip"
        subprocess.run([sys.executable, str(ROOT / "research/v537/preview/build_preview_package.py"), "--repo-root", str(ROOT), "--output", str(old)], check=True)
        files = ["index.html", "style.css", "core.js", "app.js", "core_qa.json"]
        with zipfile.ZipFile(old) as src, zipfile.ZipFile(staged, "w", compression=zipfile.ZIP_DEFLATED) as dest:
            for name in src.namelist():
                dest.writestr(name, src.read(name))
            for name in files:
                if name in src.namelist():
                    raise ValueError("Duplicate path: " + name)
                dest.writestr(name, (HERE / name).read_bytes())
            dest.writestr("STANDALONE_README.md", (HERE / "README.md").read_bytes())
        with zipfile.ZipFile(staged) as check:
            if check.testzip() is not None or len(check.namelist()) != 36:
                raise ValueError("ZIP verification failed")
        with out.open("xb") as f:
            f.write(staged.read_bytes())
    print("RESEARCH PREVIEW ONLY:", out)
    print("SHA256:", hashlib.sha256(out.read_bytes()).hexdigest())
if __name__ == "__main__":
    main()
