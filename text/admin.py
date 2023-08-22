from django.contrib import admin
from text.models import Text


class TextAdmin(admin.ModelAdmin):
    list_display = ['action', 'russian', 'english']


admin.site.register(Text, TextAdmin)
