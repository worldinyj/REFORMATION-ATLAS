#!/usr/bin/env node
"use strict";

/*
 * REFORMATION-ATLAS V4.25 browser e2e (Chromium / Playwright)
 * The source is the actual V4.24 standalone HTML from the repository.
 * No network, cookies, remote assets, server, Analytics or user responses.
 */
const fs = require("node:fs");
const path = require("node:path");
const { pathToFileURL } = require("node:url");
const { chromium } = require("playwright");

const repoRoot = path.resolve(__dirname, "../..");
const target = path.join(repoRoot, "preview/V424_L0_EDITORIAL_ALPHA_OFFLINE_PREVIEW.html");
const artifactRoot = path.join(repoRoot, "research/artifacts/V425_browser_checks");
fs.mkdirSync(artifactRoot, { recursive: true });
if (!fs.existsSync(target)) throw new Error("Missing V4.24 HTML: " + target);

const url = pathToFileURL(target).href;
const checks = [];
const issues = [];
function record(viewport, test, success, detail) {
  checks.push({ viewport, test, status: success ? "PASS" : "FAIL", detail: String(detail || "") });
  if (!success) issues.push({ viewport, test, detail: String(detail || "") });
}
const targets = [
  { id: "desktop", width: 1440, height: 900 },
  { id: "tablet", width: 768, height: 1024 },
  { id: "mobile", width: 375, height: 812 },
  { id: "small-mobile", width: 320, height: 700 }
];

async function capture(page, label) {
  await page.screenshot({
    path: path.join(artifactRoot, label + ".png"),
    animations: "disabled",
    fullPage: true
  });
}

