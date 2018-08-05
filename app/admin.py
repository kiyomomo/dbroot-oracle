from django.contrib import admin

# Register your models here.
from .models import Item


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'user'
