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
            field=models.ImageField(
                blank=True,
                help_text="Optional photo. If you also add a video, this photo is used as the video poster.",
                upload_to="portfolio/",
            ),
        ),
        migrations.AlterField(
            model_name="portfolioitem",
            name="link_url",
            field=models.URLField(
                blank=True,
                default="",
                help_text="Optional. Leave blank if the photo should not open another page.",
            ),
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
