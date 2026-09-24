"""Phishing URL Checker public API."""
from .checker import Finding, Report, URLValidationError, analyze_url

__all__ = ["Finding", "Report", "URLValidationError", "analyze_url"]
__version__ = "1.0.0"
