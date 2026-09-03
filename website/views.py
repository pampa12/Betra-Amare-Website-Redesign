from django.conf import settings
from django.http import Http404, HttpResponse
from django.shortcuts import render


GITHUB_PAGES_BASE = "https://pampa12.github.io/Betra-Amare-Website-Redesign"


def home(request):
    """Render the Django homepage while keeping all internal links on localhost."""
    response = render(request, "home.html")
    html = response.content.decode("utf-8").replace(GITHUB_PAGES_BASE, "")
    return HttpResponse(html)


def legacy_page(request, filename):
    """Serve the existing static site pages through Django during conversion."""
    allowed_pages = {"portfolio.html", "about.html", "contact.html", "inquire.html"}
    if filename not in allowed_pages:
        raise Http404

    page_path = settings.BASE_DIR / filename
    if not page_path.exists():
        raise Http404

    return HttpResponse(page_path.read_text(encoding="utf-8"), content_type="text/html")


def legacy_asset(request, filename):
    """Serve the existing CSS and JavaScript locally for the Django preview."""
    content_types = {
        "styles.css": "text/css",
        "script.js": "application/javascript",
    }
    if filename not in content_types:
        raise Http404

    asset_path = settings.BASE_DIR / filename
    if not asset_path.exists():
        raise Http404

    return HttpResponse(
        asset_path.read_text(encoding="utf-8"),
        content_type=content_types[filename],
    )
