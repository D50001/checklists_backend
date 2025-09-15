import datetime

from django.db.models import QuerySet
from .models import Order, Department
from checklists.models import Element


def get_filtered_orders(department: Department | None = None) -> QuerySet[Order]:
    queryset = Order.objects.filter(
        created_at__date=datetime.date.today()
    ).prefetch_related("checks")
    if department:
        queryset = queryset.filter(department=department)
    elements_ids_count = Element.objects.all().values_list("id", flat=True).distinct().count()
    result = []
    for order in queryset:
        checks_count = order.checks.values_list("element__id", flat=True).distinct().count()
        if checks_count < elements_ids_count:
            result.append(order)
    return result

