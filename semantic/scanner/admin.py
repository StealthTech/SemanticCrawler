from django.contrib import admin

from .models import ScanRequest, ScanResult

admin.site.register(ScanRequest)
admin.site.register(ScanResult)
