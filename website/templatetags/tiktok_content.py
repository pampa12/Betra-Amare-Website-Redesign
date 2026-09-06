from django import template

from website.featured_tiktok import FeaturedTikTok


register = template.Library()


@register.inclusion_tag("includes/featured_tiktoks.html")
def featured_tiktok_showcase(limit=4):
    """Render up to four active TikTok posts on the media kit."""
    return {
        "featured_tiktoks": FeaturedTikTok.objects.filter(active=True)[:limit],
    }
