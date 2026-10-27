"""Checks that the redesigned portfolio still uses admin-managed photos and videos."""
from django.test import TestCase
from django.urls import reverse

from website.models import AboutContent, PortfolioItem


class CreativePortfolioTests(TestCase):
    def test_empty_portfolio_shows_useful_fallback(self):
        response = self.client.get(reverse("website:portfolio"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "CREATIVE")
        self.assertContains(response, "More projects, coming soon.")
        self.assertContains(response, "ABOUT")
        self.assertContains(response, "STORIES FOR")
        self.assertContains(response, "WHAT I")
        self.assertContains(response, "portfolio-story.css")
        self.assertNotContains(response, 'class="portfolio-item')

    def test_portfolio_cards_and_mobile_mockups_use_existing_media(self):
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

    def test_video_and_photo_lightbox_markers_preserved(self):
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
