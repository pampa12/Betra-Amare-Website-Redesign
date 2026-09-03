from django.contrib import admin

from .models import HomepageContent, Inquiry, PortfolioItem


@admin.register(HomepageContent)
class HomepageContentAdmin(admin.ModelAdmin):
    list_display = ("__str__", "updated_at")

    def has_add_permission(self, request):
        if HomepageContent.objects.exists():
            return False
        return super().has_add_permission(request)


@admin.register(PortfolioItem)
class PortfolioItemAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "featured", "active", "sort_order", "updated_at")
    list_filter = ("category", "featured", "active")
    search_fields = ("title", "alt_text")
    list_editable = ("featured", "active", "sort_order")


@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "company", "status", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("name", "email", "company", "message")
    readonly_fields = ("created_at",)


admin.site.site_header = "Betra Amare Administration"
admin.site.site_title = "Betra Amare Admin"
admin.site.index_title = "Website management"
