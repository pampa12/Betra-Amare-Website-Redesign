import re
from urllib.error import URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen

from django.core.exceptions import ValidationError
from django.db import models


TIKTOK_VIDEO_PATH = re.compile(r"/video/(\d+)")
INSTAGRAM_REEL_PATH = re.compile(r"^/(?:reel|reels|p)/([A-Za-z0-9_-]+)")
TIKTOK_SHORT_HOSTS = ("vm.tiktok.com", "vt.tiktok.com")


def _hostname(url):
    return (urlparse(url).hostname or "").lower()


def _is_host(url, domain):
    host = _hostname(url)
    return host == domain or host.endswith("." + domain)


def _tiktok_video_id(url):
    """Return the numeric TikTok video id from a full public TikTok video URL."""
    if not url or not _is_host(url, "tiktok.com"):
        return ""
    match = TIKTOK_VIDEO_PATH.search(urlparse(url).path)
    return match.group(1) if match else ""


def _instagram_reel_code(url):
    """Return the shortcode from a public Instagram Reel or post URL."""
    if not url or not _is_host(url, "instagram.com"):
        return ""
    match = INSTAGRAM_REEL_PATH.search(urlparse(url).path)
    return match.group(1) if match else ""


def _is_tiktok_short_link(url):
    if not url:
        return False
    host = _hostname(url)
    path = urlparse(url).path
    return host in TIKTOK_SHORT_HOSTS or (_is_host(url, "tiktok.com") and path.startswith("/t/"))


def resolve_tiktok_short_link(url, timeout=8):
    """Follow a TikTok share link (tiktok.com/t/..., vm.tiktok.com/...) to the full video URL."""
    request = Request(url, method="HEAD", headers={"User-Agent": "Mozilla/5.0"})
    with urlopen(request, timeout=timeout) as response:
        final = response.geturl()
    video_id = _tiktok_video_id(final)
    if not video_id:
        return ""
    parsed = urlparse(final)
    return f"https://www.tiktok.com{parsed.path.rstrip('/')}"


class FeaturedTikTok(models.Model):
    """A public TikTok or Instagram Reel featured on Betra's website."""

    class Category(models.TextChoices):
        BEAUTY = "beauty", "Beauty"
        FASHION = "fashion", "Fashion"
        LIFESTYLE = "lifestyle", "Lifestyle"
        BRAND = "brand", "Brand Content"

    title = models.CharField(max_length=140)
    brand_name = models.CharField(
        max_length=120,
        blank=True,
        default="",
        help_text="Optional. Add the brand name only when it accurately describes this post.",
    )
    category = models.CharField(
        max_length=20,
        choices=Category.choices,
        default=Category.BEAUTY,
        help_text=(
            "Used by the portfolio video filters. Brand Content videos appear under "
            "Brand Work on the portfolio page."
        ),
    )
    tiktok_url = models.URLField(
        "Video link",
        help_text=(
            "Paste a public TikTok or Instagram Reel link. TikTok share links "
            "(tiktok.com/t/...) are converted to the full video link when you save."
        ),
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
        verbose_name = "Featured video"
        verbose_name_plural = "Featured videos (TikTok & Reels)"

    def clean(self):
        super().clean()
        errors = {}

        if self.tiktok_url and _is_tiktok_short_link(self.tiktok_url):
            try:
                resolved = resolve_tiktok_short_link(self.tiktok_url)
            except (URLError, OSError, ValueError):
                resolved = ""
            if resolved:
                self.tiktok_url = resolved
            else:
                errors["tiktok_url"] = (
                    "This TikTok share link couldn't be opened. Open it in your browser and "
                    "paste the full link that contains /video/ instead."
                )

        if (
            self.tiktok_url
            and "tiktok_url" not in errors
            and not (self.video_id or self.instagram_code)
        ):
            errors["tiktok_url"] = (
                "Paste a public TikTok video link (with /video/ and the video number) "
                "or an Instagram Reel link (instagram.com/reel/...)."
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
    def instagram_code(self):
        return _instagram_reel_code(self.tiktok_url)

    @property
    def platform(self):
        if self.video_id:
            return "tiktok"
        if self.instagram_code:
            return "instagram"
        return ""

    @property
    def platform_label(self):
        return {"tiktok": "TikTok", "instagram": "Instagram"}.get(self.platform, "")

    @property
    def embed_url(self):
        if self.video_id:
            return (
                f"https://www.tiktok.com/player/v1/{self.video_id}"
                # Clean player: no controls, captions or overlays. Autoplay wakes the
                # player (browsers start it muted) so the page script can control it:
                # play on hover, with sound once the visitor has clicked the page.
                "?controls=0&progress_bar=0&play_button=0&volume_control=0"
                "&fullscreen_button=0&timestamp=0&music_info=0&description=0"
                "&rel=0&closed_caption=0&native_context_menu=0"
                "&loop=1&autoplay=1"
            )
        if self.instagram_code:
            return f"https://www.instagram.com/reel/{self.instagram_code}/embed/"
        return ""

    def __str__(self):
        return self.title
