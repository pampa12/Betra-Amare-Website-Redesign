from pathlib import Path
from uuid import uuid4

from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.utils.html import format_html
from django.utils.text import slugify

from .templatetags.media_tags import cdn

from .admin_cloudinary import (
    CloudinaryPickerAdminMixin,
    ExistingCloudinaryImageFormMixin,
    existing_image_field,
)
from .featured_tiktok import FeaturedTikTok
from .models import (
    AboutContent,
    ContactContent,
    HomepageContent,
    Inquiry,
    InquiryPageContent,
    MediaKitContent,
    PortfolioItem,
    PortfolioPageContent,
)


FRIENDLY_LABELS = {
    "active": "Show on site",
    "sort_order": "Order",
}
FRIENDLY_HELP = {
    "active": "Uncheck to hide this from the website without deleting it.",
    "sort_order": "Lower numbers show first. Use 10, 20, 30… so you can slot items in between later.",
}


def _image_thumb(field_file, size=72):
    """A small preview of an uploaded photo for admin lists and forms."""
    if not field_file:
        return "—"
    try:
        url = field_file.url
    except ValueError:
        return "—"
    return format_html(
        '<img src="{}" alt="" style="width:{}px;height:{}px;object-fit:cover;border-radius:6px;display:block">',
        cdn(url, size * 3), size, int(size * 1.25),
    )


def _give_new_upload_clean_name(field_file, title):
    """Rename a new admin upload before Django sends it to media storage."""
    if not field_file or getattr(field_file, "_committed", True):
        return

    extension = Path(field_file.name).suffix.lower()
    title_slug = slugify(title)[:80] or "portfolio-item"
    field_file.name = f"{title_slug}-{uuid4().hex[:8]}{extension}"


class HomepageContentAdminForm(ExistingCloudinaryImageFormMixin, forms.ModelForm):
    reusable_image_fields = (
        "hero_image",
        "category_1_image", "category_2_image", "category_3_image",
        "about_main_image", "about_accent_image",
        "social_photo_1", "social_photo_2", "social_photo_3", "social_photo_4",
    )
    reuse_hero_image = existing_image_field()
    reuse_category_1_image = existing_image_field()
    reuse_category_2_image = existing_image_field()
    reuse_category_3_image = existing_image_field()
    reuse_about_main_image = existing_image_field()
    reuse_about_accent_image = existing_image_field()
    reuse_social_photo_1 = existing_image_field()
    reuse_social_photo_2 = existing_image_field()
    reuse_social_photo_3 = existing_image_field()
    reuse_social_photo_4 = existing_image_field()

    class Meta:
        model = HomepageContent
        fields = "__all__"


class AboutContentAdminForm(ExistingCloudinaryImageFormMixin, forms.ModelForm):
    reusable_image_fields = ("story_image",)
    reuse_story_image = existing_image_field()

    class Meta:
        model = AboutContent
        fields = "__all__"


class MediaKitContentAdminForm(ExistingCloudinaryImageFormMixin, forms.ModelForm):
    reusable_image_fields = ("hero_image",)
    reuse_hero_image = existing_image_field()

    class Meta:
        model = MediaKitContent
        fields = "__all__"


class FeaturedTikTokAdminForm(ExistingCloudinaryImageFormMixin, forms.ModelForm):
    reusable_image_fields = ("thumbnail",)
    reuse_thumbnail = existing_image_field()

    class Meta:
        model = FeaturedTikTok
        fields = "__all__"
        labels = FRIENDLY_LABELS
        help_texts = FRIENDLY_HELP


class PortfolioItemAdminForm(ExistingCloudinaryImageFormMixin, forms.ModelForm):
    reusable_image_fields = ("image",)
    reuse_image = existing_image_field()
    alt_text = forms.CharField(
        max_length=180,
        required=True,
        help_text=(
            "Describe what is visibly happening in this photo or video. "
            "Example: Betra Amare wearing a cream dress in an outdoor fashion editorial."
        ),
    )
    featured = forms.BooleanField(
        required=False,
        label="Show on homepage",
        help_text=(
            "Check this to include the photo or video in the homepage 'A few favorites' section. "
            "For a video, also upload an image to use as its homepage thumbnail/poster."
        ),
    )

    class Meta:
        model = PortfolioItem
        fields = "__all__"
        labels = {**FRIENDLY_LABELS, "link_url": "Link (optional)"}
        help_texts = FRIENDLY_HELP

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get("featured") and cleaned_data.get("video") and not cleaned_data.get("image"):
            self.add_error(
                "image",
                "Add an image/poster before showing this video on the homepage.",
            )
        return cleaned_data


