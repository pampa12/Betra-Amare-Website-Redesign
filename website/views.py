import json
import re
import time
from html import escape as html_escape
from xml.sax.saxutils import escape as xml_escape

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse

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
DEFAULT_SOCIAL_IMAGE = (
    "https://raw.githubusercontent.com/pampa12/Betraamarewebsite/"
    "main/assets/photos/betra-07.jpg"
)
CLEAN_INTERNAL_LINKS = {
    "/index.html": "/",
    "/portfolio.html": "/portfolio/",
    "/about.html": "/about/",
    "/contact.html": "/contact/",
    "/inquire.html": "/inquire/",
}
INQUIRY_COOLDOWN_SECONDS = 30

ACCESSIBILITY_STYLES = """
  <style id="accessibility-enhancements">
    .skip-link {
      position: fixed;
      top: 12px;
      left: 12px;
      z-index: 10000;
      padding: 11px 16px;
      background: #fff;
      color: #4a2435;
      border: 2px solid #4a2435;
      border-radius: 4px;
      font: 700 0.78rem/1.2 'DM Sans', Arial, sans-serif;
      text-decoration: none;
      transform: translateY(-180%);
      transition: transform .18s ease;
    }
    .skip-link:focus { transform: translateY(0); }

    a:focus-visible,
    button:focus-visible,
    input:focus-visible,
    textarea:focus-visible,
    select:focus-visible,
    [tabindex]:focus-visible {
      outline: 3px solid #a65477;
      outline-offset: 4px;
    }

    .hp-field {
      position: absolute !important;
      width: 1px !important;
      height: 1px !important;
      padding: 0 !important;
      margin: -1px !important;
      overflow: hidden !important;
      clip: rect(0, 0, 0, 0) !important;
      white-space: nowrap !important;
      border: 0 !important;
    }

    @media (prefers-reduced-motion: reduce) {
      html { scroll-behavior: auto !important; }
      *, *::before, *::after {
        animation-duration: .01ms !important;
        animation-iteration-count: 1 !important;
        transition-duration: .01ms !important;
        scroll-behavior: auto !important;
      }
    }
  </style>
"""

PERFORMANCE_HINTS = """
  <link rel="preconnect" href="https://raw.githubusercontent.com" crossorigin>
  <link rel="dns-prefetch" href="//raw.githubusercontent.com">
"""


def _analytics_tags():
    """Return Google Analytics markup only when a valid measurement ID is configured."""
    measurement_id = getattr(settings, "GA_MEASUREMENT_ID", "").strip()
    if not re.fullmatch(r"G-[A-Z0-9]+", measurement_id, flags=re.I):
        return ""

    safe_id = measurement_id.upper()
    return f"""
  <script async src="https://www.googletagmanager.com/gtag/js?id={safe_id}"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){{dataLayer.push(arguments);}}
    gtag('js', new Date());
    gtag('config', '{safe_id}', {{'anonymize_ip': true}});
  </script>
"""


def _optimize_image_tag(match):
    """Add browser loading hints without changing template-managed image URLs."""
    tag = match.group(0)
    lower_tag = tag.lower()
    additions = []

    if "decoding=" not in lower_tag:
        additions.append('decoding="async"')

    if "hero-photo" in lower_tag:
        if "loading=" not in lower_tag:
            additions.append('loading="eager"')
        if "fetchpriority=" not in lower_tag:
            additions.append('fetchpriority="high"')
    elif "loading=" not in lower_tag:
        additions.append('loading="lazy"')

    if not additions:
        return tag

    return f"{tag[:-1]} {' '.join(additions)}>"


