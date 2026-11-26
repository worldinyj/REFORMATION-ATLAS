#!/usr/bin/env python3
"""Build a portable review-only ATLAS package from a local Git checkout.
Python 3.9+, standard library. No network, deployment, commit or push."""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import tempfile
import zipfile

HERE = Path(__file__).resolve().parent

def load(path):
    return json.loads(path.read_text(encoding="utf-8"))

def git_blob(data):
    return hashlib.sha1(("blob %d\0" % len(data)).encode("ascii") + data).hexdigest()

def within(root, name):
    p = PurePosixPath(name)
    if p.is_absolute() or ".." in p.parts or not p.parts or "\\" in name:
        raise ValueError("Unsafe path: " + name)
    target = root.joinpath(*p.parts).resolve()
    if root.resolve() not in target.parents:
        raise ValueError("Path outside root: " + name)
    return target

def require(condition, message):
    if not condition:
        raise ValueError(message)

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=HERE.parents[2])
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    root = args.repo_root.resolve()
    out = args.output.resolve()
    require(out.suffix.lower() == ".zip", "Output must be a ZIP")
    require(not out.exists(), "Refusing to overwrite output")
    data = load(HERE / "atlas_preview.json")
    manifest = load(HERE / "asset_manifest.json")
    search = load(HERE / "search_index.json")
    require(data["mode"] == "research_preview_only", "Wrong package mode")
    for flag in ("can_ship", "can_merge_main", "can_import_ai_studio"):
        require(data[flag] is False, "Release guard: " + flag)
    require(data["assets"] == manifest["assets"], "Asset manifest mismatch")
    expected = {"volumes": 8, "chapters": 24, "cases": 52, "people": 10, "global_units": 6, "assets": 23}
    for key, n in expected.items():
        require(len(data[key]) == n, "Unexpected count: " + key)
    require(len(data["points"]["features"]) == 36 and len(data["theology"]["units"]) == 5, "Unexpected point/theology count")
    def ids(rows, key="id"):
        values = [r[key] for r in rows]
        require(len(values) == len(set(values)), "Duplicate " + key)
        return set(values)
    C, V, P, A, K = ids(data["chapters"]), ids(data["volumes"]), ids(data["people"]), ids(data["assets"]), ids(data["cases"], "case_id")
    T, G = ids(data["theology"]["units"]), ids(data["global_units"])
    require(ids(search["records"]) == C, "Search index mismatch")
    for v in data["volumes"]:
        require(set(v["chapter_ids"]) <= C and v["map_asset_id"] in A, "Volume reference")
    for c in data["chapters"]:
        require(c["volume_id"] in V and c["transition"]["next_chapter_id"] in C, "Chapter navigation")
        for key, pool in (("case_ids", K), ("person_ids", P), ("theology_ids", T), ("global_ids", G), ("document_asset_ids", A)):
            require(set(c[key]) <= pool, "Broken " + key + ": " + c["id"])
        require(all(isinstance(x, str) and x.strip() for x in (c["overview"]["text"], c["intermediate"]["text"], c["deep"]["markdown"])), "Missing text")
    for k in data["cases"]:
        require(k["chapter_id"] in C and k["volume_id"] in V, "Case reference")
    for f in data["points"]["features"]:
        require(f["properties"]["case_id"] in K and f["properties"]["chapter_id"] in C, "Point reference")
    for p in data["people"]:
        require(p["chapter_id"] in C and p["symbol_asset_id"] in A and p["portrait_asset_id"] is None, "Person/fallback reference")
    require(data["timeline"]["asset_id"] in A, "Timeline reference")
    paths = set()
    verified = []
    for a in manifest["assets"]:
        rel = a["preview_path"]
        require(rel.startswith("assets/") and rel.endswith(".svg") and rel not in paths, "Invalid or duplicate asset path")
        paths.add(rel)
        src = within(root, a["source_path"])
        content = src.read_bytes()
        require(git_blob(content) == a["blob_sha"], "Git blob mismatch: " + str(src))
        verified.append((rel, content))
    docs = ["atlas_preview.json", "search_index.json", "asset_manifest.json", "package_qa.json", "DATA_CONTRACT.md", "AI_STUDIO_REVIEW_GUIDE_KO.md", "README.md"]
    out.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=out.parent) as tmp:
        staged = Path(tmp) / "package.zip"
        with zipfile.ZipFile(staged, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as z:
            for name in docs:
                z.writestr(name, (HERE / name).read_bytes())
            for name, content in verified:
                z.writestr(name, content)
        with zipfile.ZipFile(staged) as z:
            require(z.testzip() is None, "ZIP integrity error")
            require(set(z.namelist()) == set(docs) | paths, "ZIP inventory mismatch")
            for a in manifest["assets"]:
                require(git_blob(z.read(a["preview_path"])) == a["blob_sha"], "ZIP asset hash mismatch")
        # Exclusive creation prevents overwriting a concurrently created output.
        with out.open("xb") as f:
            f.write(staged.read_bytes())
    print("RESEARCH PREVIEW ONLY:", out)
    print("Verified SVG assets:", len(verified))
    print("ZIP SHA256:", hashlib.sha256(out.read_bytes()).hexdigest())

if __name__ == "__main__":
    main()
