from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("website", "0007_mediakitcontent"),
    ]

    operations = [
        migrations.CreateModel(
            name="FeaturedTikTok",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=140)),
                (
                    "brand_name",
                    models.CharField(
                        blank=True,
                        default="",
                        help_text="Optional. Add the brand name only when it accurately describes this post.",
                        max_length=120,
                    ),
                ),
                (
                    "tiktok_url",
                    models.URLField(
                        help_text=(
                            "Paste the full public TikTok video URL, for example "
                            "https://www.tiktok.com/@username/video/1234567890"
                        )
                    ),
                ),
                (
                    "description",
                    models.TextField(
                        blank=True,
                        default="",
                        help_text="Optional short note about the concept, product, or deliverable.",
                    ),
                ),
                ("active", models.BooleanField(default=True)),
                ("sort_order", models.PositiveIntegerField(default=0)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "verbose_name": "Featured TikTok",
                "verbose_name_plural": "Featured TikToks",
                "ordering": ["sort_order", "-created_at"],
            },
        ),
    ]
