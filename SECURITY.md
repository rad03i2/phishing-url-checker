# Security Policy

## Scope
Phishing URL Checker performs **offline heuristic analysis only**. It does not open, fetch, resolve, or contact submitted URLs. This is intentional: checking an untrusted URL should not create network traffic to that destination.

## Reporting
Please report suspected security problems through GitHub's private vulnerability reporting feature when available. Do not publish secrets, private URLs, credentials, or personal data in public issues.

## Safe use
A `minimal` or `low` result is not a guarantee of safety, and a `high` result is not proof of malicious intent. Treat the score as one input to a broader security decision. Never enter credentials merely because this tool reports a low score.

## Supported version
The latest release on the default branch is supported.
