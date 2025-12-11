EMAIL_RE = re.compile(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+")
PHONE_RE = re.compile(r"\b(?:\+91|0)?[6-9]\d{9}\b")


def redact_pii(text: str) -> str:
text = EMAIL_RE.sub("[REDACTED_EMAIL]", text)
text = PHONE_RE.sub("[REDACTED_PHONE]", text)
return text