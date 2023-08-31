from django.contrib import admin
from demo.models import DemoUser, DemoBalanceHistory, DemoStabPool


class DemoAdmin(admin.ModelAdmin):
    list_display = ["tg_id", "balance_collective", "deposit_collective", "balance_personal", "deposit_personal"]
    search_fields = ['tg_id_id__tg_id', 'tg_id_id__tg_username']
    list_filter = ['tg_id_id__tg_id', 'tg_id_id__tg_username']


class DemoBalanceHistoryAdmin(admin.ModelAdmin):
    list_display = ["tg_id", "transaction", "date", "amount", 'transaction_type']
    search_fields = ['tg_id_id__tg_id', 'tg_id_id__tg_username']
    list_filter = ['tg_id_id__tg_id', 'tg_id_id__tg_username']


class DemoStabPoolAdmin(admin.ModelAdmin):
    list_display = ['tg_id', 'balance', 'deposit', 'withdrawal', 'hold', 'weekly_profit']


admin.site.register(DemoUser, DemoAdmin)
admin.site.register(DemoBalanceHistory, DemoBalanceHistoryAdmin)
admin.site.register(DemoStabPool, DemoStabPoolAdmin)
