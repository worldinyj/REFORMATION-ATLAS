#!/usr/bin/env python3
"""Verify a local portrait package and copy only the two approved-path pilot files.
No commit, push, or deployment. Standard library only."""
import hashlib, json, subprocess, sys, zipfile
from pathlib import Path

def digest(data):
    return hashlib.sha256(data).hexdigest()

def main():
    if len(sys.argv) != 2:
        raise SystemExit("usage: python3 import_portraits.py /path/to/ATLAS_V535_portrait_pilots.zip")
    here = Path(__file__).resolve().parent
    m = json.loads((here / "portrait_manifest.json").read_text(encoding="utf-8"))
    root = Path(subprocess.check_output(["git", "rev-parse", "--show-toplevel"], cwd=here, text=True).strip())
    branch = subprocess.check_output(["git", "branch", "--show-current"], cwd=root, text=True).strip()
    if branch != m["branch"]:
        raise SystemExit("Wrong branch: " + branch)
    raw = Path(sys.argv[1]).read_bytes()
    if digest(raw) != m["package"]["sha256"]:
        raise SystemExit("ZIP SHA256 mismatch")
    pending = []
    with zipfile.ZipFile(sys.argv[1]) as z:
        for a in m["assets"]:
            data = z.read(a["filename"])
            if len(data) != a["bytes"] or digest(data) != a["sha256"]:
                raise SystemExit("Asset verification failed: " + a["filename"])
            out = (root / a["repository_path"]).resolve()
            if out.parent != (here / "portraits").resolve():
                raise SystemExit("Unsafe destination")
            if out.exists() and out.read_bytes() != data:
                raise SystemExit("Refusing to overwrite different file: " + str(out))
            pending.append((out, data))
    for out, data in pending:
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_bytes(data)
        if digest(out.read_bytes()) != digest(data):
            raise SystemExit("Write verification failed")
        print("VERIFIED:", out.relative_to(root))
    print("No commit or push performed; review git status before committing.")
if __name__ == "__main__":
    main()
