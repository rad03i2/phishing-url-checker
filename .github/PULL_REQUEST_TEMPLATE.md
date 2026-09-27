# Phishing URL Checker pull request

## Summary
<!-- What changed and why? -->

## Area
- [ ] Validation
- [ ] Heuristic rule / scoring
- [ ] CLI / JSON
- [ ] Python API
- [ ] Tests / CI
- [ ] Security / privacy
- [ ] Documentation / identity

## Rule changes
<!-- If a rule changed, describe its signal, finding code, points and false-positive tradeoff. -->

## Verification
- [ ] I ran `python -m compileall -q src tests`.
- [ ] I ran `python -m pytest -q`.
- [ ] I ran a relevant `phishcheck` smoke test.
- [ ] I used sanitized/documentation-safe URLs in tests and examples.
- [ ] I did not include private URLs, credentials, reset tokens or customer data.
- [ ] I preserved the no-network boundary unless the PR explicitly proposes and documents a reviewed opt-in scope change.
- [ ] I did not describe a heuristic score as proof that a URL is safe or malicious.
