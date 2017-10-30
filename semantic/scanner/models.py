import json

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from utils.analytics.rss import Scanner


class ScanRequest(models.Model):
    user = models.ForeignKey('core.User', on_delete=models.CASCADE, verbose_name='Инициатор')
    url_list = models.TextField(verbose_name='Список ссылок')
    results = models.ManyToManyField('ScanResult', blank=True)
    finished = models.BooleanField(default=False, verbose_name='Выполнен')

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
        return 'Результат сканирования {}'.format(self.url)

    def verbose_meta(self):
        # return '{}: {}'.format()
        return '\n'.join(['{}: {}'.format(k, v) for k, v in json.loads(self.meta).items()])


@receiver(post_save, sender=ScanRequest)
def scan_websites(sender, instance, **kwargs):
    if instance.finished:
        return

    # TODO: Optimization
    urls = instance.url_list.replace(' ', '').replace('\n', ',').split(',')
    scanner = Scanner(urls)
    result = scanner.scan()

    current_entries = [i.url for i in ScanResult.objects.all()]

    if result:
        catalogue = result.get('catalogue')
        if catalogue:
            for v in catalogue.values():
                for entry in v:
                    if not entry.url in current_entries and entry.url:
                        scan_result = ScanResult(url=entry.url, meta=entry.to_json())
                        scan_result.save()
                        print('Trying to add:', scan_result)
                        instance.results.add(scan_result)
    instance.finished = True
    instance.save()


    # print(result)
    # if result:
    #     print({'{}: {}'.format(k, ', '.join([e.title for e in v])) for k, v in result['catalogue'].items()})
