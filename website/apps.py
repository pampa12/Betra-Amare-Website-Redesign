from django.apps import AppConfig


class WebsiteConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "website"

    def ready(self):
        # FeaturedTikTok lives in its own module so the creator-content feature stays isolated.
        from . import featured_tiktok  # noqa: F401
