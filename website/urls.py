from django.urls import path
from . import views

app_name = "website"

urlpatterns = [
    path("", views.home, name="home"),
    path("index.html", views.home, name="home-html"),
    path("portfolio.html", views.legacy_page, {"filename": "portfolio.html"}, name="portfolio"),
    path("about.html", views.legacy_page, {"filename": "about.html"}, name="about"),
    path("contact.html", views.legacy_page, {"filename": "contact.html"}, name="contact"),
    path("inquire.html", views.legacy_page, {"filename": "inquire.html"}, name="inquire"),
    path("styles.css", views.legacy_asset, {"filename": "styles.css"}, name="styles"),
    path("script.js", views.legacy_asset, {"filename": "script.js"}, name="script"),
]
