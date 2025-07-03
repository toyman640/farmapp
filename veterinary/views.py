from django.shortcuts import render
from drugapp.models import Dispatch, Drug, InventoryLog
from django.utils.timezone import localtime, now, localdate, timedelta
from django.db.models import Q
from itertools import chain
from django.db.models import F

# Create your views here.

def vet_index(request):
  today = localdate()
  now_time = now()
  last_24_hours = now_time - timedelta(hours=24)
  today_dispatches = Dispatch.objects.filter(dispatched_at__date=today)
  new_drugs = Drug.objects.filter(entered_at__gte=last_24_hours)
  restocked_logs = InventoryLog.objects.filter(updated_at__gte=last_24_hours,new_quantity__gt=F('previous_quantity')).select_related('drug')
  restocked_drugs = Drug.objects.filter(id__in=restocked_logs.values_list('drug_id', flat=True))
  combined_new_drugs = list(set(chain(new_drugs, restocked_drugs)))

  context = {
    'today_dispatches': Dispatch.objects.filter(dispatched_at__date=today),
    'today_date': today,
    'recent_drugs': combined_new_drugs,
  }

  return render(request, 'vet/index.html', context)
