from django.contrib import admin
from .models import DividendData, Holding

# Register your models here.

admin.site.register(DividendData)
admin.site.register(Holding)