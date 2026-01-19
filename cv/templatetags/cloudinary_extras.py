from __future__ import annotations

from urllib.parse import urlparse

from django import template
from django.conf import settings


register = template.Library()


def _cloud_name() -> str | None:
    """Get cloud_name from CLOUDINARY_URL or from settings.CLOUDINARY_STORAGE."""
    url = getattr(settings, "CLOUDINARY_URL", None) or getattr(settings, "CLOUDINARY", None)
    if not url:
        url = getattr(settings, "CLOUDINARY_URL", None)
    env_url = getattr(settings, "CLOUDINARY_URL", None)
    url = env_url or getattr(settings, "CLOUDINARY_URL", None)
    # Try env first
    raw = env_url or getattr(settings, "CLOUDINARY_URL", None)
    if not raw:
        raw = getattr(settings, "CLOUDINARY_URL", None)
    # Actually parse from environment variable (preferred)
    raw = getattr(settings, "CLOUDINARY_URL", None) or settings.__dict__.get("CLOUDINARY_URL")
    if raw:
        try:
            parsed = urlparse(raw)
            # format: cloudinary://api_key:api_secret@cloud_name
            if parsed.hostname:
                return parsed.hostname
        except Exception:
            pass
    # Fallback: CLOUDINARY_STORAGE
    storage = getattr(settings, "CLOUDINARY_STORAGE", {})
    return storage.get("CLOUD_NAME")


def _base() -> str | None:
    cn = _cloud_name()
    if not cn:
        return None
    return f"https://res.cloudinary.com/{cn}/"


def _as_str(value) -> str:
    if value is None:
        return ""
    # CloudinaryResource has .public_id and .format sometimes; but it also stringifies.
    return str(value)


def _ensure_absolute(url_or_path: str) -> str:
    s = url_or_path.strip()
    if not s:
        return ""
    if s.startswith("http://") or s.startswith("https://"):
        return s
    base = _base()
    if not base:
        return s
    # Common stored forms:
    # - raw/upload/v123/folder/file.pdf
    # - image/upload/v123/folder/file.jpg
    # - video/upload/...
    return base + s.lstrip("/")


def _inject_attachment(url_or_path: str) -> str:
    """Cloudinary attachments are a transformation flag, not a query param."""
    s = url_or_path
    # Works for both absolute URLs and stored paths.
    for marker in ("/raw/upload/", "/image/upload/", "/video/upload/"):
        if marker in s and "/fl_attachment/" not in s:
            return s.replace(marker, marker.replace("/upload/", "/upload/fl_attachment/"))
    # If it was stored as 'raw/upload/...'
    for marker in ("raw/upload/", "image/upload/", "video/upload/"):
        if s.startswith(marker) and "fl_attachment" not in s:
            return s.replace("/upload/", "/upload/fl_attachment/", 1)
    # Fallback: do nothing
    return s


@register.filter
def cld_url(value) -> str:
    """Return a usable Cloudinary URL even if DB stored a relative path."""
    return _ensure_absolute(_as_str(value))


@register.filter
def cld_download_url(value) -> str:
    """Return a Cloudinary URL that forces download (attachment)."""
    abs_url = _ensure_absolute(_as_str(value))
    return _inject_attachment(abs_url)
