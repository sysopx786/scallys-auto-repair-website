#!/usr/bin/env python3
"""Browser QA for Batches 1–4 bilingual Scally's service pages.
Run after src/build.py and check_site.py.
Requires: pip install playwright && python -m playwright install chromium
"""
import json
import os
from pathlib import Path
import subprocess
import sys
import time
import urllib.request
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
OUT = Path(os.environ.get("SCALLYS_QA_OUT", "/tmp/scallys-qa"))
OUT.mkdir(parents=True, exist_ok=True)
SLUGS = (
    "pa-state-inspection",
    "emissions-repair",
    "pre-purchase-inspection",
    "timing-belt-chain",
    "engine-tune-up",
    "electrical-repair",
    "auto-light-repair",
    "power-windows-locks",
    "wheel-bearings-hubs",
    "oil-leak-repair",
    "fuel-system-repair",
    "clutch-repair",
    "engine-transmission-mounts",
    "cv-axle-differential",
    "hybrid-service",
    "wheel-repair",
    "rust-repair",
    "auto-body-repair",
    "auto-glass",
)
WIDTHS = (320, 390, 768, 1100, 1280, 1600)
BASE = "http://127.0.0.1:8765"
REPORT = []
FAILURES = []

server = subprocess.Popen(
    [sys.executable, "-m", "http.server", "8765", "--bind", "127.0.0.1"],
    cwd=ROOT,
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL,
)
try:
    for attempt in range(40):
        try:
            with urllib.request.urlopen(BASE + "/", timeout=2) as reply:
                if reply.status == 200:
                    break
        except Exception:
            time.sleep(0.25)
    else:
        raise RuntimeError("Local site server did not start")

    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True, args=["--no-sandbox"])
        try:
            for lang in ("en", "es"):
                for slug in SLUGS:
                    url_path = f"/{slug}/" if lang == "en" else f"/es/{slug}/"
                    for width in WIDTHS:
                        page = browser.new_page(viewport={"width": width, "height": 900}, device_scale_factor=1)
                        errors = []
                        page.on("pageerror", lambda err: errors.append(str(err)))
                        page.on(
                            "console",
                            lambda msg: errors.append("console: " + msg.text) if msg.type == "error" else None,
                        )
                        try:
                            response = page.goto(BASE + url_path, wait_until="load", timeout=30000)
                            page.evaluate("async () => { await document.fonts.ready; return true; }")
                            measurement = page.evaluate("""() => ({
                                viewport: window.innerWidth,
                                documentWidth: document.documentElement.scrollWidth,
                                bodyWidth: document.body.scrollWidth,
                                language: document.documentElement.lang,
                                headingCount: document.querySelectorAll('h1').length,
                                visibleMainText: (document.querySelector('main')?.innerText || '').trim().length,
                                anchors: Array.from(document.querySelectorAll('a[href]')).length
                            })""")
                            status = response.status if response else None
                            label = f"{lang}/{slug} @ {width}px"
                            problems = []
                            if status != 200:
                                problems.append(f"HTTP {status}")
                            if measurement["language"] != lang:
                                problems.append(f"HTML lang={measurement['language']!r}")
                            if measurement["headingCount"] != 1:
                                problems.append(f"{measurement['headingCount']} H1 headings")
                            if measurement["visibleMainText"] < 800:
                                problems.append("Missing or very short main content")
                            if measurement["documentWidth"] > measurement["viewport"] + 1:
                                problems.append(f"Horizontal overflow {measurement['documentWidth']} > {measurement['viewport']}")
                            if errors:
                                problems.extend(errors)
                            if width in (390, 1280) and status == 200:
                                page.screenshot(path=str(OUT / f"{lang}-{slug}-{width}.png"), full_page=True)
                            row = {
                                "page": url_path,
                                "language": lang,
                                "width": width,
                                "http": status,
                                "documentWidth": measurement["documentWidth"],
                                "mainTextLength": measurement["visibleMainText"],
                                "errors": problems,
                            }
                            REPORT.append(row)
                            if problems:
                                FAILURES.append(f"{label}: {'; '.join(problems)}")
                            print(f"{'FAIL' if problems else 'PASS'} {label} HTTP {status} docWidth={measurement['documentWidth']}")
                        except Exception as exc:
                            FAILURES.append(f"{lang}/{slug} @ {width}px: {type(exc).__name__}: {exc}")
                            print("FAIL", FAILURES[-1])
                        finally:
                            page.close()
        finally:
            browser.close()
finally:
    server.terminate()
    try:
        server.wait(timeout=5)
    except subprocess.TimeoutExpired:
        server.kill()

(OUT / "batches-1-4-browser-report.json").write_text(
    json.dumps({"checks": len(REPORT), "failures": FAILURES, "measurements": REPORT}, indent=2) + "\n",
    encoding="utf-8",
)
print(f"\nBatches 1–4 browser checks: {len(REPORT)} checks, {len(FAILURES)} failures")
for item in FAILURES:
    print(" -", item)
if len(REPORT) != len(SLUGS) * 2 * len(WIDTHS) or FAILURES:
    sys.exit(1)
print("ALL BROWSER CHECKS PASSED")
