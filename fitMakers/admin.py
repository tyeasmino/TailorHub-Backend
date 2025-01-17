from django.contrib import admin
from . import models


# Register your models here.
class ServiceAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',),}


admin.site.register(models.Service, ServiceAdmin)
admin.site.register(models.FitMaker)
admin.site.register(models.Category)
admin.site.register(models.Dress)
admin.site.register(models.DressRating)

