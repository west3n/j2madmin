from django.contrib import admin
from autoposting.models import Autoposting


@admin.register(Autoposting)
class AutopostingAdmin(admin.ModelAdmin):
    list_display = ['text', 'post_time', 'accept']
    readonly_fields = ['accept', 'send']
