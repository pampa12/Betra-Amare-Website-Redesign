from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("website", "0009_featuredtiktok_show_on_homepage"),
    ]

    operations = [
        migrations.AddField(
            model_name="featuredtiktok",
            name="thumbnail",
            field=models.ImageField(
                blank=True,
                help_text=(
                    "Upload a clean still frame for the homepage card. "
                    "The Media Kit can still use the live TikTok player."
                ),
                upload_to="featured-tiktoks/thumbnails/",
            ),
        ),
    ]
