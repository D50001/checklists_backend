from django.contrib import admin
from .models import Car, Order, Department
from checklists.admin import CheckInline


class CarAdmin(admin.ModelAdmin):
    list_display = ["id", "model", "year", "vin", "license_number"]
    list_filter = ["year"]
    list_display_links = ["vin", "license_number"]


class OrderAdmin(admin.ModelAdmin):
    list_display = ["number", "date", "created_at"]
    list_display_filter = ["date"]
    list_display_links = ["number"]
    inlines = [CheckInline]


class DepartmentAdmin(admin.ModelAdmin):
    list_display = ["title"]


admin.site.register(Car, CarAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Department, DepartmentAdmin)
