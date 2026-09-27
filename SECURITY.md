# Security Policy

Phishing URL Checker is a local heuristic analyzer. It should not be treated as a browser sandbox, malware scanner, live threat-intelligence system or guarantee of URL safety.

## Analysis boundary

The current analyzer does not intentionally:

- resolve submitted hostnames;
- make HTTP or HTTPS requests;
- follow redirects;
- download page content;
- fetch certificates;
- expand shortened links;
- query reputation services;
- send telemetry.

This boundary is intentional: inspecting an untrusted URL should not make the checker itself contact that destination or disclose a private link to a third party.

## Safe interpretation

A `minimal` or `low` report is not proof of safety. A `medium` or `high` report is not proof of malicious intent.

Use the result as one signal among browser protections, organization policy, reputation/domain intelligence and human verification.

## Sensitive URLs

URLs can contain reset tokens, session IDs, access tokens, customer identifiers and private hostnames. Do not paste sensitive URLs into public GitHub issues or test fixtures.

Use sanitized examples such as `example.com`, `example.net`, `example.org` and documentation/reserved address ranges.

## Reporting a vulnerability

Use GitHub private vulnerability reporting when available. Do not publish working exploit details, private URLs, credentials, tokens or personal data in a public issue.

Relevant reports include unexpected network activity introduced by the project, unsafe handling of input/output, sensitive-data exposure caused by the application, or a parsing behavior that creates a security-relevant failure.

## Supported version

Security fixes target the current default branch.
