from django.contrib import admin
from app.models import J2MUser, Balance, BalanceHistory, Referral, Documents, Binance, Thedex, Output, NFT, Form, \
    SendMessage, SendMessageForGroup, BalanceJ2M, EveryDayBalance, APIKeys, StabPool
from django.utils.html import format_html


class DocumentsAdmin(admin.ModelAdmin):
    readonly_fields = ("tg_id", "documents_approve", "it_product")
    list_display = ['tg_id', 'documents_approve', 'approve_contract']
    search_fields = ['tg_id_id__tg_id', 'tg_id_id__tg_username']

    def clickable_contract_link(self, obj):
        return format_html(f'<a href="{1}">{1}</a>', obj.contract)

    clickable_contract_link.short_description = 'Contract Link'


class OutputAdmin(admin.ModelAdmin):
    readonly_fields = ("tg_id", "amount", "date", "wallet")
    list_display = ['tg_id', 'amount', 'date', 'approve']
    list_filter = ['tg_id_id__tg_id', 'tg_id_id__tg_username', 'date', 'approve']


class J2MAdmin(admin.ModelAdmin):
    list_display = ['tg_id', 'tg_username', 'tg_name']
    search_fields = ['tg_id', 'tg_username']
    list_filter = ['tg_id', 'tg_username', 'tg_name']

    def has_delete_permission(self, request, obj=None):
        return False


class BalanceAdmin(admin.ModelAdmin):
    list_display = ['id', 'tg_id', 'balance', 'deposit']
    search_fields = ['id', 'tg_id_id__tg_id', 'tg_id_id__tg_username']
    list_filter = ['id', 'tg_id_id__tg_id', 'tg_id_id__tg_username', 'balance']


class BalanceHistoryAdmin(admin.ModelAdmin):
    list_display = ['tg_id', 'transaction', 'transaction_type', 'date']
    search_fields = ['tg_id_id__tg_id', 'tg_id_id__tg_username']
    list_filter = ['tg_id_id__tg_id', 'tg_id_id__tg_username', 'date']


class ReferralAdmin(admin.ModelAdmin):
    list_display = ['tg_id', 'line_1', 'line_2', 'line_3']
    search_fields = ['tg_id_id__tg_id', 'tg_id_id__tg_username']


class BinanceAdmin(admin.ModelAdmin):
    list_display = ['id', 'tg_id', 'balance_j2m', 'deposit', 'balance_binance']
    search_fields = ['id', 'tg_id_id__tg_id', 'tg_id_id__tg_username']


class ThedexAdmin(admin.ModelAdmin):
    list_display = ['tg_id', 'amount', 'status', 'date']
    search_fields = ['tg_id_id__tg_id', 'tg_id_id__tg_username']
    list_filter = ['tg_id_id__tg_id', 'tg_id_id__tg_username', 'date', 'status']


class NFTAdmin(admin.ModelAdmin):
    list_display = ['id', 'tg_id', 'status', 'date']
    search_fields = ['tg_id_id__tg_id', 'tg_id_id__tg_username']
    list_filter = ['tg_id_id__tg_id', 'tg_id_id__tg_username', 'date', 'status']


class FormAdmin(admin.ModelAdmin):
    readonly_fields = ("tg_id", "name", "social")
    list_display = ["tg_id", "name", "social"]
    search_fields = ['tg_id_id__tg_id', 'tg_id_id__tg_username']
    list_filter = ['tg_id_id__tg_id', 'tg_id_id__tg_username']


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


class StabpoolAdmin(admin.ModelAdmin):
    list_display = ['tg_id', 'balance', 'deposit', 'withdrawal', 'hold', 'weekly_profit']


admin.site.register(J2MUser, J2MAdmin)
admin.site.register(Balance, BalanceAdmin)
admin.site.register(BalanceHistory, BalanceHistoryAdmin)
admin.site.register(Referral, ReferralAdmin)
admin.site.register(Documents, DocumentsAdmin)
admin.site.register(Binance, BinanceAdmin)
admin.site.register(Thedex, ThedexAdmin)
admin.site.register(Output, OutputAdmin)
admin.site.register(NFT, NFTAdmin)
admin.site.register(Form, FormAdmin)
admin.site.register(SendMessage, SendMessageAdmin)
admin.site.register(SendMessageForGroup, SendMessageForGroupAdmin)
admin.site.register(BalanceJ2M, BalanceJ2MAdmin)
admin.site.register(EveryDayBalance, EveryDayBalanceAdmin)
admin.site.register(APIKeys, J2MBinanceAdmin)
admin.site.register(StabPool, StabpoolAdmin)
