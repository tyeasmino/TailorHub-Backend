from django.contrib import admin
from .models import DressType, DressMeasurement

# Register your models here.
class DressTypeAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',),}

admin.site.register(DressType, DressTypeAdmin)
admin.site.register(DressMeasurement)
