# Phishing URL Checker Architecture

The project intentionally has a small architecture so the full risk decision remains inspectable.

## Data flow

```text
raw string
   │
   ▼
URL validation
   │
   ├── scheme must be http/https
   ├── hostname required
   ├── control characters rejected
   ├── invalid port rejected
   └── hostname length checked
   │
   ▼
structural parsing with urllib.parse
   │
   ▼
independent heuristic rules
   │
   ├── scheme / user-info / host
   ├── Punycode / subdomain depth / TLD
   ├── port / length / hyphens
   ├── path + query language
   ├── redirect-like parameters
   └── encoded authority delimiters
   │
   ▼
Finding(code, severity, points, message)
   │
   ▼
score = min(100, sum(points))
   │
   ▼
risk band + Report
```

## Core module

`src/phishing_url_checker/checker.py` contains:

- `Finding` — one explainable signal;
- `Report` — normalized output model;
- `URLValidationError` — controlled invalid-input error;
- `analyze_url()` — validation, rule evaluation and scoring.

The module uses Python's standard library and intentionally makes no network request.

## CLI layer

`src/phishing_url_checker/cli.py` handles:

- one or more URL arguments;
- UTF-8 file input;
- text rendering;
- JSON serialization;
- `--fail-on medium|high`;
- exit codes;
- version output.

## Current score bands

```text
score == 0      minimal
score 1..24     low
score 25..49    medium
score 50..100   high
```

The final score is capped at 100.

## Explainability contract

A finding contains:

- a stable rule `code`;
- a severity label;
- explicit point contribution;
- a human-readable message.

Automation should rely on JSON fields and finding codes instead of parsing prose.

## Privacy boundary

The current analyzer does not intentionally perform:

- DNS resolution;
- HTTP requests;
- redirect following;
- certificate retrieval;
- reputation queries;
- short-link expansion;
- telemetry.

This means the analyzer can only reason about information already present in the URL text.

## Rule-design principle

A new rule should be deterministic, explainable and supported by tests. Its false-positive tradeoff should be documented. Rules should not imply certainty about malicious intent.

## Security boundary

Because the application does not visit submitted links, it avoids contacting an untrusted destination during analysis. This does not make a low-risk report a proof of safety.

## Test coverage

The current tests cover:

- minimal-risk HTTPS;
- combinations that raise high risk;
- IP and Punycode detection;
- rejection of unsupported schemes;
- Unicode serialization;
- JSON CLI output and threshold exit behavior.
