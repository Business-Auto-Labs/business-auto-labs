"""Local, dependency-free normalization helpers for lead matching."""
from __future__ import annotations

import hashlib
import re
import unicodedata
from urllib.parse import urlsplit, urlunsplit


_WHITESPACE = re.compile(r"\s+")
_NON_WORD = re.compile(r"[^\w]+", re.UNICODE)


def normalize_business_name(value: str | None) -> str:
    if not value:
        return ""
    folded = unicodedata.normalize("NFKC", value).casefold()
    return _WHITESPACE.sub(" ", _NON_WORD.sub(" ", folded)).strip()


def normalize_url(value: str | None) -> str | None:
    if not value or not value.strip():
        return None
    raw = value.strip()
    if "://" not in raw:
        raw = "https://" + raw
    try:
        parsed = urlsplit(raw)
        host = (parsed.hostname or "").casefold().rstrip(".")
        port = parsed.port
    except ValueError:
        return None
    if host.startswith("www."):
        host = host[4:]
    if not host:
        return None
    netloc = host if port is None else f"{host}:{port}"
    path = parsed.path.rstrip("/")
    return urlunsplit(((parsed.scheme or "https").casefold(), netloc, path, parsed.query, ""))


def normalize_contact_value(contact_type: str, value: str | None) -> str:
    if not value:
        return ""
    raw = unicodedata.normalize("NFKC", value).strip()
    kind = contact_type.casefold()
    if kind == "email":
        return raw.casefold()
    if kind == "phone":
        digits = re.sub(r"\D", "", raw)
        return ("+" if raw.startswith("+") else "") + digits
    if kind in {"website", "url"}:
        return normalize_url(raw) or raw.casefold()
    return _WHITESPACE.sub(" ", raw).casefold()


def make_dedupe_key(
    business_name: str,
    country_id: int,
    region_id: int | None,
    city_id: int | None,
    website: str | None = None,
    public_phone: str | None = None,
    public_email: str | None = None,
) -> str:
    name = normalize_business_name(business_name)
    site = normalize_url(website)
    if site:
        identity = f"website:{urlsplit(site).netloc}"
    elif public_email:
        identity = f"email:{normalize_contact_value('email', public_email)}"
    elif public_phone:
        identity = f"phone:{normalize_contact_value('phone', public_phone)}"
    else:
        identity = "name-and-location"
    raw = "|".join(
        (name, str(country_id), str(region_id or ""), str(city_id or ""), identity)
    )
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()
