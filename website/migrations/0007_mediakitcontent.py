from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("website", "0006_refine_default_copy"),
    ]

    operations = [
        migrations.CreateModel(
            name="MediaKitContent",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("eyebrow", models.CharField(default="Media kit", max_length=120)),
                ("headline_line1", models.CharField(default="Partner with", max_length=160)),
                ("headline_emphasis", models.CharField(default="Betra Amare.", max_length=160)),
                ("intro_text", models.TextField(default="A quick look at my creative focus, audience, services, and partnership options for brands, agencies, and collaborators.")),
                ("hero_image", models.ImageField(blank=True, upload_to="media-kit/")),
                ("profile_eyebrow", models.CharField(default="Creator profile", max_length=120)),
                ("profile_title", models.CharField(default="Beauty, fashion & lifestyle", max_length=160)),
                ("profile_body", models.TextField(default="I create polished, personality-led content for beauty, fashion, lifestyle, wellness, and culture-focused brands. Projects can include creator-led campaigns, UGC, modeling, photoshoots, events, and social-first storytelling.")),
                ("instagram_followers", models.CharField(blank=True, default="", max_length=40)),
                ("tiktok_followers", models.CharField(blank=True, default="", max_length=40)),
                ("engagement_rate", models.CharField(blank=True, default="", max_length=40)),
                ("average_views", models.CharField(blank=True, default="", max_length=40)),
                ("audience_locations", models.CharField(blank=True, default="", max_length=180)),
                ("audience_age", models.CharField(blank=True, default="", max_length=120)),
                ("audience_gender", models.CharField(blank=True, default="", max_length=120)),
                ("services", models.TextField(default="Sponsored content\nUGC / content creation\nModeling\nCampaigns & photoshoots\nEvents & appearances")),
                ("partnerships", models.TextField(blank=True, default="", help_text="Optional: list past brand partnerships, one per line.")),
                ("rate_card_note", models.TextField(default="Rates and deliverables are tailored to project scope, usage, timeline, and creative requirements.")),
                ("media_kit_pdf_url", models.URLField(blank=True, default="", help_text="Optional public URL for a downloadable PDF media kit.")),
                ("contact_email", models.EmailField(default="workwithbetra@gmail.com", max_length=254)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "verbose_name": "Media kit content",
                "verbose_name_plural": "Media kit content",
            },
        ),
    ]
