from django.contrib import admin
from .models import ExchangeRate
from .models import NasdaqIndex
# Register your models here.
admin.site.register(ExchangeRate)
admin.site.register(NasdaqIndex)