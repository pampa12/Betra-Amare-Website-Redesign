from django import template

from website.featured_tiktok import FeaturedTikTok
from website.models import PortfolioItem


register = template.Library()


@register.inclusion_tag("includes/featured_tiktoks.html")
def featured_tiktok_showcase(limit=4):
    """Render active TikTok posts on the media kit."""
    return {
        "featured_tiktoks": FeaturedTikTok.objects.filter(active=True)[:limit],
    }


@register.inclusion_tag("includes/homepage_selected_work.html")
def homepage_selected_work():
    """Render the photos, video and TikToks selected for the homepage as one row.

    Everything shares the same height, so a tall TikTok sits next to the photos
    instead of on a line of its own. TikToks are spread between the photos.
    """
    items = list(
        PortfolioItem.objects.filter(active=True, featured=True).order_by(
            "sort_order", "-created_at"
        )
    )
    video_item = next((item for item in items if item.video and item.image), None)
    photos = [item for item in items if item.image and not item.video][:4]
    tiktoks = list(
        FeaturedTikTok.objects.filter(active=True, show_on_homepage=True)
        .exclude(thumbnail="")[:2]
    )

    vertical = [("video", video_item)] if video_item else []
    vertical += [("tiktok", tiktok) for tiktok in tiktoks]

    strip = []
    photo_cards = [("photo", photo) for photo in photos]
    # photo, tall, photo, tall, photo... then whatever is left over.
    while photo_cards or vertical:
        if photo_cards:
            strip.append(photo_cards.pop(0))
        if vertical:
            strip.append(vertical.pop(0))

    # Width of the whole row measured in "row heights", used to size the row
    # so it always fits on one line on desktop.
    ratio = sum(0.8 if kind == "photo" else 0.5625 for kind, _ in strip)
    return {
        "strip": [{"kind": kind, "item": item} for kind, item in strip],
        "strip_ratio": f"{ratio:.4f}",
        "strip_gaps": max(len(strip) - 1, 0),
    }


@register.inclusion_tag("includes/homepage_tiktok_favorites.html")
def homepage_tiktok_favorites(limit=2):
    """Legacy helper retained for compatibility with older templates."""
    return {
        "homepage_tiktoks": FeaturedTikTok.objects.filter(
            active=True,
            show_on_homepage=True,
        ).exclude(thumbnail="")[:limit],
    }
