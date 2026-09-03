from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render

from .forms import InquiryForm
from .models import (
    AboutContent,
    ContactContent,
    HomepageContent,
    InquiryPageContent,
    PortfolioItem,
    PortfolioPageContent,
)


GITHUB_PAGES_BASE = "https://pampa12.github.io/Betra-Amare-Website-Redesign"


def home(request):
    """Render the Django homepage with admin-managed content."""
    home_content = HomepageContent.objects.first()
    contact_content = ContactContent.objects.first()

    featured_items = PortfolioItem.objects.filter(active=True, featured=True)[:4]
    selected_items = list(featured_items)
    if not selected_items:
        selected_items = list(PortfolioItem.objects.filter(active=True)[:4])

    response = render(
        request,
        "home.html",
        {
            "home_content": home_content,
            "contact_content": contact_content,
            "selected_items": selected_items,
        },
    )
    html = response.content.decode("utf-8").replace(GITHUB_PAGES_BASE, "")
    return HttpResponse(html)


def portfolio(request):
    """Render active portfolio items and editable portfolio page copy."""
    portfolio_items = PortfolioItem.objects.filter(active=True)
    portfolio_content = PortfolioPageContent.objects.first()
    contact_content = ContactContent.objects.first()
    return render(
        request,
        "portfolio.html",
        {
            "portfolio_items": portfolio_items,
            "portfolio_content": portfolio_content,
            "contact_content": contact_content,
        },
    )


def about(request):
    """Render editable About page content from Django admin."""
    about_content = AboutContent.objects.first()
    contact_content = ContactContent.objects.first()
    return render(
        request,
        "about.html",
        {"about_content": about_content, "contact_content": contact_content},
    )


def contact(request):
    """Render editable Contact page content from Django admin."""
    contact_content = ContactContent.objects.first()
    return render(request, "contact.html", {"contact_content": contact_content})


def inquire(request):
    """Save collaboration inquiries and render editable inquiry-page copy."""
    success = False
    inquiry_content = InquiryPageContent.objects.first()
    contact_content = ContactContent.objects.first()

    if request.method == "POST":
        form = InquiryForm(request.POST)
        if form.is_valid():
            form.save()
            form = InquiryForm()
            success = True
    else:
        form = InquiryForm()

    return render(
        request,
        "inquire.html",
        {
            "form": form,
            "success": success,
            "inquiry_content": inquiry_content,
            "contact_content": contact_content,
        },
    )


def legacy_asset(request, filename):
    """Serve the existing CSS and JavaScript locally for the Django preview."""
    content_types = {
        "styles.css": "text/css",
        "script.js": "application/javascript",
    }
    if filename not in content_types:
        return HttpResponse(status=404)

    asset_path = settings.BASE_DIR / filename
    if not asset_path.exists():
        return HttpResponse(status=404)

    return HttpResponse(
        asset_path.read_text(encoding="utf-8"),
        content_type=content_types[filename],
    )
