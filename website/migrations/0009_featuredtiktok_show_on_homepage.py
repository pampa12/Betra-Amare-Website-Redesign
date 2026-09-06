from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("website", "0008_featuredtiktok"),
    ]

    operations = [
        migrations.AddField(
            model_name="featuredtiktok",
            name="show_on_homepage",
            field=models.BooleanField(
                default=False,
                help_text="Show this TikTok inside the homepage 'A few favorites' section.",
            ),
        ),
    ]
