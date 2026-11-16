#!/usr/bin/env python3
"""Resolve Zwingliana 14/9 (1978) Rott article through official OJS pages.

Python stdlib only. Default discovers journal issue/article/PDF URLs; no writes.
--download explicitly saves verified %PDF bytes outside repository and SHA256.
--self-test runs synthetic HTML checks without any network access.
"""
import argparse
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import sys
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin, urlparse
from urllib.request import Request, urlopen

ARCHIVE = "https://zwingliana.ch/issue/archive"
TITLE = "Martin Bucer und die Schweiz"
ISSUE_RE = re.compile(r"14\s*/\s*9\s*\(?\s*1978\s*\)?", re.I)

class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.current = None
    def handle_starttag(self, tag, attrs):
        if tag == "a":
            a = dict(attrs)
            self.current = {"href": a.get("href", ""), "label": "", "type": a.get("type", "")}
    def handle_data(self, data):
        if self.current is not None:
            self.current["label"] += data
    def handle_endtag(self, tag):
        if tag == "a" and self.current is not None:
            self.current["label"] = " ".join(self.current["label"].split())
            self.links.append(self.current)
            self.current = None

def links(html_text):
    p = Links()
    p.feed(html_text)
    return p.links

def find_issue(source):
    c = [x for x in links(source)
         if ISSUE_RE.search(x["label"]) and "issue/view" in x["href"]]
    if len(c) != 1:
        raise ValueError(f"Expected one Zwingliana 14/9 (1978) issue; found {len(c)}")
    return c[0]

def find_article(source):
    c = [x for x in links(source)
         if TITLE.casefold() in x["label"].casefold() and "article/view" in x["href"]]
    if len(c) != 1:
        raise ValueError(f"Expected one Rott article; found {len(c)}")
    return c[0]

def find_pdf(source):
    c = []
    for x in links(source):
        url, label = x["href"].lower(), x["label"].lower()
        if ("article/download/" in url or ".pdf" in url
            or ("article/view/" in url
                and ("pdf" in label or "pdf" in x["type"].lower()))):
            c.append(x)
    if not c:
        raise ValueError("No PDF galley link; do not invent an article ID")
    labeled = [x for x in c if "pdf" in x["label"].lower()
               or "pdf" in x["type"].lower()]
    chosen = labeled if labeled else c
    if len(chosen) != 1:
        raise ValueError(f"Ambiguous PDF links ({len(chosen)}); manual check required")
    return chosen[0]

def safe_url(url, base):
    u = urljoin(base, url)
    if urlparse(u).scheme != "https":
        raise ValueError("HTTPS required")
    if urlparse(u).netloc.lower() not in {"zwingliana.ch", "www.zwingliana.ch"}:
        raise ValueError("Unexpected journal link host")
    return u

def get(url):
    if urlparse(url).scheme != "https":
        raise ValueError("HTTPS required")
    request = Request(url, headers={
        "User-Agent": "REFORMATION-ATLAS/source-audit (research; manual review)",
        "Accept": "text/html,application/pdf"})
    with urlopen(request, timeout=22) as response:
        content = response.read(20 * 1024 * 1024 + 1)
        if len(content) > 20 * 1024 * 1024:
            raise ValueError("Resource exceeds 20 MiB; manual review")
        return response.url, response.headers.get("Content-Type", ""), content

def self_test():
    archive = ('<a href="/issue/view/100">14/8 (1977)</a>'
               '<a href="/issue/view/101"><span>14/9</span> (1978)</a>')
    issue = ('<a href="/article/view/44">Other paper</a>'
             '<a href="/article/view/45">Martin Bucer und die Schweiz:'
             ' Drei unbekannte Briefe</a>')
    detail = '<a href="/article/view/45/90">PDF</a>'
    assert find_issue(archive)["href"] == "/issue/view/101"
    assert find_article(issue)["href"] == "/article/view/45"
    assert find_pdf(detail)["href"] == "/article/view/45/90"
    for source, fn in [
        (archive.replace("14/9", "14/7"), find_issue),
        (issue.replace(TITLE, "Different title"), find_article),
        ('<a href="/article/view/45">HTML</a>', find_pdf),
    ]:
        try: fn(source)
        except ValueError: pass
        else: raise AssertionError("Unverified source incorrectly accepted")
    assert safe_url("/issue/view/101", ARCHIVE) == "https://zwingliana.ch/issue/view/101"
    try: safe_url("https://untrusted.invalid/article/4", ARCHIVE)
    except ValueError: pass
    else: raise AssertionError("Untrusted host accepted")
    return {"status": "PASS", "checks": 7, "network_used": False}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--download", action="store_true")
    parser.add_argument("--out-dir", default="/tmp/reformation-atlas-sources")
    args = parser.parse_args()
    if args.self_test:
        print(json.dumps(self_test(), indent=2))
        return
    report = {"version": "V3.87", "archive": ARCHIVE, "issue": None,
              "article": None, "pdf_link": None, "pdf_downloaded": False,
              "printed_pages_inspected": [], "status": "DISCOVERY_ONLY", "errors": []}
    try:
        archive_actual, _, html = get(ARCHIVE)
        issue_url = safe_url(find_issue(html.decode("utf-8", "replace"))["href"], archive_actual)
        report["issue"] = issue_url
        issue_actual, _, html = get(issue_url)
        article_url = safe_url(find_article(html.decode("utf-8", "replace"))["href"], issue_actual)
        report["article"] = article_url
        article_actual, _, html = get(article_url)
        pdf_url = safe_url(find_pdf(html.decode("utf-8", "replace"))["href"], article_actual)
        report["pdf_link"] = pdf_url
        if args.download:
            resolved, mime, content = get(pdf_url)
            if not content.startswith(b"%PDF-"):
                raise ValueError(f"PDF signature not found ({mime}); URL {resolved}")
            output = Path(args.out_dir).expanduser().resolve()
            output.mkdir(parents=True, exist_ok=True)
            destination = output / "Rott_1978_Zwingliana_14-9_SOURCE_ONLY.pdf"
            if destination.exists():
                raise FileExistsError(f"Refusing overwrite {destination}")
            destination.write_bytes(content)
            report.update(pdf_downloaded=True, file=str(destination),
                          size_bytes=len(content),
                          sha256=hashlib.sha256(content).hexdigest(),
                          status="PDF_ACQUIRED_BUT_PAGES_UNINSPECTED")
            # Separately verify printed p489/p491 through image-based inspection.
    except (ValueError, HTTPError, URLError, OSError) as error:
        report["errors"].append(str(error))
    print(json.dumps(report, indent=2, ensure_ascii=False))
    if report["errors"]:
        sys.exit(1)

if __name__ == "__main__":
    main()
