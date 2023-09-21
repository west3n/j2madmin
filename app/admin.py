from django.contrib import admin
from django.db.models import Q
from django.urls import reverse
from django.utils.html import format_html

from app.models import J2MUser, Balance, BalanceHistory, Referral, Documents, Binance, Thedex, Output, NFT, Form, \
    SendMessage, SendMessageForGroup, BalanceJ2M, EveryDayBalance, APIKeys, StabPool
from django.contrib.auth.models import Group
from import_export import resources, fields
from import_export.admin import ImportExportMixin


class UsersResource(resources.ModelResource):
    class Meta:
        model = J2MUser


class OutputAdmin(admin.ModelAdmin):
    readonly_fields = ("tg_id", "amount", "date", "wallet")
    list_display = ['tg_id', 'amount', 'date', 'approve', 'decline']
    list_filter = ['tg_id_id__tg_id', 'tg_id_id__tg_username', 'date', 'approve', 'decline']


class J2MAdmin(admin.ModelAdmin):
    list_display = ['tg_id', 'tg_username', 'tg_name']
    list_display_links = ['tg_id', 'tg_username', 'tg_name']
    search_fields = ['tg_id', 'tg_username']
    list_filter = ['tg_id', 'tg_username', 'tg_name']

    def has_delete_permission(self, request, obj=None):
        return False


class TgIdWithReferralFilter(admin.SimpleListFilter):
    title = 'Пользователи с рефералами'
    parameter_name = 'tg_id_with_referral'

    def lookups(self, request, model_admin):
        tg_ids_with_referral = Referral.objects.values_list('tg_id', flat=True).distinct()
        tg_id_choices = []
        for tg_id in tg_ids_with_referral:
            try:
                j2m_user = J2MUser.objects.get(tg_id=tg_id)
                tg_id_choices.append((str(tg_id), f'{tg_id} ({j2m_user.tg_name})'))
            except J2MUser.DoesNotExist:
                pass
        return tg_id_choices

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(tg_id=self.value())
        return queryset


class ReferralAdmin(admin.ModelAdmin):
    list_display = ['tg_id', 'line_1_link', 'line_2_link', 'line_3_link']
    search_fields = ['tg_id_id__tg_id', 'tg_id_id__tg_username']
    list_filter = [TgIdWithReferralFilter]
    list_per_page = 5

    def get_j2m_users(self, obj):
        tg_ids = [obj.line_1, obj.line_2, obj.line_3]
        j2m_users = J2MUser.objects.filter(tg_id__in=tg_ids)
        return j2m_users

    def line_1_link(self, obj):
        j2m_users = self.get_j2m_users(obj)
        for j2m_user in j2m_users:
            if j2m_user.tg_id == obj.line_1:
                link = reverse("admin:app_j2muser_change", args=[j2m_user.tg_id])
                return format_html('<a href="{}">{}</a>', link, j2m_user)
        return obj.line_1
    line_1_link.short_description = 'Линия 1'

    def line_2_link(self, obj):
        j2m_users = self.get_j2m_users(obj)
        for j2m_user in j2m_users:
            if j2m_user.tg_id == obj.line_2:
                link = reverse("admin:app_j2muser_change", args=[j2m_user.tg_id])
                return format_html('<a href="{}">{}</a>', link, j2m_user)
        return obj.line_2
    line_2_link.short_description = 'Линия 2'

    def line_3_link(self, obj):
        j2m_users = self.get_j2m_users(obj)
        for j2m_user in j2m_users:
            if j2m_user.tg_id == obj.line_3:
                link = reverse("admin:app_j2muser_change", args=[j2m_user.tg_id])
                return format_html('<a href="{}">{}</a>', link, j2m_user)
        return obj.line_3
    line_3_link.short_description = 'Линия 3'


class ThedexAdmin(admin.ModelAdmin):
    list_display = ['tg_id', 'amount', 'status', 'date']
    search_fields = ['tg_id_id__tg_id', 'tg_id_id__tg_username']
    list_filter = ['tg_id_id__tg_id', 'tg_id_id__tg_username', 'date', 'status']


class SendMessageAdmin(admin.ModelAdmin):
    list_display = ["tg_id", "text"]

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    # def has_add_permission(self, request):
    #     return True


class SendMessageForGroupAdmin(admin.ModelAdmin):
    list_display = ["group", "text"]

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class BalanceJ2MAdmin(admin.ModelAdmin):
    list_display = ["date_monday", "balance_monday_usdt", "balance_monday_busd", "date_sunday",
                    "balance_sunday_usdt", "balance_sunday_busd", "profit"]

    # def has_change_permission(self, request, obj=None):
    #     return False

    def has_delete_permission(self, request, obj=None):
        return False

    # def has_add_permission(self, request):
    #     return False


class EveryDayBalanceAdmin(admin.ModelAdmin):
    list_display = ["date", "balance_usdt", "balance_busd", "total"]

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False


class J2MBinanceAdmin(admin.ModelAdmin):
    list_display = ["api_key", "description"]

    def has_change_permission(self, request, obj=None):
        return False


admin.site.register(J2MUser, J2MAdmin)
admin.site.register(Referral, ReferralAdmin)
admin.site.register(Thedex, ThedexAdmin)
admin.site.register(Output, OutputAdmin)
admin.site.register(SendMessage, SendMessageAdmin)
admin.site.register(SendMessageForGroup, SendMessageForGroupAdmin)
admin.site.register(BalanceJ2M, BalanceJ2MAdmin)
admin.site.register(EveryDayBalance, EveryDayBalanceAdmin)
admin.site.register(APIKeys, J2MBinanceAdmin)
admin.site.unregister(Group)
