from django.db import models


class Text(models.Model):
    action = models.TextField(verbose_name="Расположение текста", unique=True, null=False)
    russian = models.TextField(verbose_name="Текст на русском", null=False)
    english = models.TextField(verbose_name="Текст на английском", null=False)

    class Meta:
        verbose_name = 'Текст в боте'
        verbose_name_plural = 'Тексты в боте'