def _finish_page(request, response, *, title, description, route_name, contact_content=None):
    """Normalize links and add SEO, accessibility, privacy, and performance enhancements."""
    html = response.content.decode("utf-8").replace(GITHUB_PAGES_BASE, "")

    for old_url, clean_url in CLEAN_INTERNAL_LINKS.items():
        html = html.replace(old_url, clean_url)

    # Route site CSS and JavaScript through Django's staticfiles app.
    html = html.replace('href="/styles.css"', 'href="/static/css/styles.css"')
    html = html.replace('src="/script.js"', 'src="/static/js/script.js"')

    # Make the privacy policy reachable from every page footer.
    if 'href="/privacy/"' not in html and '<div class="footer-nav">' in html:
        html = html.replace(
            '<div class="footer-nav">',
            '<div class="footer-nav"><a href="/privacy/">Privacy</a>',
            1,
        )

    # Improve image loading: prioritize the hero and defer below-the-fold imagery.
    html = re.sub(r"<img\b[^>]*>", _optimize_image_tag, html, flags=re.I)

    # The shared script is non-critical for initial HTML rendering.
    html = html.replace(
        '<script src="/static/js/script.js"></script>',
        '<script src="/static/js/script.js" defer></script>',
    )

    # Give keyboard users a direct route to the page content.
    if 'id="main-content"' not in html:
        html = html.replace(
            "<main>",
            '<main id="main-content" tabindex="-1">',
            1,
        )
    if 'class="skip-link"' not in html:
        html = html.replace(
            "<body>",
            '<body id="top">\n  <a class="skip-link" href="#main-content">Skip to main content</a>',
            1,
        )

    # Make the mobile-menu relationship explicit for assistive technology.
    html = html.replace(
        'id="menuToggle" aria-label="Open navigation" aria-expanded="false"',
        'id="menuToggle" aria-label="Open navigation" aria-expanded="false" aria-controls="mainNav"',
    )

    # Use a real target for existing back-to-top links.
    html = html.replace('href="#">Back to top', 'href="#top">Back to top')

    canonical_url = request.build_absolute_uri(reverse(route_name))
    home_url = request.build_absolute_uri(reverse("website:home"))

    instagram_url = (
        contact_content.instagram_url
        if contact_content and contact_content.instagram_url
        else "https://www.instagram.com/betra_amare"
    )
    tiktok_url = (
        contact_content.tiktok_url
        if contact_content and contact_content.tiktok_url
        else "https://www.tiktok.com/@betraamarey"
    )

    # Remove older SEO tags so every page has one clean, authoritative set.
    html = re.sub(r"\s*<title>.*?</title>", "", html, count=1, flags=re.I | re.S)
    html = re.sub(
        r"\s*<meta\s+name=[\"']description[\"'][^>]*>",
        "",
        html,
        flags=re.I,
    )
    html = re.sub(
        r"\s*<meta\s+(?:property|name)=[\"'](?:og:|twitter:)[^\"']+[\"'][^>]*>",
        "",
        html,
        flags=re.I,
    )
    html = re.sub(
        r"\s*<link\s+rel=[\"']canonical[\"'][^>]*>",
        "",
        html,
        flags=re.I,
    )

    structured_data = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "Person",
                "@id": f"{home_url}#person",
                "name": "Betra Amare",
                "url": home_url,
                "jobTitle": "Model and Digital Creator",
                "sameAs": [instagram_url, tiktok_url],
            },
            {
                "@type": "WebSite",
                "@id": f"{home_url}#website",
                "url": home_url,
                "name": "Betra Amare",
                "publisher": {"@id": f"{home_url}#person"},
            },
            {
                "@type": "WebPage",
                "@id": f"{canonical_url}#webpage",
                "url": canonical_url,
                "name": title,
                "description": description,
                "isPartOf": {"@id": f"{home_url}#website"},
                "about": {"@id": f"{home_url}#person"},
            },
        ],
    }
    structured_json = json.dumps(structured_data, ensure_ascii=False).replace("</", "<\\/")

    safe_title = html_escape(title, quote=True)
    safe_description = html_escape(description, quote=True)
    safe_canonical = html_escape(canonical_url, quote=True)

    seo_tags = f"""
  <title>{safe_title}</title>
  <meta name="description" content="{safe_description}">
  <link rel="canonical" href="{safe_canonical}">
  <meta property="og:title" content="{safe_title}">
  <meta property="og:description" content="{safe_description}">
  <meta property="og:type" content="website">
  <meta property="og:url" content="{safe_canonical}">
  <meta property="og:image" content="{DEFAULT_SOCIAL_IMAGE}">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{safe_title}">
  <meta name="twitter:description" content="{safe_description}">
  <meta name="twitter:image" content="{DEFAULT_SOCIAL_IMAGE}">
  <script type="application/ld+json">{structured_json}</script>
{PERFORMANCE_HINTS}{ACCESSIBILITY_STYLES}{_analytics_tags()}"""

    html = html.replace("</head>", f"{seo_tags}</head>", 1)
    return HttpResponse(html)


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
    return _finish_page(
        request,
        response,
        title="Betra Amare | Model & Digital Creator",
        description=(
            "Betra Amare is a model and digital creator producing polished beauty, "
            "fashion, lifestyle, and brand content with an authentic editorial feel."
        ),
        route_name="website:home",
        contact_content=contact_content,
    )


def portfolio(request):
    """Render active portfolio items and editable portfolio page copy."""
    portfolio_items = PortfolioItem.objects.filter(active=True)
    portfolio_content = PortfolioPageContent.objects.first()
    contact_content = ContactContent.objects.first()
    response = render(
        request,
        "portfolio.html",
        {
            "portfolio_items": portfolio_items,
            "portfolio_content": portfolio_content,
            "contact_content": contact_content,
        },
    )
    return _finish_page(
        request,
        response,
        title="Portfolio | Betra Amare — Beauty, Fashion & Lifestyle",
        description=(
            "Explore Betra Amare's selected modeling and creator work across beauty, "
            "fashion, lifestyle, editorial, and brand content."
        ),
        route_name="website:portfolio",
        contact_content=contact_content,
    )