(async () => {
  const browser = await chromium.launch({ headless: true, args: ["--no-sandbox"] });
  try {
    for (const targetViewport of targets) {
      const tag = targetViewport.id;
      const context = await browser.newContext({
        viewport: { width: targetViewport.width, height: targetViewport.height },
        deviceScaleFactor: 1,
        reducedMotion: "reduce",
        locale: "ko-KR"
      });
      const page = await context.newPage();
      const runtime = [];
      const remote = [];
      page.on("pageerror", err => runtime.push(String(err)));
      page.on("console", msg => { if (msg.type() === "error") runtime.push("console: " + msg.text()); });
      page.on("request", req => {
        if (/^https?:/i.test(req.url())) remote.push(req.url());
      });

      async function visit(hash) {
        await page.goto(url + hash, { waitUntil: "load" });
        await page.waitForSelector("main .hero", { timeout: 10000 });
      }
      async function checkOverflow(label) {
        const metric = await page.evaluate(() => ({
          viewport: window.innerWidth,
          document: document.documentElement.scrollWidth,
          body: document.body.scrollWidth
        }));
        record(tag, "horizontal-overflow-" + label,
          metric.document <= metric.viewport + 1 && metric.body <= metric.viewport + 1,
          JSON.stringify(metric));
      }

      await visit("#/volumes");
      record(tag, "volume-index-cards", await page.locator("main .grid .card").count() === 8, "expected 8");
      await checkOverflow("volume-index");
      await capture(page, tag + "-volumes");

      for (let i = 1; i <= 8; i++) {
        const vol = "VOL-" + String(i).padStart(2, "0");
        await visit("#/volumes/" + vol);
        const contentCount = await page.locator("main .article").count();
        const related = await page.locator("main .anchor").count();
        record(tag, vol + "-readable", contentCount === 1 && related === (i === 8 ? 0 : 6), "article=" + contentCount + "; links=" + related);
        await checkOverflow(vol);
      }
      await capture(page, tag + "-volume08");

      await visit("#/themes");
      record(tag, "theme-index-cards", await page.locator("main .grid .card").count() === 6, "expected 6");
      await checkOverflow("theme-index");
      await capture(page, tag + "-themes");

      for (let i = 1; i <= 6; i++) {
        const theme = "T415-" + String(i).padStart(2, "0");
        await visit("#/themes/" + theme);
        const related = await page.locator("main .anchor").count();
        record(tag, theme + "-seven-history-links", related === 7, "anchors=" + related);
        await checkOverflow(theme);
      }
      await capture(page, tag + "-theme06");

      await visit("#/themes/T415-01");
      const themeLabel = await page.locator("main .anchor").first().innerText();
      record(tag, "human-readable-anchor-role", themeLabel.includes("핵심 사례") && !themeLabel.includes("CORE_CASE"), themeLabel);
      await page.locator("main .anchor").first().click();
      await page.waitForURL(/#\/volumes\/VOL-01$/);
      record(tag, "theme-to-volume-click", (await page.locator("main .article").count()) === 1, "clicked actual first theme anchor");
      const focusTarget = await page.evaluate(() => document.activeElement && document.activeElement.id);
      record(tag, "keyboard-focus-after-navigation", focusTarget === "main", "activeElement=" + focusTarget);

      for (let i = 1; i <= 6; i++) {
        await visit("#/reader/" + i);
        record(tag, "reader-" + i, (await page.locator("main .article").count()) === 1, "chapter " + i);
        await checkOverflow("reader-" + i);
      }
      await visit("#/reader/1");
      await page.locator("main .controls button").last().click();
      await page.waitForURL(/#\/reader\/2$/);
      record(tag, "reader-next-click", (await page.locator("main .article").count()) === 1, "next chapter 2");
      await capture(page, tag + "-reader");

      await visit("#/volumes");
      const input = page.locator("#search");
      await input.fill("후스");
      await page.waitForURL(/#\/search$/);
      const results = await page.locator("main .grid .card").count();
      record(tag, "search-actual-input", results > 0, "query=후스, results=" + results);
      await checkOverflow("search");
      await capture(page, tag + "-search");

      await visit("#/check");
      const checkText = await page.locator("main").innerText();
      record(tag, "built-in-reference-check", checkText.includes("구조 점검 통과"), "42 internal links expected");
      await checkOverflow("integrity");
      record(tag, "no-browser-page-errors", runtime.length === 0, JSON.stringify(runtime));
      record(tag, "no-remote-requests", remote.length === 0, JSON.stringify(remote));
      const nav = await page.locator('nav[aria-label="콘텐츠 탐색"]').count();
      record(tag, "accessible-navigation-landmark", nav === 1, "nav label must exist");
      record(tag, "language-declaration", await page.locator("html").getAttribute("lang") === "ko", "lang=ko");

      await context.close();
    }
  } finally {
    await browser.close();
  }
  const summary = {
    version: "V4.25",
    input: "preview/V424_L0_EDITORIAL_ALPHA_OFFLINE_PREVIEW.html",
    actual_browser_engine: "Chromium / Playwright",
    date: new Date().toISOString(),
    viewport_profiles: targets,
    checks_performed: checks.length,
    checks_passed: checks.filter(x => x.status === "PASS").length,
    failures: issues,
    passes: checks,
    browser_execution_status: issues.length ? "FAILED" : "PASSED",
    claims: {
      human_reader_tested: false,
      expert_history_signoff: false,
      manual_screenshot_reviewed: false,
      iOS_Safari_tested: false,
      can_ship: false
    }
  };
  const reportFile = path.join(artifactRoot, "V425_BROWSER_REPORT.json");
  fs.writeFileSync(reportFile, JSON.stringify(summary, null, 2) + "\n", "utf8");
  console.log(JSON.stringify({
    input: summary.input,
    browser: summary.actual_browser_engine,
    tested_viewports: targets.map(x => x.id),
    count: summary.checks_performed,
    pass: summary.checks_passed,
    fail: issues.length,
    failures: issues,
    report: path.relative(repoRoot, reportFile)
  }, null, 2));
  if (issues.length) process.exitCode = 1;
})().catch(err => { console.error(err); process.exitCode = 1; });