class SingletonContentAdmin(admin.ModelAdmin):
    list_display = ("__str__", "updated_at")

    def has_add_permission(self, request):
        if self.model.objects.exists():
            return False
        return super().has_add_permission(request)


@admin.register(HomepageContent)
class HomepageContentAdmin(CloudinaryPickerAdminMixin, SingletonContentAdmin):
    form = HomepageContentAdminForm
    fieldsets = (
        ("Hero", {"fields": ("eyebrow", "headline_line1", "headline_line2", "headline_emphasis", "intro_text", "hero_image", "reuse_hero_image", "cta_text")}),
        ("A little bit of my world", {"fields": ("world_eyebrow", "world_title_line1", "world_title_emphasis", "world_body")}),
        ("Category cards", {"fields": (("category_1_title", "category_1_subtitle"), "category_1_image", "reuse_category_1_image", ("category_2_title", "category_2_subtitle"), "category_2_image", "reuse_category_2_image", ("category_3_title", "category_3_subtitle"), "category_3_image", "reuse_category_3_image")}),
        ("Meet Betra", {"fields": ("about_eyebrow", "about_title_line1", "about_title_emphasis", "about_text_1", "about_text_2", "about_main_image", "reuse_about_main_image", "about_accent_image", "reuse_about_accent_image")}),
        ("Selected work", {"fields": ("selected_eyebrow", "selected_title")}),
        ("Collaboration", {"fields": ("collab_eyebrow", "collab_title_prefix", "collab_title_emphasis", "collab_body", "collab_button_text", "collab_email")}),
        ("Social", {"fields": ("social_eyebrow", "social_title", "social_photo_1", "reuse_social_photo_1", "social_photo_2", "reuse_social_photo_2", "social_photo_3", "reuse_social_photo_3", "social_photo_4", "reuse_social_photo_4")}),
    )


@admin.register(AboutContent)
class AboutContentAdmin(CloudinaryPickerAdminMixin, SingletonContentAdmin):
    form = AboutContentAdminForm
    fieldsets = (
        ("About page", {"fields": (
            "eyebrow", "headline_line1", "headline_emphasis", "intro_text",
            "story_eyebrow", "story_title", "story_paragraph_1", "story_paragraph_2",
            "story_paragraph_3", "story_image", "reuse_story_image",
            "value_1_title", "value_1_text", "value_2_title", "value_2_text",
            "value_3_title", "value_3_text",
        )}),
    )


@admin.register(ContactContent)
class ContactContentAdmin(SingletonContentAdmin):
    pass


@admin.register(PortfolioPageContent)
class PortfolioPageContentAdmin(SingletonContentAdmin):
    fieldsets = (
        ("Skills & certifications", {
            "fields": ("skills", "tools", "certifications"),
            "description": (
                "The 'Skills & Certifications' section on the portfolio page. "
                "Only add certifications you have actually earned; the heading says "
                "'Skills & Expertise' until the first one is added."
            ),
        }),
        ("Page text", {"fields": ("eyebrow", "headline_line1", "headline_emphasis", "intro_text")}),
        ("Closing call to action", {"fields": (
            "collab_eyebrow", "collab_title_prefix", "collab_title_emphasis", "button_text", "work_email",
        )}),
    )


@admin.register(InquiryPageContent)
class InquiryPageContentAdmin(SingletonContentAdmin):
    pass


@admin.register(MediaKitContent)
class MediaKitContentAdmin(CloudinaryPickerAdminMixin, SingletonContentAdmin):
    form = MediaKitContentAdminForm
    fieldsets = (
        ("Hero", {"fields": ("eyebrow", "headline_line1", "headline_emphasis", "intro_text", "hero_image", "reuse_hero_image")}),
        ("Creator profile", {"fields": ("profile_eyebrow", "profile_title", "profile_body")}),
        (
            "Audience & performance",
            {
                "fields": (
                    ("instagram_followers", "tiktok_followers"),
                    ("engagement_rate", "average_views"),
                    "audience_locations",
                    ("audience_age", "audience_gender"),
                ),
                "description": "Leave any stat blank if you do not want it shown publicly.",
            },
        ),
        ("Services", {"fields": ("services", "partnerships", "rate_card_note")}),
        ("Downloads & contact", {"fields": ("media_kit_pdf_url", "contact_email")}),
    )


