"""Staff-only Cloudinary asset browser and reusable image-field controls.

No Cloudinary API credentials or Admin API calls are exposed to the browser.
Selections are verified server-side and saved as existing public IDs in ImageFields.
"""
import logging

import cloudinary
import cloudinary.api
from cloudinary.exceptions import Error as CloudinaryError
from django import forms
from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseNotAllowed, JsonResponse
from django.urls import path, reverse

logger = logging.getLogger(__name__)
PAGE_SIZE = 24
MAX_PUBLIC_ID_LENGTH = 100  # Existing ImageFields use Django's default max_length.


def existing_image_field():
    """An optional ID field alongside, not instead of, the normal upload control."""
    return forms.CharField(
        label="Or choose an existing Cloudinary photo",
        required=False,
        max_length=MAX_PUBLIC_ID_LENGTH,
        widget=forms.TextInput(
            attrs={
                "class": "cloudinary-picker-input",
                "readonly": "readonly",
                "autocomplete": "off",
            }
        ),
        help_text="Reuses an image already in your Cloudinary library without uploading it again.",
    )


class ExistingCloudinaryImageFormMixin:
    """Set reusable_image_fields in each admin ModelForm."""

    reusable_image_fields = ()

    class Media:
        js = ("website/admin/cloudinary_picker.js",)
        css = {"all": ("website/admin/cloudinary_picker.css",)}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        opts = self._meta.model._meta
        url_name = f"admin:{opts.app_label}_{opts.model_name}_cloudinary_images"
        for image_field in self.reusable_image_fields:
            picker = self.fields[f"reuse_{image_field}"]
            picker.widget.attrs["data-picker-url"] = reverse(url_name)
            picker.widget.attrs["data-image-label"] = self.fields[image_field].label

    def clean(self):
        cleaned_data = super().clean()
        for image_field in self.reusable_image_fields:
            picker_name = f"reuse_{image_field}"
            public_id = cleaned_data.get(picker_name)
            if not public_id:
                continue

            # Uploads and reuse must not ambiguously overwrite each other.
            if self.files.get(image_field):
                self.add_error(picker_name, "Choose either an uploaded file or an existing photo, not both.")
                continue
            if not settings.USE_CLOUDINARY or not settings.CLOUDINARY_URL:
                self.add_error(picker_name, "Cloudinary storage must be enabled to reuse an existing photo.")
                continue

            try:
                asset = cloudinary.api.resource(public_id, resource_type="image", type="upload")
            except CloudinaryError:
                logger.warning("Cloudinary could not verify a selected image.", exc_info=True)
                self.add_error(picker_name, "Unable to verify this Cloudinary photo. Try again.")
                continue

            if (
                asset.get("public_id") != public_id
                or asset.get("resource_type") != "image"
                or asset.get("type") != "upload"
            ):
                self.add_error(picker_name, "Select an existing, publicly deliverable Cloudinary image.")
                continue

            # Cloudinary's Django storage saves the public_id as the ImageField
            # name. A string is already committed, so no new upload occurs.
            cleaned_data[image_field] = public_id
        return cleaned_data


class CloudinaryPickerAdminMixin:
    """Adds a model-scoped, permission-checked browser endpoint under Django admin."""

    def get_urls(self):
        opts = self.model._meta
        name = f"{opts.app_label}_{opts.model_name}_cloudinary_images"
        custom = [
            path(
                "cloudinary-images/",
                self.admin_site.admin_view(self.cloudinary_images),
                name=name,
            )
        ]
        return custom + super().get_urls()

    def cloudinary_images(self, request):
        if not (self.has_add_permission(request) or self.has_change_permission(request)):
            raise PermissionDenied
        if request.method != "GET":
            return HttpResponseNotAllowed(["GET"])
        if not settings.USE_CLOUDINARY or not settings.CLOUDINARY_URL:
            return JsonResponse({"error": "Cloudinary storage is not enabled."}, status=503)

        prefix = request.GET.get("q", "").strip()
        cursor = request.GET.get("cursor", "").strip()
        if len(prefix) > 100 or len(cursor) > 2048:
            return JsonResponse({"error": "Invalid search or page token."}, status=400)

        options = {
            "resource_type": "image",
            "type": "upload",
            "max_results": PAGE_SIZE,
        }
        if prefix:
            options["prefix"] = prefix
        if cursor:
            options["next_cursor"] = cursor

        try:
            result = cloudinary.api.resources(**options)
        except CloudinaryError:
            logger.warning("Cloudinary photo browser is unavailable.", exc_info=True)
            return JsonResponse({"error": "Could not load Cloudinary photos. Please try again."}, status=502)

        images = []
        for item in result.get("resources", []):
            public_id = item.get("public_id", "")
            if not public_id or len(public_id) > MAX_PUBLIC_ID_LENGTH:
                continue
            if item.get("resource_type") != "image" or item.get("type") != "upload":
                continue
            images.append({
                "public_id": public_id,
                "preview_url": cloudinary.CloudinaryImage(public_id).build_url(
                    secure=True, width=240, height=180, crop="fill",
                    resource_type="image", type="upload",
                ),
            })
        return JsonResponse({"images": images, "next_cursor": result.get("next_cursor") or ""})
