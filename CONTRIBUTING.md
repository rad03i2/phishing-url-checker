# Contributing to Phishing URL Checker

Contributions are welcome when they keep the checker explainable, privacy-preserving and deterministic.

## Development setup

```bash
git clone https://github.com/rad03i2/phishing-url-checker.git
cd phishing-url-checker
python -m pip install -e . pytest
```

## Quality checks

```bash
python -m compileall -q src tests
python -m pytest -q
phishcheck https://example.com
```

## Adding or changing a rule

A rule change should:

1. identify a structural signal available from the URL text;
2. use a stable, descriptive finding code;
3. expose an explicit point contribution;
4. explain why the signal matters without declaring malicious intent;
5. consider legitimate uses and false positives;
6. include focused tests;
7. preserve the no-network analysis boundary unless a separately reviewed opt-in design explicitly changes scope.

## Privacy

Never commit or paste private URLs containing credentials, reset tokens, session identifiers, customer data or private infrastructure details. Use documentation-safe domains and reserved example IP ranges.

## Pull requests

Describe the rule or behavior changed, the false-positive tradeoff, tests performed and whether public JSON/CLI behavior changed.

---

**Radwan Abd alhady Ahmed — رضوان عبدالهادي — [@rad03i2](https://github.com/rad03i2)**
