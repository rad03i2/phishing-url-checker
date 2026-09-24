# Phishing URL Checker

Offline, explainable URL risk analysis for developers, students, support teams, and security-aware users. The tool inspects the **text structure** of HTTP(S) URLs and reports common phishing indicators without opening the site or sending the URL to a third party.

> A heuristic score is not a verdict. A low score does not prove a site is safe, and a high score does not prove malicious intent.

## Why this project exists

Many URL checkers require submitting a potentially private link to an online service. This project provides a small local first-pass inspection tool that is deterministic, scriptable, transparent, and suitable for CI or support workflows.

## Features

- Offline analysis: no DNS lookup, HTTP request, telemetry, API key, or cloud service.
- Detects raw IP hosts, URL user-info deception, Punycode, deep subdomains, known shorteners, unusual ports, long URLs, heavily hyphenated hosts, selected high-abuse TLD signals, credential-oriented path/query language, and URL-like redirect parameters.
- Weighted `0..100` score with `minimal`, `low`, `medium`, and `high` risk bands.
- Every score contribution is returned as an explainable finding with code, severity, points, and message.
- Batch analysis from command arguments or a UTF-8 text file.
- Human-readable and JSON output plus CI-friendly `--fail-on` thresholds.
- Public Python API with typed dataclasses.
- Arabic/Unicode-safe input and JSON output.
- Zero runtime dependencies.

## Preview

```text
$ phishcheck "http://user@192.0.2.1/login/verify"
URL: http://user@192.0.2.1/login/verify
Host: 192.0.2.1
Risk: HIGH (.../100)
Findings:
  - [MEDIUM] Connection is not protected by HTTPS. (plain-http, +15)
  - [HIGH] URL contains user-info before the hostname... (userinfo, +30)
  - [HIGH] Hostname is a raw IP address... (ip-host, +25)
```

The exact score is calculated from the current rule set; use finding codes rather than parsing prose in automation.

## Requirements and installation

Python 3.10 or newer.

```bash
git clone https://github.com/rad03i2/phishing-url-checker.git
cd phishing-url-checker
python -m pip install -e .
```

For development/testing:

```bash
python -m pip install -e . pytest
```

## Usage

```bash
phishcheck https://example.com
phishcheck "http://user@192.0.2.1/login/verify"
phishcheck --file examples/urls.txt
phishcheck https://example.com --json
phishcheck suspicious-url-here --fail-on high
python -m phishing_url_checker https://example.com
```

`--fail-on medium` or `--fail-on high` returns exit code `2` when any analyzed URL reaches that threshold. Invalid input/file errors return `1`; normal completion returns `0`.

### Python API

```python
from phishing_url_checker import analyze_url

report = analyze_url("https://example.com/account/verify")
print(report.risk, report.score)
for finding in report.findings:
    print(finding.code, finding.message)
```

## Configuration

No environment variables, accounts, secrets, or configuration files are required. Detection rules are intentionally visible in `src/phishing_url_checker/checker.py` so users can audit how a score is produced.

## Project structure

```text
src/phishing_url_checker/
  checker.py       # validation, rules, score, report models
  cli.py           # CLI, batch/JSON output, exit codes
  __init__.py      # public API
  __main__.py      # python -m support
tests/test_checker.py
examples/urls.txt
.github/workflows/ci.yml
```

## Testing

```bash
python -m compileall -q src tests
python -m pytest -q
```

GitHub Actions runs compilation, tests, and a CLI smoke test on Ubuntu, Windows, and macOS with Python 3.10, 3.12, and 3.13.

## Security and privacy

Submitted URLs stay local. The checker never visits a URL, resolves its hostname, downloads content, or queries a reputation service. This prevents the checker itself from contacting an untrusted destination and avoids disclosing private links to a remote provider. See `SECURITY.md`.

## Limitations

This is a **lexical/structural heuristic checker**, not a browser sandbox, antivirus engine, reputation database, certificate validator, page-content scanner, or guarantee of safety. New or carefully crafted phishing URLs can look structurally normal. Legitimate URLs can trigger warnings. Shortened links cannot be expanded offline. Internationalized domains require human context even when Punycode is highlighted. For important decisions, combine this result with browser protections, organizational security controls, domain/reputation intelligence, and human verification.

## Optional roadmap

Future work may add user-supplied allow/block lists and pluggable, explicitly opt-in reputation providers while preserving the default offline mode.

## Contributing

See `CONTRIBUTING.md`. Please include tests for new rules and explain false-positive tradeoffs.

## License

MIT — see `LICENSE`.

## Author

**Radwan Abdulhadi Ahmed**  
**رضوان عبدالهادي أحمد**  
GitHub: **@rad03i2**

---

# العربية | مدقق روابط التصيد

أداة محلية وقابلة للتفسير لتحليل مؤشرات الخطورة في روابط HTTP وHTTPS. تفحص **بنية نص الرابط فقط** وتعرض إشارات شائعة مرتبطة بروابط التصيد، من دون فتح الموقع أو إرسال الرابط إلى أي خدمة خارجية.

