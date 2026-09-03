from django.conf import settings
from django.http import Http404, HttpResponse
from django.shortcuts import render

from .forms import InquiryForm
from .models import HomepageContent, PortfolioItem


GITHUB_PAGES_BASE = "https://pampa12.github.io/Betra-Amare-Website-Redesign"


def home(request):
    """Render the Django homepage while keeping all internal links on localhost."""
    home_content = HomepageContent.objects.first()
    response = render(request, "home.html", {"home_content": home_content})
    html = response.content.decode("utf-8").replace(GITHUB_PAGES_BASE, "")
    return HttpResponse(html)


def portfolio(request):
    """Render active portfolio items managed through Django admin."""
    portfolio_items = PortfolioItem.objects.filter(active=True)
    return render(request, "portfolio.html", {"portfolio_items": portfolio_items})


def inquire(request):
    """Save collaboration inquiries and show them in Django admin."""
    success = False

    if request.method == "POST":
        form = InquiryForm(request.POST)
        if form.is_valid():
            form.save()
            form = InquiryForm()
            success = True
    else:
        form = InquiryForm()

    return render(request, "inquire.html", {"form": form, "success": success})


def legacy_page(request, filename):
    """Serve the remaining static site pages through Django during conversion."""
    allowed_pages = {"about.html", "contact.html"}
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
