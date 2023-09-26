from django.contrib import admin, messages
from weekly.models import WeeklyBalance


@admin.register(WeeklyBalance)
class WeeklyBalanceAdmin(admin.ModelAdmin):
    list_display = [
        'date', 'collective_profit', 'stabpool_profit', 'is_withdrawal'
    ]

    def add_view(self, request, form_url='', extra_context=None):
        self.message_user(
            request, "Обратите внимание, что при нажатии 'Сохранить' время создания нового объекта "
                     "может занять около 10 минут, не прерывайте этот процесс во избежание потери данных!",
            level=messages.WARNING)
        return super().add_view(request, form_url=form_url, extra_context=extra_context)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        self.message_user(
            request, "Обратите внимание, что при нажатии кнопки 'Сохранить' редактирование объекта может занять "
                     "около 10 минут, не прерывайте этот процесс во избежание потери данных!",
            level=messages.WARNING)
        return super().change_view(request, object_id, form_url=form_url, extra_context=extra_context)
