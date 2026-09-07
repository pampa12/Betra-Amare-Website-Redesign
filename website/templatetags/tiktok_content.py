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
    """Render only the portfolio media explicitly selected for the homepage."""
    items = list(
        PortfolioItem.objects.filter(active=True, featured=True).order_by(
            "sort_order", "-created_at"
        )
    )

    video_item = next(
        (item for item in items if item.video and item.image),
        None,
    )

    photo_items = [
        item
        for item in items
        if item.image and not item.video
    ][:4]

    top_photos = photo_items[:3]
    bottom_photo = photo_items[3] if len(photo_items) > 3 else None

    homepage_tiktoks = list(
        FeaturedTikTok.objects.filter(
            active=True,
            show_on_homepage=True,
        )
        .exclude(thumbnail="")[:2]
    )

    bottom_count = (1 if video_item else 0) + len(homepage_tiktoks) + (
        1 if bottom_photo else 0
    )

    return {
        "top_photos": top_photos,
        "video_item": video_item,
        "homepage_tiktoks": homepage_tiktoks,
        "bottom_photo": bottom_photo,
        "bottom_count": bottom_count,
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
