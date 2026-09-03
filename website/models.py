from django.db import models


class HomepageContent(models.Model):
    eyebrow = models.CharField(max_length=120, default="Model · Creator · Storyteller")
    headline_line1 = models.CharField(max_length=120, default="Beauty, style &")
    headline_line2 = models.CharField(max_length=120, default="the moments")
    headline_emphasis = models.CharField(max_length=120, default="in between.")
    intro_text = models.TextField(
        default=(
            "I create confident, feminine visuals rooted in beauty, fashion, "
            "lifestyle, and authentic storytelling."
        )
    )
    hero_image = models.ImageField(upload_to="homepage/", blank=True)
    cta_text = models.CharField(max_length=80, default="Explore my work")

    world_eyebrow = models.CharField(max_length=120, default="A little bit of my world")
    world_title_line1 = models.CharField(max_length=120, default="Created to feel")
    world_title_emphasis = models.CharField(max_length=120, default="beautifully real.")
    world_body = models.TextField(
        default=(
            "From polished beauty looks to everyday lifestyle moments, I love creating imagery "
            "that feels personal, elevated, and easy to connect with."
        )
    )

    about_eyebrow = models.CharField(max_length=120, default="Meet Betra")
    about_title_line1 = models.CharField(max_length=120, default="Creator first.")
    about_title_emphasis = models.CharField(max_length=120, default="Always myself.")
    about_text_1 = models.TextField(
        default=(
            "I'm Betra Amare, a model and digital creator with a love for beauty, fashion, confidence, "
            "and authentic storytelling. I create content that feels polished without losing the personality behind it."
        )
    )
    about_text_2 = models.TextField(
        default=(
            "Whether I'm creating for a brand or sharing a piece of my everyday life, I want the final result "
            "to feel warm, intentional, and true to me."
        )
    )
    about_main_image = models.ImageField(upload_to="homepage/about/", blank=True)
    about_accent_image = models.ImageField(upload_to="homepage/about/", blank=True)

    selected_eyebrow = models.CharField(max_length=120, default="Selected work")
    selected_title = models.CharField(max_length=120, default="A few favorites.")

    collab_eyebrow = models.CharField(max_length=120, default="Let's create something memorable")
    collab_title_prefix = models.CharField(max_length=180, default="For brands that want content to")
    collab_title_emphasis = models.CharField(max_length=120, default="feel human.")
    collab_body = models.TextField(
        default=(
            "I partner with beauty, fashion, lifestyle, and wellness brands to create content that feels natural "
            "to my audience while giving the product a beautiful, intentional spotlight."
        )
    )
    collab_button_text = models.CharField(max_length=80, default="Work with me")
    collab_email = models.EmailField(default="workwithbetra@gmail.com")

    social_eyebrow = models.CharField(max_length=120, default="Follow along")
    social_title = models.CharField(max_length=120, default="More of the everyday.")

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Homepage content"
        verbose_name_plural = "Homepage content"

    def __str__(self):
        return "Homepage content"


class AboutContent(models.Model):
    eyebrow = models.CharField(max_length=120, default="About Betra")
    headline_line1 = models.CharField(max_length=160, default="Confidence, creativity")
    headline_emphasis = models.CharField(max_length=120, default="a little softness.")
    intro_text = models.TextField(
        default=(
            "I care about the kind of content that feels beautiful but still personal — "
            "the kind that makes someone stop because it feels like a real moment, not just an ad."
        )
    )
    story_eyebrow = models.CharField(max_length=120, default="My story")
    story_title = models.CharField(max_length=160, default="Hi, I'm Betra.")
    story_paragraph_1 = models.TextField(
        default=(
            "I'm a model and digital content creator with a love for beauty, fashion, lifestyle, "
            "and self-expression. Creating started as a way for me to share what I love, and it grew "
            "into a space where I can connect with people, work with brands, and tell stories visually."
        )
    )
    story_paragraph_2 = models.TextField(
        default=(
            "My favorite content feels polished without feeling distant. I love clean beauty, feminine "
            "styling, everyday moments, and visuals that let personality come through. Whether I'm in front "
            "of a camera for a photoshoot or building a concept for a brand, I want the final piece to feel "
            "intentional and natural."
        )
    )
    story_paragraph_3 = models.TextField(
        default=(
            "What matters most to me is creating from a place that still feels like me. I want my audience "
            "to trust what I share, and I want brands I work with to feel like their product has been "
            "introduced in a way that fits naturally into my world."
        )
    )
    story_image = models.ImageField(upload_to="about/", blank=True)
    value_1_title = models.CharField(max_length=80, default="Authentic")
    value_1_text = models.CharField(
        max_length=220,
        default="Content that keeps my real voice and personality at the center.",
    )
    value_2_title = models.CharField(max_length=80, default="Intentional")
    value_2_text = models.CharField(
        max_length=220,
        default="Every detail — styling, framing, mood, and message — has a reason.",
    )
    value_3_title = models.CharField(max_length=80, default="Warm")
    value_3_text = models.CharField(
        max_length=220,
        default="Beautiful visuals that still feel approachable, human, and easy to connect with.",
    )
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "About page content"
        verbose_name_plural = "About page content"

    def __str__(self):
        return "About page content"


class ContactContent(models.Model):
    eyebrow = models.CharField(max_length=120, default="Say hello")
    headline_line1 = models.CharField(max_length=120, default="Let's stay")
    headline_emphasis = models.CharField(max_length=120, default="connected.")
    intro_text = models.TextField(
        default=(
            "For general questions, social messages, or anything that isn't a project inquiry, "
            "you can reach me here."
        )
    )
    section_eyebrow = models.CharField(max_length=120, default="Contact")
    section_title_line1 = models.CharField(max_length=120, default="Find me")
    section_title_line2 = models.CharField(max_length=120, default="around the internet.")
    body_text = models.TextField(
        default=(
            "The easiest ways to reach me are by email or through my social platforms. For brand work, "
            "campaigns, UGC, modeling, or paid collaborations, use the dedicated inquiry page instead."
        )
    )
    general_email = models.EmailField(default="betraamare@icloud.com")
    instagram_url = models.URLField(default="https://www.instagram.com/betra_amare")
    instagram_handle = models.CharField(max_length=80, default="@betra_amare")
    tiktok_url = models.URLField(default="https://www.tiktok.com/@betraamarey")
    tiktok_handle = models.CharField(max_length=80, default="@betraamarey")
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Contact page content"
        verbose_name_plural = "Contact page content"

    def __str__(self):
        return "Contact page content"


class PortfolioItem(models.Model):
    class Category(models.TextChoices):
        BEAUTY = "beauty", "Beauty"
        FASHION = "fashion", "Fashion"
        LIFESTYLE = "lifestyle", "Lifestyle"
        BRAND = "brand", "Brand Content"

    title = models.CharField(max_length=140)
    category = models.CharField(max_length=20, choices=Category.choices)
    image = models.ImageField(upload_to="portfolio/")
    alt_text = models.CharField(max_length=180, blank=True)
    featured = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    sort_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["sort_order", "-created_at"]

    def __str__(self):
        return self.title


class Inquiry(models.Model):
    class Status(models.TextChoices):
        NEW = "new", "New"
        REPLIED = "replied", "Replied"
        ARCHIVED = "archived", "Archived"

    name = models.CharField(max_length=120)
    email = models.EmailField()
    company = models.CharField(max_length=160, blank=True)
    project_type = models.CharField(max_length=120, blank=True)
    budget = models.CharField(max_length=120, blank=True)
    message = models.TextField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.NEW)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} — {self.email}"
