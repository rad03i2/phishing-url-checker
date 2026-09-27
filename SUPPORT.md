# Phishing URL Checker Support

## Start here

```bash
python --version
phishcheck --version
phishcheck https://example.com
```

For a development checkout:

```bash
python -m pip install -e . pytest
python -m compileall -q src tests
python -m pytest -q
```

## Common questions

### Why did a legitimate URL receive findings?

The rules are heuristics. Structural patterns such as long URLs, unusual ports, Punycode or account-related words can occur in legitimate systems. Review the individual finding codes rather than treating the total as a verdict.

### Why did a suspicious URL receive a low score?

The tool only sees the URL text. It does not inspect page content, reputation, DNS history, certificates or destination behavior. A carefully designed malicious URL can look structurally ordinary.

### Why does a shortened link not reveal its final destination?

Expanding it would require a network request. The current project's privacy boundary deliberately avoids visiting or resolving submitted URLs.

### Why is my URL rejected?

The current analyzer accepts only URLs with explicit `http://` or `https://`, a hostname, valid port syntax and no control characters.

### Should automation parse the text output?

Prefer `--json` and finding codes. Human-readable wording may evolve while rule codes are the safer integration anchor.

## Bug reports

Include:

- Python version;
- operating system;
- sanitized example URL when safe;
- expected behavior;
- actual finding codes / score;
- whether the problem concerns validation, scoring, CLI output or serialization.

Do not publish private reset links, session-bearing URLs, access tokens, credentials or customer-specific links in public issues.

## Security reports

Follow [SECURITY.md](SECURITY.md) and use private vulnerability reporting when available.

---

## الدعم بالعربية

إذا ظهرت نتيجة غير متوقعة، راجع أسباب النتيجة الفردية أولًا بدل الاعتماد على الرقم النهائي وحده. الأداة لا تفحص محتوى الموقع ولا السمعة ولا DNS.

لا تنشر روابط خاصة تحتوي Tokens أو روابط استعادة كلمة المرور أو روابط عملاء داخل Issues العامة.
