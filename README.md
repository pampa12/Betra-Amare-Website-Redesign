# Betra Amare Website Redesign

A clean editorial portfolio and creator website for Betra Amare.

This repository is the new redesign workspace and is intentionally separate from the original website repository.

## Pages

- `index.html` — editorial homepage
- `portfolio.html` — filterable portfolio gallery
- `about.html` — personal about page
- `contact.html` — collaboration inquiry page
- `styles.css` — shared visual system and responsive styling
- `script.js` — mobile navigation, reveal animations, portfolio filtering, and contact-form behavior

## Design direction

The site uses a warm editorial look with large serif typography, restrained blush accents, generous whitespace, image-led layouts, and minimal navigation. It is inspired by high-end personal portfolio sites while keeping Betra's own creator identity and content.

## Photos

During the redesign stage, the site loads Betra's existing photo assets from the original public GitHub repository. This keeps the new codebase separate while allowing the redesign to be previewed immediately. The photos can be copied into this repository later before the original repository is retired.

## Preview

Open `index.html` locally, or enable GitHub Pages for the `main` branch to publish a live preview.

## Reuse photos already in Cloudinary (Django Admin)

The Django Admin now includes a **Choose from Cloudinary** button beside existing
image-upload fields on Homepage content, About page content, Media kit content,
Portfolio items, and Featured TikToks. Normal **Choose File** uploads still work.

1. In Render > `betra-amare` > Environment, keep `CLOUDINARY_URL` and
   `USE_CLOUDINARY=True` configured (do not share the URL or API secret).
2. Sign into `/admin/`, open an item, and click **Choose from Cloudinary**
   next to the relevant image field.
3. Browse images or search by the **beginning** of an image public ID, then click
   a thumbnail. Save the Django admin form. The existing Cloudinary resource is
   referenced by public ID; no duplicate upload occurs.
4. If you prefer to upload a new photo, use the normal file picker instead.
   Don't choose an existing photo and upload a new file in the same field.

The thumbnail browser lists only public-delivery image resources (`image/upload`)
through a staff-only, model-permission-checked Django endpoint. Each submitted
public ID is verified against Cloudinary using the server-side Admin API before
it is saved to the existing ImageField. API secrets are never sent to the browser.
Listing and validation use Cloudinary's rate-limited Admin API; large libraries
can be paginated. Images with IDs longer than the existing field's 100-character
limit are skipped. Nothing in this feature deletes or replaces Cloudinary assets.

Run the focused tests with:

```sh
python manage.py test website.tests_cloudinary_picker
```
