from django.contrib import admin
from promo.models import Promo


@admin.register(Promo)
class PromoAdmin(admin.ModelAdmin):
    readonly_fields = ['structure', 'percentage', 'date_end', 'balance', 'profit']

    def has_delete_permission(self, request, obj=None):
        return True

    def get_readonly_fields(self, request, obj=None):
        if obj:
            if obj.date_start is not None:
                return self.readonly_fields + ['date_start']
        return self.readonly_fields
