"""Email Betra when someone sends an inquiry, so no lead sits unseen in the admin."""
import logging
import threading

from django.conf import settings
from django.core.mail import EmailMessage
from django.urls import NoReverseMatch, reverse

logger = logging.getLogger(__name__)


def _admin_link(request, inquiry):
    try:
        return request.build_absolute_uri(reverse("admin:website_inquiry_change", args=[inquiry.pk]))
    except NoReverseMatch:
        return ""


def build_inquiry_alert(inquiry, request):
    subject = f"New inquiry from {inquiry.name}"
    if inquiry.company:
        subject += f" ({inquiry.company})"
    lines = [
        "You have a new inquiry from your website.",
        "",
        f"Name: {inquiry.name}",
        f"Email: {inquiry.email}",
    ]
    if inquiry.company:
        lines.append(f"Company / brand: {inquiry.company}")
    if inquiry.project_type:
        lines.append(f"Project type: {inquiry.project_type}")
    if inquiry.budget:
        lines.append(f"Budget: {inquiry.budget}")
    lines += ["", "Message:", inquiry.message, ""]
    lines.append("Reply to this email to answer them directly.")
    link = _admin_link(request, inquiry)
    if link:
        lines.append(f"See it in your admin: {link}")
    return EmailMessage(
        subject=subject,
        body="\n".join(lines),
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=list(settings.INQUIRY_ALERT_TO),
        reply_to=[inquiry.email],
    )


def _send(message):
    try:
        message.send(fail_silently=False)
    except Exception:  # The inquiry is already saved; a mail problem must not break the form.
        logger.exception("Could not send the inquiry alert email")


def send_inquiry_alert(inquiry, request):
    if not getattr(settings, "INQUIRY_ALERTS_ENABLED", False):
        return
    message = build_inquiry_alert(inquiry, request)
    if getattr(settings, "INQUIRY_ALERT_ASYNC", True):
        threading.Thread(target=_send, args=(message,), daemon=True).start()
    else:
        _send(message)
