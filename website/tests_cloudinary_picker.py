"""Tests for the Django admin picker that reuses existing Cloudinary photos."""
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings
from django.urls import reverse

from website.admin import PortfolioItemAdminForm
from website.models import PortfolioItem

CLOUDINARY_TEST_SETTINGS = {
    "USE_CLOUDINARY": True,
    "CLOUDINARY_URL": "cloudinary://test-key:test-secret@test-cloud",
}
PUBLIC_ID = "media/portfolio/existing-photo"


def resource(public_id=PUBLIC_ID, *, resource_type="image", delivery_type="upload"):
    return {
        "public_id": public_id,
        "resource_type": resource_type,
        "type": delivery_type,
    }


def portfolio_data(**overrides):
    data = {
        "title": "Existing beauty photo",
        "category": "beauty",
        "alt_text": "Portrait in natural light",
        "sort_order": 0,
        "active": True,
    }
    data.update(overrides)
    return data


@override_settings(**CLOUDINARY_TEST_SETTINGS)
class CloudinaryImagePickerTests(TestCase):
    def setUp(self):
        self.url = reverse("admin:website_portfolioitem_cloudinary_images")
        self.admin_user = get_user_model().objects.create_superuser(
            username="test-admin", email="admin@example.com", password="test-password"
        )

    @patch("website.admin_cloudinary.cloudinary.CloudinaryImage")
    @patch("website.admin_cloudinary.cloudinary.api.resources")
    def test_admin_can_page_cloudinary_images_without_credentials_in_response(self, resources, cloud_image):
        resources.return_value = {
            "resources": [resource()],
            "next_cursor": "next-page-token",
        }
        cloud_image.return_value.build_url.return_value = "https://res.cloudinary.com/test-cloud/image/upload/test.jpg"
        self.client.force_login(self.admin_user)
        response = self.client.get(self.url, {"q": "media/", "cursor": "previous-page-token"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["images"][0]["public_id"], PUBLIC_ID)
        self.assertEqual(response.json()["next_cursor"], "next-page-token")
        self.assertNotIn("test-secret", response.content.decode())
        resources.assert_called_once_with(
            resource_type="image",
            type="upload",
            max_results=24,
            prefix="media/",
            next_cursor="previous-page-token",
        )

    def test_anonymous_admin_browser_is_not_public(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/admin/login/", response.url)

    def test_staff_without_model_permissions_cannot_list_images(self):
        limited_user = get_user_model().objects.create_user(
            username="limited-user", password="test-password", is_staff=True
        )
        self.client.force_login(limited_user)
        self.assertEqual(self.client.get(self.url).status_code, 403)

    @override_settings(USE_CLOUDINARY=False)
    def test_disabled_cloudinary_returns_clean_error(self):
        self.client.force_login(self.admin_user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 503)

    @patch("website.admin_cloudinary.cloudinary.api.resource")
    @patch("website.models._optimize_new_upload")
    def test_existing_photo_reuses_public_id_without_upload(self, optimize, fetch):
        fetch.return_value = resource()
        form = PortfolioItemAdminForm(data=portfolio_data(reuse_image=PUBLIC_ID))
        self.assertTrue(form.is_valid(), form.errors.as_text())
        item = form.save()
        self.assertEqual(item.image.name, PUBLIC_ID)
        self.assertTrue(item.image._committed)
        fetch.assert_called_once_with(PUBLIC_ID, resource_type="image", type="upload")
        # Even when save() calls image optimization, it won't open or re-upload an existing public ID.
        self.assertTrue(item.pk)
        self.assertEqual(PortfolioItem.objects.get(pk=item.pk).image.name, PUBLIC_ID)

    @patch("website.admin_cloudinary.cloudinary.api.resource")
    def test_rejects_asset_not_returned_by_own_cloudinary_account(self, fetch):
        fetch.return_value = resource("some-other-photo")
        form = PortfolioItemAdminForm(data=portfolio_data(reuse_image=PUBLIC_ID))
        self.assertFalse(form.is_valid())
        self.assertIn("reuse_image", form.errors)

    @patch("website.admin_cloudinary.cloudinary.api.resource")
    def test_rejects_nonpublic_delivery_types(self, fetch):
        fetch.return_value = resource(delivery_type="private")
        form = PortfolioItemAdminForm(data=portfolio_data(reuse_image=PUBLIC_ID))
        self.assertFalse(form.is_valid())
        self.assertIn("reuse_image", form.errors)

    def test_existing_upload_reference_is_unchanged_when_no_new_choice(self):
        item = PortfolioItem.objects.create(
            title="Original", category="beauty", image="portfolio/previous-upload"
        )
        form = PortfolioItemAdminForm(data=portfolio_data(), instance=item)
        self.assertTrue(form.is_valid(), form.errors.as_text())
        saved = form.save()
        self.assertEqual(saved.image.name, "portfolio/previous-upload")

    @patch("website.admin_cloudinary.cloudinary.api.resource")
    def test_picker_available_on_homepage_and_portfolio_admin(self, fetch):
        self.client.force_login(self.admin_user)
        home = self.client.get(reverse("admin:website_homepagecontent_add"))
        portfolio = self.client.get(reverse("admin:website_portfolioitem_add"))
        self.assertContains(home, "reuse_category_1_image")
        self.assertContains(home, "reuse_hero_image")
        self.assertContains(portfolio, "reuse_image")
        self.assertContains(portfolio, "Choose from Cloudinary", status_code=200)
        fetch.assert_not_called()
