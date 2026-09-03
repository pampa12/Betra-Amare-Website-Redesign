from django.urls import path
from . import views

app_name = "website"

urlpatterns = [
    path("", views.home, name="home"),
    path("index.html", views.home, name="home-html"),
    path("portfolio.html", views.portfolio, name="portfolio"),
    path("about.html", views.about, name="about"),
    path("contact.html", views.contact, name="contact"),
    path("inquire.html", views.inquire, name="inquire"),
    path("styles.css", views.legacy_asset, {"filename": "styles.css"}, name="styles"),
    path("script.js", views.legacy_asset, {"filename": "script.js"}, name="script"),
]
