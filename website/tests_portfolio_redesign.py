"""Regression tests for the pink editorial portfolio and Cloudinary-backed media."""
from django.test import TestCase
from django.urls import reverse

from website.featured_tiktok import FeaturedTikTok
from website.models import AboutContent, PortfolioItem


class CreativePortfolioTests(TestCase):
    def test_empty_portfolio_displays_pink_portfolio_sections_without_fake_collaborations(self):
        response = self.client.get(reverse("website:portfolio"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Creative")
        self.assertContains(response, "portfolio.")
        self.assertContains(response, "CONTENT THAT")
        self.assertContains(response, "SELECTED")
        self.assertContains(response, "TOOLS OF")
        self.assertContains(response, "portfolio-cinematic.css")
        self.assertContains(response, "portfolio-cinematic.js")
        self.assertContains(response, "More projects, coming soon.")
        self.assertContains(response, "Collaboration work, curated here.")
        self.assertContains(response, "portfolio-story.css")
        self.assertNotContains(response, 'class="portfolio-item')

    def test_existing_photos_show_in_cinematic_hero_phone_and_work_gallery(self):
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
        self.assertContains(response, 'class="cinematic-hero-art"')
        self.assertContains(response, 'class="portfolio-masonry cp-masonry cinematic-project-grid"')
        self.assertContains(response, 'class="cp-iphone"')
        self.assertContains(response, 'data-phone-slideshow')
        self.assertContains(response, 'class="cp-reel-image is-active"')
        self.assertContains(response, "portfolio-reel.js")
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

    def test_real_cloudinary_video_takes_priority_over_photos(self):
        PortfolioItem.objects.create(
            title="Campaign photograph", category="beauty",
            image="portfolio/campaign-photo", active=True,
        )
        PortfolioItem.objects.create(
            title="Selected film", category="brand",
            image="portfolio/video-poster",
            video="portfolio/videos/film.mp4", featured=True, active=True,
        )
        response = self.client.get(reverse("website:portfolio"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'data-mode="video"')
        self.assertContains(response, "data-portfolio-reel")
        self.assertContains(response, "autoplay muted loop playsinline controls")
        self.assertContains(response, "portfolio/videos/film.mp4")
        self.assertContains(response, "Pause video")
        self.assertNotContains(response, "data-phone-slideshow")

    def test_active_tiktok_embeds_as_video_fallback_when_no_uploaded_video(self):
        FeaturedTikTok.objects.create(
            title="Own UGC reel",
            tiktok_url="https://www.tiktok.com/@creator/video/7543219876543210987",
            active=True,
        )
        PortfolioItem.objects.create(
            title="Photo", category="beauty", image="portfolio/photo", active=True
        )
        response = self.client.get(reverse("website:portfolio"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'data-mode="tiktok"')
        self.assertContains(response, "www.tiktok.com/player/v1/7543219876543210987?autoplay=1")
        self.assertContains(response, "Open original TikTok")
        self.assertNotContains(response, "data-portfolio-reel")
        self.assertNotContains(response, "data-phone-slideshow")

    def test_inactive_video_and_tiktok_do_not_appear(self):
        PortfolioItem.objects.create(
            title="Unpublished film", category="brand",
            video="portfolio/videos/private.mp4", active=False,
        )
        FeaturedTikTok.objects.create(
            title="Unpublished TikTok",
            tiktok_url="https://www.tiktok.com/@creator/video/7543219876543210987",
            active=False,
        )
        response = self.client.get(reverse("website:portfolio"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'data-mode="photos"')
        self.assertContains(response, "Creative films")
        self.assertNotContains(response, "private.mp4")
        self.assertNotContains(response, "www.tiktok.com/player/")
