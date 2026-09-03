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
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Homepage content"
        verbose_name_plural = "Homepage content"

    def __str__(self):
        return "Homepage content"


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
