from django.core.validators import FileExtensionValidator
from django.db import migrations, models

import website.models


class Migration(migrations.Migration):

    dependencies = [
        ("website", "0004_inquirypagecontent_portfoliopagecontent_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="portfolioitem",
            name="image",
            field=models.ImageField(blank=True, upload_to="portfolio/"),
        ),
        migrations.AddField(
            model_name="portfolioitem",
            name="video",
            field=models.FileField(
                blank=True,
                help_text="Optional video. Supported formats: MP4, MOV, M4V, WEBM.",
                storage=website.models.portfolio_video_storage,
                upload_to="portfolio/videos/",
                validators=[FileExtensionValidator(["mp4", "mov", "m4v", "webm"])],
            ),
        ),
    ]
