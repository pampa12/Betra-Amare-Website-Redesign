"""Regression tests for the cinematic editorial portfolio and managed media."""
from unittest import mock

from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse

from website.featured_tiktok import FeaturedTikTok
from website.models import AboutContent, PortfolioItem


class FilmPortfolioTests(TestCase):
    def get_page(self):
        return self.client.get(reverse("website:portfolio"))

    def test_empty_page_renders_black_intro_and_appropriate_empty_state(self):
        response = self.get_page()
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Who made this creative portfolio?")
        self.assertContains(response, "BETRA")
        self.assertContains(response, "PORTFOLIO")
        self.assertContains(response, "SELECTED")
        self.assertContains(response, "Coming")
        self.assertContains(response, "CREATIVE")
        self.assertContains(response, "portfolio-film.css")
        self.assertContains(response, "portfolio-film.js")
        self.assertNotContains(response, 'class="portfolio-item')
        self.assertNotContains(response, 'class="film-gallery-menu')

    def test_existing_cloudinary_images_fill_about_and_selected_work(self):
        AboutContent.objects.create(story_image="about/intro-photo")
        PortfolioItem.objects.create(
            title="Beauty portrait", category="beauty",
            image="media/portfolio/beauty-portrait", alt_text="Editorial beauty portrait",
            featured=True, active=True,
        )
        PortfolioItem.objects.create(
            title="Fashion portrait", category="fashion",
            image="media/portfolio/fashion-portrait", active=True,
        )
        PortfolioItem.objects.create(
            title="Unpublished draft", category="lifestyle",
            image="media/portfolio/draft", active=False,
        )
        response = self.get_page()
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'class="film-about-portrait')
        self.assertContains(response, "about/intro-photo")
        self.assertContains(response, 'class="film-gallery portfolio-masonry"')
        self.assertContains(response, "Beauty portrait")
        self.assertContains(response, "Fashion portrait")
        self.assertContains(response, 'data-filter="beauty"')
        self.assertContains(response, 'aria-pressed="false"')
        self.assertContains(response, 'data-film-stills')
        self.assertNotContains(response, "Unpublished draft")
        self.assertNotContains(response, "media/portfolio/draft")

    def test_selected_work_keeps_video_and_photo_lightbox(self):
        PortfolioItem.objects.create(
            title="Video project", category="brand",
            video="portfolio/videos/reel.mp4",
            image="portfolio/posters/reel",
            active=True,
        )
        PortfolioItem.objects.create(
            title="Image project", category="lifestyle",
            image="portfolio/lifestyle-still", active=True,
        )
        response = self.get_page()
        self.assertContains(response, 'data-media-type="video"')
        self.assertContains(response, 'data-media-type="image"')
        self.assertContains(response, 'id="portfolioLightbox"')
        self.assertContains(response, "portfolio.js")
        self.assertContains(response, 'data-film-video')

    def test_active_uploaded_video_plays_as_motion_showcase(self):
        PortfolioItem.objects.create(
            title="Featured film", category="beauty",
            video="portfolio/videos/featured.mp4",
            image="portfolio/posters/featured", featured=True, active=True,
        )
        response = self.get_page()
        self.assertContains(response, 'class="film-feature-video film-reel-native"')
        self.assertContains(response, "data-film-video")
        self.assertContains(response, "autoplay muted loop playsinline controls")
        self.assertContains(response, "portfolio/videos/featured.mp4")
        self.assertNotContains(response, 'data-film-stills')

    def test_falls_back_to_active_own_tiktok_only_when_no_uploaded_video(self):
        FeaturedTikTok.objects.create(
            title="Official creator video",
            tiktok_url="https://www.tiktok.com/@creator/video/7543219876543210987",
            active=True,
        )
        response = self.get_page()
        self.assertContains(response, "www.tiktok.com/player/v1/7543219876543210987")
        self.assertContains(response, "Official creator video")
        self.assertNotContains(response, "data-film-video")

    def test_unpublished_video_and_tiktok_are_excluded(self):
        PortfolioItem.objects.create(
            title="Private film", category="brand",
            video="portfolio/private.mp4", active=False,
        )
        FeaturedTikTok.objects.create(
            title="Private TikTok",
            tiktok_url="https://www.tiktok.com/@creator/video/7543219876543210987",
            active=False,
        )
        response = self.get_page()
        self.assertNotContains(response, "portfolio/private.mp4")
        self.assertNotContains(response, "www.tiktok.com/player/")
        self.assertContains(response, "film-reel-empty")

    def test_tiktoks_and_reels_fill_a_filterable_video_strip(self):
        FeaturedTikTok.objects.create(
            title="Glow routine", category="beauty",
            tiktok_url="https://www.tiktok.com/@betraamarey/video/7629417669174807821",
            sort_order=1,
        )
        FeaturedTikTok.objects.create(
            title="Weekend fit", category="lifestyle",
            tiktok_url="https://www.instagram.com/reel/Ddo7hnHBPcr/?igsh=abc",
            sort_order=2,
        )
        response = self.get_page()
        self.assertContains(response, "film-editorial--reels")
        self.assertContains(response, "data-reel-track")
        self.assertContains(response, 'data-src="https://www.tiktok.com/player/v1/7629417669174807821')
        self.assertContains(response, 'data-src="https://www.instagram.com/reel/Ddo7hnHBPcr/embed/"')
        self.assertContains(response, "film-reel-phone--instagram")
        self.assertContains(response, 'data-reel-filter="beauty"')
        self.assertContains(response, 'data-reel-filter="lifestyle"')
        self.assertNotContains(response, 'data-reel-filter="fashion"')
        self.assertContains(response, "portfolio-reels.js")
        # Embeds load lazily from data-src, never eagerly.
        self.assertNotRegex(response.content.decode(), r'(?<!data-)src="https://www\.tiktok\.com/player/')

    def test_brand_videos_move_to_brand_work_without_duplicates(self):
        FeaturedTikTok.objects.create(
            title="Wavy Talk collab", category="brand", brand_name="Wavy Talk",
            tiktok_url="https://www.tiktok.com/@betraamarey/video/7597429740336647479",
        )
        FeaturedTikTok.objects.create(
            title="Glow routine", category="beauty",
            tiktok_url="https://www.tiktok.com/@betraamarey/video/7629417669174807821",
        )
        response = self.get_page()
        html = response.content.decode()
        self.assertEqual(html.count("player/v1/7597429740336647479"), 1)
        self.assertContains(response, "film-brands-reels")
        self.assertContains(response, "Collab · Wavy Talk")
        self.assertNotContains(response, "Selected brand projects will appear here")

    def test_collaborations_are_derived_from_active_brand_content(self):
        PortfolioItem.objects.create(
            title="Actual collaboration", category="brand",
            image="portfolio/actual-campaign", active=True,
        )
        PortfolioItem.objects.create(
            title="Unpublished collaboration", category="brand",
            image="portfolio/draft-campaign", active=False,
        )
        PortfolioItem.objects.create(
            title="Beauty campaign", category="beauty",
            image="portfolio/beauty-campaign", active=True,
        )
        response = self.get_page()
        self.assertContains(response, "Actual collaboration")
        self.assertContains(response, "portfolio/actual-campaign")
        self.assertContains(response, 'class="film-brand-card')
        self.assertNotContains(response, "Unpublished collaboration")
        self.assertNotContains(response, "portfolio/draft-campaign")


