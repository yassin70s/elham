from django.contrib import admin
from django.http import HttpRequest
from django.urls import path
from . import models

class MyAppAdmin(admin.ModelAdmin):
    pass
admin.site.register(models.MyApp,MyAppAdmin)

