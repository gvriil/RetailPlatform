# network/admin.py
from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from .models import NetworkNode, Product


@admin.action(description=_("Clear debt for selected nodes"))
def clear_debt(modeladmin, request, queryset):
    """
    Admin action to clear debt for selected NetworkNode objects.
    Sets debt to 0 for all objects in the queryset.
    """
    updated = queryset.update(debt=0)
    modeladmin.message_user(
        request, _(f"Debt cleared for {updated} selected network nodes.")
    )


class NetworkNodeAdmin(admin.ModelAdmin):
    """
    Admin configuration for NetworkNode model.
    Provides customized list display, filtering, and actions.
    """

    list_display = (
        "name",
        "node_type",
        "city",
        "supplier_link",
        "debt",
        "level",
        "created_at",
    )
    list_filter = ("city", "country", "node_type", "level")
    search_fields = ("name", "email", "city", "country")
    readonly_fields = ("created_at", "level")
    actions = [clear_debt]

    def supplier_link(self, obj):
        """
        Creates a clickable link to the supplier node in the admin interface.

        Args:
            obj: The NetworkNode instance

        Returns:
            SafeString: HTML formatted link to supplier or "-" if no supplier
        """
        if obj.supplier:
            url = reverse("admin:network_networknode_change",
                          args=[obj.supplier.id])
            return format_html('<a href="{}">{}</a>', url, obj.supplier.name)
        return "-"

    supplier_link.short_description = _("Supplier")


class ProductAdmin(admin.ModelAdmin):
    """
    Admin configuration for Product model.
    """

    list_display = ("name", "model", "release_date", "price", "quantity")
    list_filter = ("release_date",)
    search_fields = ("name", "model")
    filter_horizontal = ("nodes",)  # Better UI for many-to-many relationship


# Register all models with their admin classes
admin.site.register(NetworkNode, NetworkNodeAdmin)
admin.site.register(Product, ProductAdmin)
