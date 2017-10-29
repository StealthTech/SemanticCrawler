from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class ScanRequest(models.Model):
    user = models.ForeignKey('core.User', on_delete=models.CASCADE, verbose_name='Инициатор')
    url_list = models.TextField(verbose_name='Список ссылок')

    class Meta:
        verbose_name = 'запрос на сканирование'
        verbose_name_plural = 'запросы на сканирование'

    def __str__(self):
        return 'Запрос на сканирование №{}'.format(self.pk)


class ScanResult(models.Model):
    url = models.CharField(max_length=255, verbose_name='Ссылка')
    meta = models.TextField(verbose_name='Мета-информация')

    class Meta:
        verbose_name = 'результат сканирования'
        verbose_name_plural = 'результаты сканирования'

    def __str__(self):
        return 'Результат сканирования №{}'.format(self.pk)


@receiver(post_save, sender=ScanRequest)
def scan_websites(sender, instance, **kwargs):
    print('123')
