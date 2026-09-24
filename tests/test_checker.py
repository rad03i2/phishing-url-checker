import json
from phishing_url_checker import URLValidationError, analyze_url
from phishing_url_checker.cli import main


def test_clean_https_is_minimal():
    report = analyze_url("https://example.com/docs")
    assert report.risk == "minimal"
    assert report.score == 0
    assert report.hostname == "example.com"


def test_combined_indicators_raise_high_risk():
    report = analyze_url("http://user@example-login-secure-update.top:8080/account/verify?next=https://other.test")
    codes = {f.code for f in report.findings}
    assert report.risk == "high"
    assert {"plain-http", "userinfo", "watch-tld", "unusual-port", "credential-language", "external-redirect"} <= codes


def test_ip_and_punycode_detection():
    assert "ip-host" in {f.code for f in analyze_url("https://192.0.2.1/login").findings}
    assert "punycode" in {f.code for f in analyze_url("https://xn--e1afmkfd.xn--p1ai/").findings}


def test_invalid_schemes_rejected():
    for value in ("javascript:alert(1)", "ftp://example.com", "example.com"):
        try:
            analyze_url(value)
        except URLValidationError:
            pass
        else:
            raise AssertionError(value)


def test_unicode_path_and_serialization():
    report = analyze_url("https://example.com/مرحبا")
    payload = json.dumps(report.to_dict(), ensure_ascii=False)
    assert "مرحبا" in payload


def test_cli_json_and_threshold(capsys):
    assert main(["https://example.com", "--json"]) == 0
    assert json.loads(capsys.readouterr().out)[0]["risk"] == "minimal"
    assert main(["http://user@192.0.2.1/login/verify", "--fail-on", "medium"]) == 2