@admin.register(FeaturedTikTok)
class FeaturedTikTokAdmin(CloudinaryPickerAdminMixin, admin.ModelAdmin):
    form = FeaturedTikTokAdminForm
    list_display = ("title", "platform_name", "category", "brand_name", "show_on_homepage", "active", "sort_order")
    list_display_links = ("title",)
    list_editable = ("category", "show_on_homepage", "active", "sort_order")
    readonly_fields = ("thumbnail_preview",)
    list_filter = ("category", "show_on_homepage", "active")
    search_fields = ("title", "brand_name", "description", "tiktok_url")
    fieldsets = (
        (
            "Video post",
            {
                "fields": ("title", "tiktok_url", "category", "brand_name", "description"),
                "description": (
                    "Paste a TikTok link (share links like tiktok.com/t/... work) or an Instagram Reel link. "
                    "Videos play in the portfolio's Stories in Motion strip and on the Media Kit. "
                    "Brand Content videos appear under Brand Work."
                ),
            },
        ),
        (
            "Homepage thumbnail (optional)",
            {
                "classes": ("collapse",),
                "fields": ("thumbnail_preview", "thumbnail", "reuse_thumbnail"),
                "description": "Only needed if you check 'Show on homepage' below.",
            },
        ),
        (
            "Display",
            {
                "fields": ("show_on_homepage", "active", "sort_order"),
                "description": (
                    "Check 'Show on homepage' to use the uploaded thumbnail as a clean clickable card inside "
                    "'A few favorites'. The homepage shows up to two checked TikToks."
                ),
            },
        ),
    )


    @admin.display(description="Platform")
    def platform_name(self, obj):
        return obj.platform_label or "—"

    @admin.display(description="Current thumbnail")
    def thumbnail_preview(self, obj):
        return _image_thumb(obj.thumbnail, 120)


@admin.register(PortfolioItem)
class PortfolioItemAdmin(CloudinaryPickerAdminMixin, admin.ModelAdmin):
    form = PortfolioItemAdminForm
    list_display = (
        "photo",
        "title",
        "category",
        "media_type",
        "featured",
        "active",
        "sort_order",
    )
    list_display_links = ("photo", "title")
    list_editable = ("category", "featured", "active", "sort_order")
    readonly_fields = ("photo_preview",)
    list_filter = ("category", "featured", "active")
    search_fields = ("title", "alt_text")
    fieldsets = (
        (
            "Portfolio media",
            {
                "fields": ("title", "category", "photo_preview", "image", "reuse_image", "video", "alt_text", "link_url"),
                "description": (
                    "Add a photo, a video, or both. If both are added, the photo is used as the video's poster image. "
                    "Alt text is required so every portfolio item is accessible and search-friendly."
                ),
            },
        ),
        (
            "Display",
            {
                "fields": ("featured", "active", "sort_order"),
                "description": (
                    "Use 'Show on homepage' to choose exactly which portfolio photos/videos can appear in "
                    "the homepage 'A few favorites' section."
                ),
            },
        ),
    )

    def save_model(self, request, obj, form, change):
        _give_new_upload_clean_name(obj.image, obj.title)
        _give_new_upload_clean_name(obj.video, obj.title)
        super().save_model(request, obj, form, change)

    @admin.display(description="")
    def photo(self, obj):
        return _image_thumb(obj.image, 56)

    @admin.display(description="Current photo")
    def photo_preview(self, obj):
        return _image_thumb(obj.image, 140)

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
    list_editable = ("status",)
    list_filter = ("status", "created_at")
    search_fields = ("name", "email", "company", "message")
    readonly_fields = ("created_at",)


admin.site.site_header = "Betra Amare Administration"
admin.site.site_title = "Betra Amare Admin"
admin.site.index_title = "What would you like to update?"
# More room for lists; the menu is one click away on the home screen.
admin.site.enable_nav_sidebar = False

# Show the things Betra edits most at the top of the admin menu.
ADMIN_MENU_ORDER = [
    "PortfolioItem",
    "FeaturedTikTok",
    "Inquiry",
    "HomepageContent",
    "MediaKitContent",
    "AboutContent",
    "PortfolioPageContent",
    "ContactContent",
    "InquiryPageContent",
]
_default_get_app_list = admin.site.get_app_list


def _ordered_app_list(request, app_label=None):
    app_list = _default_get_app_list(request, app_label)
    for app in app_list:
        if app.get("app_label") == "website":
            app["name"] = "Website"
            app["models"].sort(
                key=lambda m: ADMIN_MENU_ORDER.index(m["object_name"])
                if m["object_name"] in ADMIN_MENU_ORDER else len(ADMIN_MENU_ORDER)
            )
    # Put the Website section before Users/Groups.
    app_list.sort(key=lambda app: 0 if app.get("app_label") == "website" else 1)
    return app_list


admin.site.get_app_list = _ordered_app_list


# Betra manages the site alone; permission groups only add clutter.
try:
    admin.site.unregister(Group)
except admin.sites.NotRegistered:
    pass
