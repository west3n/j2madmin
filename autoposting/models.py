from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


class Autoposting(models.Model):
    text = models.TextField(
        verbose_name='Текст поста', null=False, blank=False,
        help_text="HTML-теги: <b>Жирность</b> (&lt;b&gt;Жирность&lt;/b&gt;), "
                  "<em>Курсив</em> (&lt;em&gt;Курсив&lt;/em&gt;), "
                  "<a href=''>Ссылка</a> (&lt;a href='https://www.example.com'&gt;Ссылка&lt;/a&gt;)")
    image = models.ImageField(verbose_name='Картинка в посте', null=True, blank=True)
    post_time = models.DateTimeField(verbose_name='Время поста', null=False, blank=False)
    callback_name = models.CharField(verbose_name="Текст на кнопке", max_length=25, null=True, blank=True,
                                     help_text="Не забудьте добавить ссылку в форме ниже!")
    callback_url = models.URLField(verbose_name='Ссылка в кнопке', blank=True, null=True,
                                   help_text="Это поле нужно заполнять вместе с полем 'Текст на кнопке'")
    accept = models.BooleanField(verbose_name='Подтверждено?', default=False,
                                 help_text="Это поле заполняется автоматически после подтверждения")
    send = models.BooleanField(verbose_name='Отправлено?', default=False,
                               help_text="Это поле заполняется автоматически после отправки")

    class Meta:
        verbose_name = 'Автопостинг'
        verbose_name_plural = 'Автопостинг'

    def clean(self):
        if self.post_time < timezone.now():
            raise ValidationError('Время поста не может быть раньше текущего времени!')
        if self.callback_name and not self.callback_url:
            raise ValidationError('Кнопка не может быть без ссылки!')
        if self.callback_url and not self.callback_name:
            raise ValidationError('Ссылка не может быть без имени кнопки!')

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