> النتيجة تقدير إرشادي وليست حكمًا نهائيًا. النتيجة المنخفضة لا تثبت أن الموقع آمن، والنتيجة المرتفعة لا تثبت وحدها أنه خبيث.

## لماذا هذا المشروع؟

تتطلب أدوات كثيرة إرسال الرابط إلى خدمة عبر الإنترنت، وقد يكون الرابط خاصًا. يوفر هذا المشروع فحصًا أوليًا صغيرًا يعمل محليًا، ونتيجته حتمية وقابلة للأتمتة، كما أن قواعده واضحة ويمكن مراجعتها.

## الميزات

- يعمل دون DNS أو طلبات HTTP أو تتبع أو مفاتيح API أو خدمات سحابية.
- يكشف استخدام عنوان IP بدل النطاق، وبيانات المستخدم داخل الرابط، وPunycode، وكثرة النطاقات الفرعية، ومختصرات الروابط المعروفة، والمنافذ غير المعتادة، والروابط الطويلة، وكثرة الشرطات، وبعض إشارات TLD، وكلمات الحساب/تسجيل الدخول في المسار أو الاستعلام، ومعاملات إعادة التوجيه التي تحتوي روابط.
- درجة موزونة من 0 إلى 100 مع مستويات: أدنى، منخفض، متوسط، مرتفع.
- كل سبب يظهر بكود ومستوى ونقاط ورسالة تفسيرية.
- فحص عدة روابط من سطر الأوامر أو ملف UTF-8.
- مخرجات نصية أو JSON وخيار `--fail-on` المناسب لـCI.
- Python API باستخدام dataclasses.
- يدعم العربية وUnicode في الإدخال وJSON.
- بلا اعتماديات تشغيل خارجية.

## التثبيت

يتطلب Python 3.10 أو أحدث:

```bash
git clone https://github.com/rad03i2/phishing-url-checker.git
cd phishing-url-checker
python -m pip install -e .
```

للتطوير والاختبار:

```bash
python -m pip install -e . pytest
```

## الاستخدام

```bash
phishcheck https://example.com
phishcheck "http://user@192.0.2.1/login/verify"
phishcheck --file examples/urls.txt
phishcheck https://example.com --json
python -m phishing_url_checker https://example.com
```

يعيد `--fail-on medium` أو `--fail-on high` رمز الخروج `2` عند بلوغ الحد، بينما أخطاء الإدخال تعيد `1` والنجاح الطبيعي يعيد `0`.

### Python API

```python
from phishing_url_checker import analyze_url

report = analyze_url("https://example.com/account/verify")
print(report.risk, report.score)
```

## الإعداد

لا يحتاج المشروع متغيرات بيئة أو حسابات أو أسرارًا. توجد قواعد الكشف بصورة واضحة في `src/phishing_url_checker/checker.py` ويمكن مراجعة طريقة حساب النتيجة مباشرة.

## بنية المشروع

- `src/phishing_url_checker/`: محرك التحليل وCLI وواجهة Python.
- `tests/`: اختبارات الوظائف وسطر الأوامر.
- `examples/urls.txt`: روابط آمنة مخصصة للتجربة والتوثيق.
- `.github/workflows/ci.yml`: فحص متعدد الأنظمة وإصدارات Python.

## الاختبارات

```bash
python -m compileall -q src tests
python -m pytest -q
```

يشغل GitHub Actions الاختبارات على Ubuntu وWindows وmacOS مع Python 3.10 و3.12 و3.13.

## الأمان والخصوصية

لا يزور البرنامج الروابط ولا يحل أسماء النطاقات ولا ينزل محتوى ولا يستعلم من قواعد سمعة خارجية. لذلك يبقى الرابط محليًا ولا يتسبب الفحص نفسه في اتصال بوجهة غير موثوقة. راجع `SECURITY.md`.

## القيود

هذه أداة تحليل بنيوي/لفظي وليست sandbox للمتصفح أو مضاد فيروسات أو قاعدة سمعة أو مدقق شهادات أو ماسح محتوى صفحات. قد يبدو رابط تصيد متقن طبيعيًا، وقد تُظهر روابط سليمة تحذيرات. ولا يمكن كشف الوجهة النهائية للرابط المختصر دون اتصال بالشبكة. عند القرارات المهمة استخدم وسائل حماية إضافية وتحققًا بشريًا.

## التطوير المستقبلي الاختياري

يمكن مستقبلًا إضافة قوائم سماح/حظر يقدمها المستخدم ومزودي سمعة اختياريين مع الحفاظ على الوضع المحلي كخيار افتراضي.

## المساهمة

راجع `CONTRIBUTING.md`. يجب إضافة اختبارات للقواعد الجديدة وشرح احتمالات النتائج الإيجابية الكاذبة.

## الترخيص

MIT — راجع `LICENSE`.

## المؤلف

**Radwan Abdulhadi Ahmed**  
**رضوان عبدالهادي أحمد**  
GitHub: **@rad03i2**
