import django_filters
from .models import Dispatch

class DispatchFilter(django_filters.FilterSet):
  drug_name = django_filters.CharFilter(
    field_name='drug__drug_name', lookup_expr='icontains', label='Drug Name'
  )
  dispatched_at = django_filters.DateFromToRangeFilter(
    field_name='dispatched_at', label='Dispatch Date Range'
  )

  class Meta:
    model = Dispatch
    fields = ['drug_name', 'dispatched_at']
