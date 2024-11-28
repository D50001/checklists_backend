from django.contrib import admin
from .models import Element, Check


class CheckInline(admin.TabularInline):
    model = Check
    extra = 0

class ElementAdmin(admin.ModelAdmin):
    list_display = ["element"]


admin.site.register(Element, ElementAdmin)
