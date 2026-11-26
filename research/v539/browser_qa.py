#!/usr/bin/env python3
"""Local Chromium acceptance test; optional Playwright dependency.
Never deploys or modifies the existing app."""
import argparse
from functools import partial
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
import json
from pathlib import Path
from threading import Thread

SITE = Path(__file__).resolve().parent / "site"

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--output", type=Path, required=True)
    p.add_argument("--chromium", help="Optional local Chromium executable")
    args = p.parse_args()
    from playwright.sync_api import sync_playwright
    args.output.mkdir(parents=True, exist_ok=False)
    data = json.loads((SITE / "atlas_preview.json").read_text(encoding="utf-8"))
    assert data["mode"] == "research_preview_only"
    assert not any(data[k] for k in ("can_ship", "can_merge_main", "can_import_ai_studio"))
    http = ThreadingHTTPServer(("127.0.0.1", 0), partial(SimpleHTTPRequestHandler, directory=str(SITE)))
    Thread(target=http.serve_forever, daemon=True).start()
    url = f"http://127.0.0.1:{http.server_port}/"
    records, errors = [], []
    def check(name, test):
        try:
            test()
            records.append({"name": name, "pass": True})
        except Exception as exc:
            records.append({"name": name, "pass": False, "error": str(exc)})
    def require(condition, message):
        if not condition:
            raise AssertionError(message)
    try:
        with sync_playwright() as pw:
            opts = {"headless": True}
            if args.chromium:
                opts["executable_path"] = args.chromium
            browser = pw.chromium.launch(**opts)
            page = browser.new_page(viewport={"width": 1440, "height": 1000})
            page.on("pageerror", lambda exc: errors.append(str(exc)))
            def go(route, heading=None):
                page.goto(url + "#" + route)
                page.locator("main h1").wait_for()
                if heading is not None:
                    require(page.locator("main h1").inner_text() == heading, "Unexpected heading")
                require(page.locator("main h1").inner_text() != "미리보기를 열 수 없습니다", "Load failed")
            def images(n):
                imgs = page.locator("main img")
                require(imgs.count() == n, "Image count")
                ok = imgs.evaluate_all("""async imgs => {for (const i of imgs) i.loading='eager'; return (await Promise.all(imgs.map(async i=>{try {await i.decode();return i.naturalWidth>0}catch{return false}}))).every(Boolean)}""")
                require(ok, "Image decode failed")
            def route_count(route, count, tag="main article.card"):
                go(route)
                require(page.locator(tag).count() == count, "Count mismatch: " + route)
            check("home", lambda: route_count("home", 8))
            for v in data["volumes"]:
                def volume(v=v):
                    go("volume/" + v["id"], v["title"])
                    require(page.locator("main article.card").count() == 3, "Chapter count")
                    images(1)
                check("volume:" + v["id"], volume)
            for c in data["chapters"]:
                for level in ("overview", "intermediate", "deep"):
                    def chapter(c=c, level=level):
                        go("chapter/" + c["id"] + "/" + level, c["title"])
                        require(page.locator("article.reading").inner_text().strip(), "Empty article")
                        require(page.locator(".next a").get_attribute("href") == "#chapter/" + c["transition"]["next_chapter_id"] + "/overview", "Next link")
                    check(c["id"] + ":" + level, chapter)
            for v in data["volumes"]:
                def maps(v=v):
                    go("maps")
                    page.locator("main select").select_option(v["id"])
                    n = sum(v["kind"] == "thematic" or c["volume_id"] == v["id"] for c in data["cases"])
                    require(page.locator("main article.card").count() == n, "Case count")
                    images(1)
                check("maps:" + v["id"], maps)
            def people():
                route_count("people", 10)
                images(10)
            check("people", people)
            def documents():
                go("documents")
                images(5)
            check("documents", documents)
            check("themes", lambda: route_count("themes", 11))
            for q, n in (("루터",4),("타밀어",3),("서상륜",3),("zzzz_nonexistent_zzzz",0)):
                def search(q=q, n=n):
                    go("search")
                    page.get_by_role("searchbox").fill(q)
                    page.get_by_role("button", name="검색").click()
                    require(page.locator("main article.card").count() == n, "Search count")
                check("search:" + q, search)
            for width in (360, 768, 1440):
                for route in ("home", "chapter/L448-04-02/deep", "people", "maps", "documents"):
                    def layout(width=width, route=route):
                        page.set_viewport_size({"width": width, "height": 900})
                        go(route)
                        require(page.evaluate("document.documentElement.scrollWidth <= window.innerWidth + 1"), "Horizontal overflow")
                        page.screenshot(path=str(args.output / (str(width) + "_" + route.replace("/", "_") + ".png")), full_page=True)
                    check("layout:" + str(width) + ":" + route, layout)
            def keyboard():
                go("chapter/L448-04-02/deep")
                page.locator("#skip-link").focus()
                page.keyboard.press("Enter")
                require(page.evaluate("document.activeElement.id") == "main", "Skip focus")
                require(page.evaluate("location.hash") == "#chapter/L448-04-02/deep", "Skip route changed")
            check("skip-link", keyboard)
            browser.close()
    finally:
        http.shutdown()
        http.server_close()
    report = {"scope": "real local Chromium acceptance", "checks": records, "page_errors": errors,
              "passed": sum(r["pass"] for r in records), "total": len(records), "can_ship": False}
    (args.output / "browser_qa.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"passed": report["passed"], "total": report["total"], "page_errors": errors}, ensure_ascii=False))
    if report["passed"] != report["total"] or errors:
        raise SystemExit(1)

if __name__ == "__main__":
    main()
