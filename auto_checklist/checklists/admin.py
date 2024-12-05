from django.contrib import admin
from .models import Element, Check, Category


class CheckInline(admin.TabularInline):
    model = Check
    extra = 0


class ElementAdmin(admin.ModelAdmin):
    list_display = ["element"]


class CategoryAdmin(admin.ModelAdmin):
    list_display = ["title"]


admin.site.register(Element, ElementAdmin)
admin.site.register(Category, CategoryAdmin)
