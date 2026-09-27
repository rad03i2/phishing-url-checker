<div align="center">

<img src="assets/project-cover.svg" alt="Phishing URL Checker" width="100%" />
<img src="assets/project-logo.svg" alt="Phishing URL Checker logo" width="92" />

# Phishing URL Checker — English Guide

**Offline structural URL analysis with explainable heuristic findings.**

[![CI](https://github.com/rad03i2/phishing-url-checker/actions/workflows/ci.yml/badge.svg)](https://github.com/rad03i2/phishing-url-checker/actions/workflows/ci.yml)

**[Main README](README.md) · [العربية](README_AR.md) · [Architecture](docs/ARCHITECTURE.md) · [Security](SECURITY.md)**

</div>

---

## Purpose

Phishing URL Checker performs a local first-pass inspection of HTTP(S) URL text. It is designed for developers, students, support teams and security-aware users who want an auditable structural score without causing network traffic to the submitted destination.

The result is heuristic evidence, not a malicious/safe verdict.

## Current capabilities

- validates HTTP and HTTPS URLs;
- analyzes plain HTTP, user-info, raw-IP hosts and Punycode;
- detects deep subdomains, known shorteners, selected watch-list TLDs and unusual ports;
- detects long URLs and heavily hyphenated hosts;
- looks for multiple credential/account terms in path/query text;
- detects URL-like redirect parameters;
- detects selected encoded delimiters in the authority;
- produces a score from 0 to 100;
- emits explainable findings with stable codes;
- supports text and JSON output;
- analyzes multiple command-line URLs or UTF-8 files;
- exposes `--fail-on medium|high` for automation;
- exposes a Python API;
- has zero runtime dependencies.

## Install

```bash
git clone https://github.com/rad03i2/phishing-url-checker.git
cd phishing-url-checker
python -m pip install -e .
```

For development:

```bash
python -m pip install -e . pytest
```

## Usage

```bash
phishcheck https://example.com
phishcheck "http://user@192.0.2.1/login/verify"
phishcheck --file examples/urls.txt
phishcheck https://example.com --json
phishcheck suspicious-url-here --fail-on high
python -m phishing_url_checker https://example.com
```

## Python API

```python
from phishing_url_checker import analyze_url

report = analyze_url("https://example.com/account/verify")

print(report.hostname)
print(report.score)
print(report.risk)

for finding in report.findings:
    print(finding.code, finding.severity, finding.points, finding.message)
```

## Scoring

```text
minimal  score = 0
low      score = 1..24
medium   score = 25..49
high     score = 50..100
```

The total is the sum of current rule points capped at 100. Finding codes are better automation anchors than human-readable prose.

## Privacy

The analyzer does not intentionally resolve hostnames, make HTTP requests, expand short links, fetch certificates, query reputation services or send telemetry.

## Important limitation

A structurally ordinary URL may still be malicious. A legitimate URL may trigger one or more rules. Combine the result with other controls for important security decisions.

## Testing

```bash
python -m compileall -q src tests
python -m pytest -q
```

CI runs on Python 3.10, 3.12 and 3.13 across Ubuntu, Windows and macOS.

## More documentation

- [Architecture](docs/ARCHITECTURE.md)
- [Brand identity](docs/BRAND.md)
- [Security](SECURITY.md)
- [Support](SUPPORT.md)
- [Contributing](CONTRIBUTING.md)
- [Changelog](CHANGELOG.md)
- [License](LICENSE)

## Author

**Radwan Abd alhady Ahmed**  
**رضوان عبدالهادي**  
GitHub: [@rad03i2](https://github.com/rad03i2)