class FeaturedVideoLinkTests(TestCase):
    def test_instagram_reel_links_are_accepted(self):
        post = FeaturedTikTok(title="Reel", tiktok_url="https://www.instagram.com/reel/DaIpBL_Rba_/?vrfl=x")
        post.full_clean()
        self.assertEqual(post.platform, "instagram")
        self.assertEqual(post.embed_url, "https://www.instagram.com/reel/DaIpBL_Rba_/embed/")

    def test_tiktok_share_links_are_expanded_on_save(self):
        post = FeaturedTikTok(title="Share link", tiktok_url="https://www.tiktok.com/t/ZTfprFgNQ/")
        resolved = "https://www.tiktok.com/@betraamarey/video/7629417669174807821"
        with mock.patch("website.featured_tiktok.resolve_tiktok_short_link", return_value=resolved):
            post.full_clean()
        self.assertEqual(post.tiktok_url, resolved)
        self.assertEqual(post.video_id, "7629417669174807821")

    def test_unreachable_share_link_explains_what_to_paste(self):
        post = FeaturedTikTok(title="Share link", tiktok_url="https://vm.tiktok.com/ZMabc123/")
        with mock.patch("website.featured_tiktok.resolve_tiktok_short_link", side_effect=OSError):
            with self.assertRaises(ValidationError) as ctx:
                post.full_clean()
        self.assertIn("/video/", str(ctx.exception))

    def test_other_links_are_rejected(self):
        post = FeaturedTikTok(title="Nope", tiktok_url="https://www.youtube.com/watch?v=abc")
        with self.assertRaises(ValidationError):
            post.full_clean()
