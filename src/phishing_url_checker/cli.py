from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path
from .checker import URLValidationError, analyze_url

VERSION = "1.0.0"

def _render(report) -> str:
    lines = [f"URL: {report.normalized_url}", f"Host: {report.hostname}", f"Risk: {report.risk.upper()} ({report.score}/100)"]
    if report.findings:
        lines.append("Findings:")
        lines.extend(f"  - [{f.severity.upper()}] {f.message} ({f.code}, +{f.points})" for f in report.findings)
    else:
        lines.append("Findings: none from the built-in heuristic rules")
    lines.append("Note: heuristic result only; it does not prove that a site is safe or malicious.")
    return "\n".join(lines)

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="phishcheck", description="Offline, explainable phishing URL risk checker")
    parser.add_argument("urls", nargs="*", help="HTTP(S) URL(s) to analyze")
    parser.add_argument("--file", type=Path, help="UTF-8 text file containing one URL per line")
    parser.add_argument("--json", action="store_true", help="emit JSON")
    parser.add_argument("--fail-on", choices=["medium", "high"], help="return exit code 2 when this risk threshold is met")
    parser.add_argument("--version", action="version", version=f"phishcheck {VERSION} — Radwan Abdulhadi Ahmed / @rad03i2")
    return parser

def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    values = list(args.urls)
    if args.file:
        try:
            values.extend(line.strip() for line in args.file.read_text(encoding="utf-8-sig").splitlines() if line.strip() and not line.lstrip().startswith("#"))
        except OSError as exc:
            print(f"error: {exc}", file=sys.stderr); return 1
    if not values:
        print("error: provide at least one URL or --file", file=sys.stderr); return 1
    reports = []
    try:
        reports = [analyze_url(value) for value in values]
    except URLValidationError as exc:
        print(f"error: {exc}", file=sys.stderr); return 1
    if args.json:
        print(json.dumps([r.to_dict() for r in reports], ensure_ascii=False, indent=2))
    else:
        print("\n\n".join(_render(r) for r in reports))
    if args.fail_on:
        threshold = {"medium": 25, "high": 50}[args.fail_on]
        if any(r.score >= threshold for r in reports): return 2
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
