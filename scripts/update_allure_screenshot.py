"""Regenerate the README Allure report screenshot after the report is built."""

from __future__ import annotations

import argparse
import http.server
import os
import shutil
import subprocess
import sys
import tempfile
import threading
from pathlib import Path


CHROME_CANDIDATES = [
    Path(os.environ.get("CHROME_PATH", "")),
    Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe"),
    Path(r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"),
    Path(r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"),
    Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"),
]


class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, fmt, *args):
        pass


def find_chrome() -> str | None:
    for candidate in CHROME_CANDIDATES:
        if candidate.is_file():
            return str(candidate)
    return shutil.which("chrome") or shutil.which("msedge")


def start_server(report_dir: Path):
    handler = lambda *args, **kwargs: QuietHandler(
        *args, directory=str(report_dir), **kwargs
    )
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server, server.server_address[1]


def capture_screenshot(chrome: str, url: str, screenshot: Path) -> None:
    with tempfile.TemporaryDirectory(
        prefix="allure-screenshot-profile-", ignore_cleanup_errors=True
    ) as profile:
        command = [
            chrome,
            "--headless=new",
            "--disable-gpu",
            "--disable-software-rasterizer",
            "--no-sandbox",
            "--disable-extensions",
            "--disable-background-networking",
            "--no-first-run",
            "--no-default-browser-check",
            f"--user-data-dir={profile}",
            "--virtual-time-budget=10000",
            "--window-size=1440,900",
            f"--screenshot={screenshot}",
            url,
        ]
        subprocess.run(
            command,
            check=True,
            timeout=45,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )


def parse_args(argv):
    parser = argparse.ArgumentParser(
        description="Generate docs/allure-report.png from reports/allure-report."
    )
    parser.add_argument("--report-dir", type=Path, help="Allure report directory.")
    parser.add_argument("--output", type=Path, help="PNG output path.")
    return parser.parse_args(argv)


def main(argv=None) -> int:
    args = parse_args(argv)
    repo_root = Path(__file__).resolve().parents[1]
    report_dir = args.report_dir or repo_root / "reports" / "allure-report"
    output = args.output or repo_root / "docs" / "allure-report.png"

    if not (report_dir / "index.html").is_file():
        print(f"Allure report not found: {report_dir / 'index.html'}", file=sys.stderr)
        return 1

    chrome = find_chrome()
    if not chrome:
        print("Chrome or Edge not found. Set CHROME_PATH to the browser exe.", file=sys.stderr)
        return 1

    output.parent.mkdir(parents=True, exist_ok=True)
    server, port = start_server(report_dir)
    try:
        url = f"http://127.0.0.1:{port}/index.html"
        with tempfile.TemporaryDirectory(
            prefix="allure-screenshot-output-", ignore_cleanup_errors=True
        ) as tmp:
            screenshot = Path(tmp) / "allure-report.png"
            capture_screenshot(chrome, url, screenshot)
            if not screenshot.is_file() or screenshot.stat().st_size < 10_000:
                print("Screenshot looks incomplete; the report may still be loading.", file=sys.stderr)
                return 1
            shutil.copyfile(screenshot, output)
    finally:
        server.shutdown()
        server.server_close()

    print(f"Updated {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
