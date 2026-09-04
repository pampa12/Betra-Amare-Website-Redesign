from django.urls import path
from django.views.generic import RedirectView

from . import views

app_name = "website"

urlpatterns = [
    path("", views.home, name="home"),
    path("portfolio/", views.portfolio, name="portfolio"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    path("inquire/", views.inquire, name="inquire"),
    path("robots.txt", views.robots_txt, name="robots"),
    path("sitemap.xml", views.sitemap_xml, name="sitemap"),

    # Keep old links working, but permanently redirect them to the clean URLs.
    path("index.html", RedirectView.as_view(pattern_name="website:home", permanent=True)),
    path("portfolio.html", RedirectView.as_view(pattern_name="website:portfolio", permanent=True)),
    path("about.html", RedirectView.as_view(pattern_name="website:about", permanent=True)),
    path("contact.html", RedirectView.as_view(pattern_name="website:contact", permanent=True)),
    path("inquire.html", RedirectView.as_view(pattern_name="website:inquire", permanent=True)),

    path("styles.css", views.legacy_asset, {"filename": "styles.css"}, name="styles"),
    path("script.js", views.legacy_asset, {"filename": "script.js"}, name="script"),
]
