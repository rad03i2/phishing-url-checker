<div align="center">

<img src="assets/project-cover.svg" alt="Phishing URL Checker — offline explainable URL forensics" width="100%" />

<br/>

<img src="assets/project-logo.svg" alt="Phishing URL Checker logo" width="104" />

# Phishing URL Checker

**Offline, explainable URL risk analysis — inspect the URL text without visiting the destination.**

<div dir="rtl">
<strong>تحليل محلي وقابل للتفسير لبنية روابط HTTP(S)، من دون فتح الموقع أو إرسال الرابط إلى خدمة خارجية.</strong>
</div>

<br/>

[![CI](https://github.com/rad03i2/phishing-url-checker/actions/workflows/ci.yml/badge.svg)](https://github.com/rad03i2/phishing-url-checker/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/Python-3.10%2B-4DD5FF?logo=python&logoColor=0B0F14)
![Offline](https://img.shields.io/badge/network-no%20requests-87F5B5)
![Explainable](https://img.shields.io/badge/output-explainable-FFB547)
![Score](https://img.shields.io/badge/risk-0..100-FF5D5D)
![License](https://img.shields.io/badge/license-MIT-A9B6C2)

**[العربية](README_AR.md) · [English](README_EN.md) · [Rules & Architecture](docs/ARCHITECTURE.md) · [Security](SECURITY.md) · [Support](SUPPORT.md)**

</div>

---

## Threat Lens: inspect structure, not content

Phishing URL Checker analyzes the **lexical and structural shape** of an HTTP(S) URL. It never needs to resolve the hostname, fetch the page, follow a redirect, or submit the link to a reputation provider.

> A heuristic score is evidence, not a verdict. A low score does not prove safety, and a high score does not prove malicious intent.

<table>
<tr>
<td width="25%"><strong>Private by design</strong><br/><sub>Submitted URLs stay local during analysis.</sub></td>
<td width="25%"><strong>Explainable</strong><br/><sub>Every contribution has a code, severity, point value and message.</sub></td>
<td width="25%"><strong>Deterministic</strong><br/><sub>The same URL and rule set produce the same structural result.</sub></td>
<td width="25%"><strong>Automation-ready</strong><br/><sub>JSON output and risk thresholds work well in scripts and CI.</sub></td>
</tr>
</table>

## What it can flag

The current rules inspect signals such as:

| Signal | Example interpretation |
|---|---|
| Plain HTTP | Connection is not protected by HTTPS |
| URL user-info | Text before the hostname may visually mislead a user |
| Raw IP host | Host is an IP address rather than a domain name |
| Punycode | Internationalized hostname needs careful human verification |
| Deep subdomains | Host contains an unusually long label chain |
| Known shorteners | Final destination is hidden by the shortened URL |
| Watch-list TLD | A selected TLD receives a low-weight caution signal |
| Unusual port | Web URL uses a port other than 80 or 443 |
| Long URL | Length can make destination details harder to inspect |
| Many hyphens | Host contains several hyphens |
| Credential language | Path/query includes multiple account/login-related terms |
| Redirect parameter | Query contains a URL-like redirect destination |
| Encoded authority delimiters | Encoded delimiter characters appear in the authority |

The implementation and point values are visible in `src/phishing_url_checker/checker.py`.

## Quick start

```bash
git clone https://github.com/rad03i2/phishing-url-checker.git
cd phishing-url-checker
python -m pip install -e .
```

Analyze a normal URL:

```bash
phishcheck https://example.com
```

Analyze a structurally suspicious example using documentation-safe addresses:

```bash
phishcheck "http://user@192.0.2.1/login/verify"
```

Batch mode:

```bash
phishcheck --file examples/urls.txt
```

JSON:

```bash
phishcheck https://example.com --json
```

CI-style threshold:

```bash
phishcheck suspicious-url-here --fail-on high
```

## Risk model

The checker adds rule points, caps the total at 100, then maps the score to the current bands:

```text
0          → minimal
1..24      → low
25..49     → medium
50..100    → high
```

Each finding remains visible, so automation should prefer stable finding `code` values rather than parsing the human-readable prose.

## Example output

```text
URL: http://user@192.0.2.1/login/verify
Host: 192.0.2.1
Risk: HIGH (.../100)
Findings:
  - [MEDIUM] Connection is not protected by HTTPS. (plain-http, +15)
  - [HIGH] URL contains user-info before the hostname... (userinfo, +30)
  - [HIGH] Hostname is a raw IP address... (ip-host, +25)
Note: heuristic result only; it does not prove that a site is safe or malicious.
```

The exact score is produced by the current rule set.

## Python API

```python
from phishing_url_checker import analyze_url

report = analyze_url("https://example.com/account/verify")
print(report.risk, report.score)

for finding in report.findings:
    print(finding.code, finding.severity, finding.points)
```

The public API exposes typed dataclasses for reports and findings.

## Exit codes

| Code | Meaning |
|---:|---|
| `0` | Normal completion |
| `1` | Invalid input or file error |
| `2` | A report met the selected `--fail-on` threshold |

## Privacy boundary

During analysis the checker does **not** intentionally:

- perform DNS lookup;
- send HTTP/HTTPS requests;
- follow redirects;
- query certificate services;
- expand short URLs;
- contact reputation or threat-intelligence APIs;
- send telemetry.

That boundary is a core property of the project.

## Tests and CI

```bash
python -m pip install -e . pytest
python -m compileall -q src tests
python -m pytest -q
```

GitHub Actions runs compilation, tests, and a CLI smoke test across Ubuntu, Windows and macOS on Python 3.10, 3.12 and 3.13.

## What this project is not

It is not:

- a browser sandbox;
- an antivirus engine;
- a live reputation database;
- a certificate validator;
- a page-content scanner;
- a shortened-link expander;
- a guarantee that a URL is safe or malicious.

A well-crafted phishing URL can look structurally ordinary, and a legitimate URL can trigger heuristics. Important decisions should combine structural analysis with browser protections, organizational controls, domain/reputation intelligence and human verification.

## Repository map

```text
phishing-url-checker/
├── assets/                       visual identity
├── docs/
│   ├── ARCHITECTURE.md           rule and data-flow documentation
│   └── BRAND.md                  Threat Lens identity
├── examples/urls.txt             documentation-safe examples
├── src/phishing_url_checker/
│   ├── checker.py                validation + heuristic rules + scoring
│   ├── cli.py                    CLI + JSON + thresholds
│   ├── __init__.py               public Python API
│   └── __main__.py               python -m entry point
├── tests/test_checker.py
├── README_AR.md
├── README_EN.md
├── CHANGELOG.md
├── CONTRIBUTING.md
├── SECURITY.md
├── SUPPORT.md
└── LICENSE
```

## Project documents

| Resource | Purpose |
|---|---|
| [README_AR.md](README_AR.md) | الدليل العربي |
| [README_EN.md](README_EN.md) | Full English guide |
| [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) | Validation, rule flow and scoring model |
| [docs/BRAND.md](docs/BRAND.md) | Threat Lens visual system |
| [SECURITY.md](SECURITY.md) | Safe use and privacy boundary |
| [SUPPORT.md](SUPPORT.md) | Troubleshooting |
| [CONTRIBUTING.md](CONTRIBUTING.md) | Rule-design and contribution guidance |
| [CHANGELOG.md](CHANGELOG.md) | Notable repository changes |
| [LICENSE](LICENSE) | MIT License |

---

<div align="center">

### Built by رضوان عبدالهادي

**Radwan Abd alhady Ahmed · [@rad03i2](https://github.com/rad03i2)**

<sub>Inspect the structure. Explain the evidence. Keep the URL local.</sub>

</div>
