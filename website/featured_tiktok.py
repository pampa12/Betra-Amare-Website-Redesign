import re
from urllib.parse import urlparse

from django.core.exceptions import ValidationError
from django.db import models


TIKTOK_VIDEO_PATH = re.compile(r"/video/(\d+)")


def _tiktok_video_id(url):
    """Return the numeric TikTok video id from a full public TikTok video URL."""
    if not url:
        return ""

    parsed = urlparse(url)
    hostname = (parsed.hostname or "").lower()
    if hostname != "tiktok.com" and not hostname.endswith(".tiktok.com"):
        return ""

    match = TIKTOK_VIDEO_PATH.search(parsed.path)
    return match.group(1) if match else ""


class FeaturedTikTok(models.Model):
    """A public TikTok post featured on Betra's website."""

    title = models.CharField(max_length=140)
    brand_name = models.CharField(
        max_length=120,
        blank=True,
        default="",
        help_text="Optional. Add the brand name only when it accurately describes this post.",
    )
    tiktok_url = models.URLField(
        help_text=(
            "Paste the full public TikTok video URL, for example "
            "https://www.tiktok.com/@username/video/1234567890"
        )
    )
    thumbnail = models.ImageField(
        upload_to="featured-tiktoks/thumbnails/",
        blank=True,
        help_text=(
            "Upload a clean still frame for the homepage card. The Media Kit can still use the live TikTok player."
        ),
    )
    description = models.TextField(
        blank=True,
        default="",
        help_text="Optional short note about the concept, product, or deliverable.",
    )
    active = models.BooleanField(default=True)
    show_on_homepage = models.BooleanField(
        default=False,
        help_text="Show this TikTok as a clean thumbnail card inside the homepage 'A few favorites' section.",
    )
    sort_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["sort_order", "-created_at"]
        verbose_name = "Featured TikTok"
        verbose_name_plural = "Featured TikToks"

    def clean(self):
        super().clean()
        errors = {}

        if self.tiktok_url and not _tiktok_video_id(self.tiktok_url):
            errors["tiktok_url"] = (
                "Paste the full public TikTok video URL that contains /video/ and the video number. "
                "TikTok short share links cannot be embedded automatically."
            )

        if self.show_on_homepage and not self.thumbnail:
            errors["thumbnail"] = (
                "Upload a thumbnail before showing this TikTok on the homepage."
            )

        if errors:
            raise ValidationError(errors)

    @property
    def video_id(self):
        return _tiktok_video_id(self.tiktok_url)

    @property
    def embed_url(self):
        video_id = self.video_id
        if not video_id:
            return ""
        return (
            f"https://www.tiktok.com/player/v1/{video_id}"
            "?autoplay=0&loop=1&music_info=1&description=0"
        )

    def __str__(self):
        return self.title
