from pathlib import Path
from uuid import uuid4

from django.contrib import admin
from django.utils.text import slugify

from .models import (
    AboutContent,
    ContactContent,
    HomepageContent,
    Inquiry,
    InquiryPageContent,
    PortfolioItem,
    PortfolioPageContent,
)


def _give_new_upload_clean_name(field_file, title):
    """Rename a new admin upload before Django sends it to media storage."""
    if not field_file or getattr(field_file, "_committed", True):
        return

    extension = Path(field_file.name).suffix.lower()
    title_slug = slugify(title)[:80] or "portfolio-item"
    field_file.name = f"{title_slug}-{uuid4().hex[:8]}{extension}"


class SingletonContentAdmin(admin.ModelAdmin):
    list_display = ("__str__", "updated_at")

    def has_add_permission(self, request):
        if self.model.objects.exists():
            return False
        return super().has_add_permission(request)


@admin.register(HomepageContent)
class HomepageContentAdmin(SingletonContentAdmin):
    fieldsets = (
        ("Hero", {"fields": ("eyebrow", "headline_line1", "headline_line2", "headline_emphasis", "intro_text", "hero_image", "cta_text")}),
        ("A little bit of my world", {"fields": ("world_eyebrow", "world_title_line1", "world_title_emphasis", "world_body")}),
        ("Category cards", {"fields": (("category_1_title", "category_1_subtitle"), "category_1_image", ("category_2_title", "category_2_subtitle"), "category_2_image", ("category_3_title", "category_3_subtitle"), "category_3_image")}),
        ("Meet Betra", {"fields": ("about_eyebrow", "about_title_line1", "about_title_emphasis", "about_text_1", "about_text_2", "about_main_image", "about_accent_image")}),
        ("Selected work", {"fields": ("selected_eyebrow", "selected_title")}),
        ("Collaboration", {"fields": ("collab_eyebrow", "collab_title_prefix", "collab_title_emphasis", "collab_body", "collab_button_text", "collab_email")}),
        ("Social", {"fields": ("social_eyebrow", "social_title", "social_photo_1", "social_photo_2", "social_photo_3", "social_photo_4")}),
    )


@admin.register(AboutContent)
class AboutContentAdmin(SingletonContentAdmin):
    pass


@admin.register(ContactContent)
class ContactContentAdmin(SingletonContentAdmin):
    pass


@admin.register(PortfolioPageContent)
class PortfolioPageContentAdmin(SingletonContentAdmin):
    pass


@admin.register(InquiryPageContent)
class InquiryPageContentAdmin(SingletonContentAdmin):
    pass


@admin.register(PortfolioItem)
class PortfolioItemAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "media_type", "featured", "active", "sort_order", "updated_at")
    list_filter = ("category", "featured", "active")
    search_fields = ("title", "alt_text")
    list_editable = ("featured", "active", "sort_order")
    fieldsets = (
        (
            "Portfolio media",
            {
                "fields": ("title", "category", "image", "video", "alt_text", "link_url"),
                "description": (
                    "Add a photo, a video, or both. If both are added, the photo is used as the video's poster image."
                ),
            },
        ),
        ("Display", {"fields": ("featured", "active", "sort_order")}),
    )

    def save_model(self, request, obj, form, change):
        # Use the portfolio title rather than the raw phone/camera filename.
        # A short unique suffix prevents collisions without exposing messy source names.
        _give_new_upload_clean_name(obj.image, obj.title)
        _give_new_upload_clean_name(obj.video, obj.title)
        super().save_model(request, obj, form, change)

    @admin.display(description="Media")
    def media_type(self, obj):
        if obj.video and obj.image:
            return "Video + poster"
        if obj.video:
            return "Video"
        return "Photo"


@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "company", "status", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("name", "email", "company", "message")
    readonly_fields = ("created_at",)


admin.site.site_header = "Betra Amare Administration"
admin.site.site_title = "Betra Amare Admin"
admin.site.index_title = "Website management"