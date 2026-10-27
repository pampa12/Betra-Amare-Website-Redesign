"""Regression tests for the pink editorial portfolio and Cloudinary-backed media."""
from django.test import TestCase
from django.urls import reverse

from website.models import AboutContent, PortfolioItem


class CreativePortfolioTests(TestCase):
    def test_empty_portfolio_displays_pink_portfolio_sections_without_fake_collaborations(self):
        response = self.client.get(reverse("website:portfolio"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "MY")
        self.assertContains(response, "marketing")
        self.assertContains(response, "YOUR SOCIALS DESERVE")
        self.assertContains(response, "BRAND")
        self.assertContains(response, "SKILLS")
        self.assertContains(response, "More projects, coming soon.")
        self.assertContains(response, "Collaboration work, curated here.")
        self.assertContains(response, "portfolio-story.css")
        self.assertNotContains(response, 'class="portfolio-item')

    def test_existing_photos_show_in_collage_phones_and_work_gallery(self):
        AboutContent.objects.create(story_image="about/intro-photo")
        PortfolioItem.objects.create(
            title="Beauty campaign", category="beauty",
            image="media/portfolio/beauty-portrait", alt_text="Beauty portrait",
            featured=True, active=True,
        )
        PortfolioItem.objects.create(
            title="Fashion portrait", category="fashion",
            image="media/portfolio/fashion-portrait", alt_text="Fashion portrait",
            active=True,
        )
        PortfolioItem.objects.create(
            title="Hidden draft", category="lifestyle",
            image="media/portfolio/draft", active=False,
        )

        response = self.client.get(reverse("website:portfolio"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Beauty campaign")
        self.assertContains(response, "Fashion portrait")
        self.assertContains(response, "cp-phone cp-phone-1")
        self.assertContains(response, "cp-phone cp-phone-2")
        self.assertContains(response, "about/intro-photo")
        self.assertContains(response, 'data-filter="beauty"')
        self.assertContains(response, 'aria-pressed="false"')
        self.assertNotContains(response, "Hidden draft")
        self.assertNotContains(response, "media/portfolio/draft")
        self.assertContains(response, "Collaboration work, curated here.")

    def test_brand_partnerships_show_only_active_brand_items_with_images(self):
        PortfolioItem.objects.create(
            title="Brand campaign", category="brand",
            image="media/portfolio/brand-campaign",
            alt_text="Brand collaboration image", active=True,
        )
        PortfolioItem.objects.create(
            title="Beauty shoot", category="beauty",
            image="media/portfolio/beauty", alt_text="Beauty portrait", active=True,
        )
        PortfolioItem.objects.create(
            title="Unapproved campaign", category="brand",
            image="media/portfolio/draft-brand", active=False,
        )
        response = self.client.get(reverse("website:portfolio"))
        self.assertContains(response, "cp-brand-phone")
        self.assertContains(response, "Brand campaign")
        self.assertContains(response, "media/portfolio/brand-campaign")
        self.assertNotContains(response, "Unapproved campaign")
        self.assertNotContains(response, "Collaboration work, curated here.")

    def test_video_and_photo_lightbox_markers_are_preserved(self):
        PortfolioItem.objects.create(
            title="Reel example", category="brand",
            image="media/portfolio/video-poster",
            video="portfolio/videos/reel.mp4", alt_text="Campaign video", active=True,
        )
        PortfolioItem.objects.create(
            title="Lifestyle example", category="lifestyle",
            image="media/portfolio/street-style", alt_text="Lifestyle photo", active=True,
        )
        response = self.client.get(reverse("website:portfolio"))
        self.assertContains(response, 'data-media-type="video"')
        self.assertContains(response, 'data-media-type="image"')
        self.assertContains(response, 'id="portfolioLightbox"')
        self.assertContains(response, "portfolio.js")
