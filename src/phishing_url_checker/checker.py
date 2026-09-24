"""Explainable, offline URL risk analysis."""
from __future__ import annotations

from dataclasses import asdict, dataclass
import ipaddress
import re
from urllib.parse import parse_qsl, unquote, urlsplit

SUSPICIOUS_WORDS = {"login", "signin", "verify", "verification", "secure", "account", "update", "password", "wallet", "confirm", "banking"}
SHORTENERS = {"bit.ly", "tinyurl.com", "t.co", "is.gd", "cutt.ly", "rb.gy", "rebrand.ly", "shorturl.at"}
RISKY_TLDS = {"zip", "mov", "top", "click", "work", "support"}
REDIRECT_KEYS = {"url", "uri", "redirect", "redirect_url", "redirect_uri", "next", "target", "dest", "destination", "continue", "return"}

@dataclass(frozen=True)
class Finding:
    code: str
    severity: str
    points: int
    message: str

@dataclass(frozen=True)
class Report:
    input: str
    normalized_url: str
    hostname: str
    score: int
    risk: str
    findings: tuple[Finding, ...]

    def to_dict(self) -> dict:
        data = asdict(self)
        data["findings"] = [asdict(item) for item in self.findings]
        return data

class URLValidationError(ValueError):
    pass

def _add(findings: list[Finding], code: str, severity: str, points: int, message: str) -> None:
    findings.append(Finding(code, severity, points, message))

def analyze_url(raw: str) -> Report:
    """Analyze a single HTTP(S) URL without making any network request."""
    value = raw.strip()
    if not value:
        raise URLValidationError("URL cannot be empty")
    if any(ord(ch) < 32 for ch in value):
        raise URLValidationError("URL contains control characters")
    parsed = urlsplit(value)
    if parsed.scheme.lower() not in {"http", "https"}:
        raise URLValidationError("only http:// and https:// URLs are supported")
    if not parsed.hostname:
        raise URLValidationError("URL must include a hostname")
    try:
        port = parsed.port
    except ValueError as exc:
        raise URLValidationError("invalid port") from exc

    host = parsed.hostname.rstrip(".").lower()
    if len(host) > 253:
        raise URLValidationError("hostname is too long")
    findings: list[Finding] = []

    if parsed.scheme.lower() == "http":
        _add(findings, "plain-http", "medium", 15, "Connection is not protected by HTTPS.")
    if parsed.username is not None or parsed.password is not None:
        _add(findings, "userinfo", "high", 30, "URL contains user-info before the hostname, a common visual-deception pattern.")
    try:
        ipaddress.ip_address(host.strip("[]"))
        _add(findings, "ip-host", "high", 25, "Hostname is a raw IP address rather than a domain name.")
    except ValueError:
        pass
    if host.startswith("xn--") or ".xn--" in host:
        _add(findings, "punycode", "medium", 20, "Hostname contains Punycode; verify the intended Unicode domain carefully.")
    labels = host.split(".")
    if len(labels) >= 5:
        _add(findings, "many-subdomains", "low", 8, "Hostname has an unusually deep subdomain chain.")
    if host in SHORTENERS or any(host.endswith("." + item) for item in SHORTENERS):
        _add(findings, "shortener", "medium", 18, "Known URL-shortening domain hides the final destination.")
    if labels and labels[-1] in RISKY_TLDS:
        _add(findings, "watch-tld", "low", 6, "Top-level domain is frequently abused; this alone does not make the URL malicious.")
    if port is not None and port not in {80, 443}:
        _add(findings, "unusual-port", "low", 5, "URL uses a non-standard web port.")
    if len(value) > 180:
        _add(findings, "long-url", "low", 7, "URL is unusually long and may obscure its destination.")
    if host.count("-") >= 3:
        _add(findings, "hyphenated-host", "low", 5, "Hostname contains many hyphens.")

    decoded_path = unquote(parsed.path).lower()
    tokens = set(re.findall(r"[a-z]+", decoded_path + " " + parsed.query.lower()))
    hits = sorted(tokens & SUSPICIOUS_WORDS)
    if len(hits) >= 2:
        _add(findings, "credential-language", "medium", 12, "Path/query contains multiple credential or account-related terms: " + ", ".join(hits[:5]) + ".")
    for key, target in parse_qsl(parsed.query, keep_blank_values=True):
        if key.lower() in REDIRECT_KEYS and re.match(r"(?i)^https?%?3a|^https?://", target):
            _add(findings, "external-redirect", "medium", 12, "Query contains a URL-like redirect destination.")
            break
    if "%40" in parsed.netloc.lower() or "%2f" in parsed.netloc.lower():
        _add(findings, "encoded-authority", "high", 20, "Authority contains encoded delimiter characters.")

    score = min(100, sum(item.points for item in findings))
    risk = "high" if score >= 50 else "medium" if score >= 25 else "low" if score > 0 else "minimal"
    normalized = parsed.geturl()
    return Report(value, normalized, host, score, risk, tuple(findings))
