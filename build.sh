#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate

# Create the production admin once when the temporary Render environment
# variables are present. Existing accounts are left unchanged on later deploys.
python manage.py shell <<'PY'
import os
from django.contrib.auth import get_user_model

username = os.getenv("DJANGO_SUPERUSER_USERNAME", "").strip()
email = os.getenv("DJANGO_SUPERUSER_EMAIL", "").strip()
password = os.getenv("DJANGO_SUPERUSER_PASSWORD", "")

if username and password:
    User = get_user_model()
    user, created = User.objects.get_or_create(
        username=username,
        defaults={"email": email, "is_staff": True, "is_superuser": True},
    )
    if created:
        user.set_password(password)
        user.save()
        print("Production superuser created.")
    else:
        print("Production superuser already exists; leaving it unchanged.")
else:
    print("Production superuser variables not set; skipping admin creation.")
PY
