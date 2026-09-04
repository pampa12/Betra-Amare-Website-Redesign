from django.db import migrations


OLD_INTRO = (
    "I create confident, feminine visuals rooted in beauty, fashion, "
    "lifestyle, and authentic storytelling."
)
NEW_INTRO = (
    "I create confident, feminine visuals across beauty, fashion, and lifestyle — "
    "with a polished eye and a personal point of view."
)

OLD_ABOUT = (
    "I'm Betra Amare, a model and digital creator with a love for beauty, fashion, confidence, "
    "and authentic storytelling. I create content that feels polished without losing the personality behind it."
)
NEW_ABOUT = (
    "I'm Betra Amare, a model and digital creator drawn to beauty, fashion, confidence, "
    "and expressive visuals. I create content that feels polished without losing the personality behind it."
)


def refine_default_copy(apps, schema_editor):
    HomepageContent = apps.get_model("website", "HomepageContent")
    HomepageContent.objects.filter(intro_text=OLD_INTRO).update(intro_text=NEW_INTRO)
    HomepageContent.objects.filter(about_text_1=OLD_ABOUT).update(about_text_1=NEW_ABOUT)


class Migration(migrations.Migration):
    dependencies = [
        ("website", "0005_portfolioitem_video"),
    ]

    operations = [
        migrations.RunPython(refine_default_copy, migrations.RunPython.noop),
    ]