def about(request):
    """Render editable About page content from Django admin."""
    about_content = AboutContent.objects.first()
    contact_content = ContactContent.objects.first()
    response = render(
        request,
        "about.html",
        {"about_content": about_content, "contact_content": contact_content},
    )
    return _finish_page(
        request,
        response,
        title="About Betra Amare | Model & Digital Creator",
        description=(
            "Meet Betra Amare, a model and digital creator focused on confident, "
            "feminine beauty, fashion, lifestyle, and authentic visual storytelling."
        ),
        route_name="website:about",
        contact_content=contact_content,
    )


def contact(request):
    """Render editable Contact page content from Django admin."""
    contact_content = ContactContent.objects.first()
    response = render(request, "contact.html", {"contact_content": contact_content})
    return _finish_page(
        request,
        response,
        title="Contact Betra Amare | Creator & Model",
        description=(
            "Contact Betra Amare for general questions and social communication, "
            "or use the inquiry page for brand collaborations and project work."
        ),
        route_name="website:contact",
        contact_content=contact_content,
    )


def inquire(request):
    """Save collaboration inquiries with lightweight bot and repeat-submit protection."""
    success = False
    inquiry_content = InquiryPageContent.objects.first()
    contact_content = ContactContent.objects.first()

    if request.method == "POST":
        form = InquiryForm(request.POST)
        if form.is_valid():
            now = time.time()
            last_submit = float(request.session.get("last_inquiry_submit_at", 0) or 0)
            if now - last_submit < INQUIRY_COOLDOWN_SECONDS:
                form.add_error(
                    None,
                    "That was submitted very recently. Please wait a moment before sending another inquiry.",
                )
            else:
                form.save()
                request.session["last_inquiry_submit_at"] = now
                form = InquiryForm()
                success = True
    else:
        form = InquiryForm()

    response = render(
        request,
        "inquire.html",
        {
            "form": form,
            "success": success,
            "inquiry_content": inquiry_content,
            "contact_content": contact_content,
        },
    )
    return _finish_page(
        request,
        response,
        title="Work With Betra Amare | Brand & Creator Inquiries",
        description=(
            "Send a project inquiry to Betra Amare for brand campaigns, UGC, modeling, "
            "beauty, fashion, lifestyle, and paid creator collaborations."
        ),
        route_name="website:inquire",
        contact_content=contact_content,
    )


def privacy(request):
    """Render the website privacy policy."""
    contact_content = ContactContent.objects.first()
    response = render(request, "privacy.html", {"contact_content": contact_content})
    return _finish_page(
        request,
        response,
        title="Privacy Policy | Betra Amare",
        description=(
            "Read how the Betra Amare website handles inquiry information, essential cookies, "
            "analytics, and privacy requests."
        ),
        route_name="website:privacy",
        contact_content=contact_content,
    )


def robots_txt(request):
    """Tell search engines which parts of the site may be crawled."""
    sitemap_url = request.build_absolute_uri(reverse("website:sitemap"))
    body = "\n".join(
        [
            "User-agent: *",
            "Allow: /",
            "Disallow: /admin/",
            f"Sitemap: {sitemap_url}",
        ]
    )
    return HttpResponse(body, content_type="text/plain; charset=utf-8")


def sitemap_xml(request):
    """Provide a simple XML sitemap for the public website pages."""
    route_names = [
        "website:home",
        "website:portfolio",
        "website:about",
        "website:contact",
        "website:inquire",
        "website:privacy",
    ]
    urls = [request.build_absolute_uri(reverse(name)) for name in route_names]
    entries = "".join(f"<url><loc>{xml_escape(url)}</loc></url>" for url in urls)
    xml = (
        '<?xml version="1.0" encoding="UTF-8"?>'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
        f"{entries}"
        "</urlset>"
    )
    return HttpResponse(xml, content_type="application/xml; charset=utf-8")


def legacy_asset(request, filename):
    """Serve the existing CSS and JavaScript locally for older cached links."""
    content_types = {
        "styles.css": "text/css",
        "script.js": "application/javascript",
    }
    if filename not in content_types:
        return HttpResponse(status=404)

    asset_path = settings.BASE_DIR / filename
    if not asset_path.exists():
        return HttpResponse(status=404)

    response = HttpResponse(
        asset_path.read_text(encoding="utf-8"),
        content_type=content_types[filename],
    )
    if not settings.DEBUG:
        response["Cache-Control"] = "public, max-age=604800, immutable"
    return response
