from django import template

from website.featured_tiktok import FeaturedTikTok


register = template.Library()


@register.inclusion_tag("includes/featured_tiktoks.html")
def featured_tiktok_showcase(limit=4):
    """Render active TikTok posts on the media kit."""
    return {
        "featured_tiktoks": FeaturedTikTok.objects.filter(active=True)[:limit],
    }


@register.inclusion_tag("includes/homepage_tiktok_favorites.html")
def homepage_tiktok_favorites(limit=2):
    """Render up to two TikTok posts selected for the homepage favorites area."""
    return {
        "homepage_tiktoks": FeaturedTikTok.objects.filter(
            active=True,
            show_on_homepage=True,
        )[:limit],
    }
