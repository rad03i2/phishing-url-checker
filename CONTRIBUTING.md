# Contributing

Contributions are welcome when they keep the checker explainable, privacy-preserving, and safe by default.

1. Fork the repository and create a focused branch.
2. Use Python 3.10+ and install with `python -m pip install -e . pytest`.
3. Add or update tests for behavioral changes.
4. Run `python -m compileall -q src tests` and `python -m pytest -q`.
5. Keep new detection rules deterministic and document false-positive tradeoffs.
6. Open a pull request describing the problem, approach, and validation performed.

Do not add automatic navigation to submitted URLs, telemetry, secret material, or remote reputation services without an explicit privacy-preserving design discussion.
