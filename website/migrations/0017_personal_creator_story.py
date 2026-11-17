from django.db import migrations


def update_creator_copy(apps, schema_editor):
    db = schema_editor.connection.alias
    Home = apps.get_model("website", "HomepageContent")
    About = apps.get_model("website", "AboutContent")
    Tool = apps.get_model("website", "Tool")

    # Update only the approved story fields; leave all media and other settings untouched.
    home_fields = {
        "about_title_line1": "Rooted in culture.",
        "about_title_emphasis": "Driven by creativity.",
        "about_text_1": "Growing up in Ethiopia shaped the way I see the world, express myself, and approach creativity. My roots have taught me resilience, individuality, and the beauty of finding inspiration in everyday life.",
        "about_text_2": "Before I even knew what content creation was, I was cutting pictures out of fashion magazines and creating vision boards. What started as a childhood fascination with fashion has grown into a passion for modeling, digital storytelling, and creative marketing. Today, I create to inspire others to embrace their individuality, build confidence, and become the best versions of themselves — something I'm constantly working toward, too.",
    }
    about_fields = {
        "story_paragraph_1": "Growing up in Ethiopia shaped the way I see the world, express myself, and approach creativity. My roots have taught me resilience, individuality, and the beauty of finding inspiration in everyday life.",
        "story_paragraph_2": "Before I even knew what content creation was, I was cutting pictures out of fashion magazines and creating vision boards. What started as a childhood fascination with fashion has grown into a passion for modeling, digital storytelling, and creative marketing.",
        "story_paragraph_3": "Today, I create to inspire others to embrace their individuality, build confidence, and become the best versions of themselves — something I'm constantly working toward, too.",
    }
    Home.objects.using(db).all().update(**home_fields)
    About.objects.using(db).all().update(**about_fields)
    for name in ("CapCut", "Pinterest"):
        if not Tool.objects.using(db).filter(name__iexact=name).exists():
            Tool.objects.using(db).create(name=name, active=True, sort_order=100)


class Migration(migrations.Migration):
    dependencies = [("website", "0016_contact_linkedin")]
    operations = [
        migrations.RunPython(update_creator_copy, migrations.RunPython.noop),
    ]
