#!/usr/bin/env python3
"""Reproducible, opt-in retrieval of the 1529 Zurich W2119 digitization.

Default = offline preview. This is not OCR, palaeographic collation, or approval.
Downloaded source bytes are deliberately saved OUTSIDE the git repository.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import sys
import tempfile
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
VLID = "170052"
TARGETS = {
    "w2119-pdf": {
        "url": "https://www.e-rara.ch/download/pdf/170052.pdf",
        "type": "pdf",
        "name": "W2119_1529_e-rara_170052.pdf",
    },
    "w2119-iiif": {
        "url": "https://www.e-rara.ch/i3f/v20/170052/manifest",
        "type": "json",
        "name": "W2119_1529_e-rara_170052_manifest.json",
    },
}
MAX_BYTES = 30 * 1024 * 1024

def inspect_bytes(data, kind):
    """File-format check only. Return canvas count when IIIF JSON is available."""
    if kind == "pdf":
        if not data.startswith(b"%PDF-"):
            raise ValueError("PDF magic bytes missing (likely HTML/block page)")
        if b"%%EOF" not in data[-4096:]:
            raise ValueError("PDF EOF marker missing near file end")
        return {"type": "PDF", "canvas_count": None}
    try:
        obj = json.loads(data.decode("utf-8"))
    except (UnicodeError, ValueError) as exc:
        raise ValueError("Manifest is not valid UTF-8 JSON") from exc
    if not isinstance(obj, dict):
        raise ValueError("IIIF manifest must be a JSON object")
    context = json.dumps(obj.get("@context", ""), ensure_ascii=False)
    if "iiif.io/api/presentation/2" not in context:
        raise ValueError("IIIF Presentation API v2 context not found")
    sequences = obj.get("sequences")
    if not isinstance(sequences, list) or not sequences:
        raise ValueError("IIIF v2 manifest missing sequences")
    canvases = sequences[0].get("canvases")
    if not isinstance(canvases, list) or not canvases:
        raise ValueError("IIIF manifest has no canvases")
    return {"type": "IIIF_V2_MANIFEST", "canvas_count": len(canvases),
            "canvas_ids": [c.get("@id") for c in canvases]}

def download(url):
    if not url.startswith("https://www.e-rara.ch/"):
        raise ValueError("Only the institution's W2119 e-rara endpoint is permitted")
    req = Request(url, headers={"User-Agent": "ATLAS-research-source-audit/2.24"})
    with urlopen(req, timeout=30) as response:
        final_url = response.geturl()
        if not final_url.startswith("https://www.e-rara.ch/"):
            raise ValueError("Unexpected download redirect domain")
        header_size = response.headers.get("Content-Length")
        if header_size and int(header_size) > MAX_BYTES:
            raise ValueError("Server file larger than 30 MiB")
        parts, total = [], 0
        while True:
            chunk = response.read(min(1024 * 1024, MAX_BYTES - total + 1))
            if not chunk:
                break
            total += len(chunk)
            if total > MAX_BYTES:
                raise ValueError("Downloaded bytes exceed 30 MiB")
            parts.append(chunk)
    return b"".join(parts)

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", choices=sorted(TARGETS), default="w2119-pdf")
    parser.add_argument("--mode", choices=["preview", "fetch", "self-test"], default="preview")
    parser.add_argument("--output-dir", default=str(Path.home() / "Downloads" / "REFORMATION_ATLAS_V224_SOURCES"))
    args = parser.parse_args()
    if args.mode == "self-test":
        assert VLID == "170052" and len(TARGETS) == 2
        assert all(VLID in x["url"] for x in TARGETS.values())
        assert inspect_bytes(b"%PDF-1.4\n...\n%%EOF\n", "pdf")["type"] == "PDF"
        example = {"@context": "http://iiif.io/api/presentation/2/context.json",
                   "sequences": [{"canvases": [{"@id": "https://example.org/canvas1"}]}]}
        assert inspect_bytes(json.dumps(example).encode(), "json")["canvas_count"] == 1
        for kind, data in [("pdf", b"<!doctype html>"), ("json", b"<html>Error</html>")]:
            try:
                inspect_bytes(data, kind)
            except ValueError:
                pass
            else:
                raise AssertionError("invalid source accepted")
        print("PASS V224 offline source-file validation (no network request; no original images inspected)")
        return 0
    t = TARGETS[args.target]
    print(json.dumps({"target": args.target, "url": t["url"], "mode": args.mode,
                      "verified_witness": "1529 Zurich W2119 bibliographic identity",
                      "original_page_collated": False}, ensure_ascii=False, indent=2))
    if args.mode == "preview":
        print("DRY RUN: no network access. Use --mode fetch explicitly; never commit downloaded originals.")
        return 0
    out_dir = Path(args.output_dir).expanduser().resolve()
    if out_dir == ROOT or ROOT in out_dir.parents:
        raise ValueError("Refusing to write third-party source images inside Git repository")
    out_dir.mkdir(parents=True, exist_ok=True)
    try:
        raw = download(t["url"])
        info = inspect_bytes(raw, t["type"])
    except (HTTPError, URLError, TimeoutError, ValueError, OSError) as exc:
        print(f"FETCH NOT VERIFIED: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 2
    target = out_dir / t["name"]
    if target.exists():
        raise ValueError(f"Refusing to overwrite existing source: {target}")
    fd, tmp_name = tempfile.mkstemp(prefix=".atlas-v224-", dir=str(out_dir))
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(raw)
        os.replace(tmp_name, target)
    finally:
        if os.path.exists(tmp_name):
            os.unlink(tmp_name)
    result = {"source_url": t["url"], "saved_path": str(target),
              "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest(),
              "format_verified": info["type"], "canvas_count": info["canvas_count"],
              "original_pages_visually_inspected": 0,
              "zk_variant_readings_collated": 0, "publication_approved": False}
    if "canvas_ids" in info:
        result["canvas_ids"] = info["canvas_ids"]
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
