"""Template filters that ask Cloudinary for right-sized, modern-format images.

Usage:
    {% load media_tags %}
    <img src="{{ item.image.url|cdn:900 }}">
    <img src="{{ hero.url|cdn:1600 }}" srcset="{{ hero.url|cdn_srcset:'640,1100,1600,2200' }}" sizes="100vw">

Non-Cloudinary URLs (local development, uploaded files on disk) pass through
unchanged, so the filters are always safe to use.
"""
from django import template

register = template.Library()

UPLOAD_SEGMENT = "/image/upload/"


def _transform(url, width):
    if not url or "res.cloudinary.com" not in url or UPLOAD_SEGMENT not in url:
        return url
    head, tail = url.split(UPLOAD_SEGMENT, 1)
    # Skip URLs that already carry a transformation (e.g. "w_800,c_fill/...").
    first = tail.split("/", 1)[0]
    if "," in first or first.startswith(("w_", "c_", "f_", "q_")):
        return url
    parts = ["f_auto", "q_auto"]
    if width:
        parts += ["c_limit", f"w_{int(width)}"]
    return f"{head}{UPLOAD_SEGMENT}{','.join(parts)}/{tail}"


@register.filter
def cdn(url, width=None):
    """Auto format + quality, and limit the width (never upscales)."""
    try:
        width = int(width) if width not in (None, "") else None
    except (TypeError, ValueError):
        width = None
    return _transform(str(url or ""), width)


@register.filter
def cdn_srcset(url, widths="640,1100,1600"):
    """A srcset string for the given comma-separated widths."""
    url = str(url or "")
    if "res.cloudinary.com" not in url:
        return ""
    entries = []
    for raw in str(widths).split(","):
        raw = raw.strip()
        if raw.isdigit():
            entries.append(f"{_transform(url, int(raw))} {raw}w")
    return ", ".join(entries)


def share_image_url(url):
    """A 1200×630 JPEG crop, the size link previews (iMessage, LinkedIn, email) expect."""
    if not url or "res.cloudinary.com" not in url or UPLOAD_SEGMENT not in url:
        return url
    head, tail = url.split(UPLOAD_SEGMENT, 1)
    return f"{head}{UPLOAD_SEGMENT}f_jpg,q_auto,c_fill,g_auto,w_1200,h_630/{tail}"


def default_share_image():
    from website.models import HomepageContent, MediaKitContent

    for model, field in ((HomepageContent, "hero_image"), (MediaKitContent, "hero_image")):
        content = model.objects.only(field).first()
        image = getattr(content, field, None) if content else None
        if image:
            try:
                return image.url
            except ValueError:
                continue
    return ""

