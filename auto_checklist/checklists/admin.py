from django.contrib import admin
from .models import (
    Element,
    Check,
    Category,
    SubCategory,
    Recommendation
)


class CheckInline(admin.TabularInline):
    model = Check
    readonly_fields = ["image_tag"]
    extra = 0


class ElementAdmin(admin.ModelAdmin):
    list_display = ["element"]


class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ["title"]


class CategoryAdmin(admin.ModelAdmin):
    list_display = ["title"]


class RecommendationAdmin(admin.ModelAdmin):
    list_display = ["car", "element", "created_at"]


class CheckAdmin(admin.ModelAdmin):
    list_display = ['order', 'element', 'state', 'image_tag']
    readonly_fields = ['image_tag']


admin.site.register(Element, ElementAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(SubCategory, SubCategoryAdmin)
admin.site.register(Recommendation, RecommendationAdmin)
admin.site.register(Check, CheckAdmin)
