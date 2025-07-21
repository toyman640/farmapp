from django.shortcuts import render
from drugapp.models import Dispatch, Drug, InventoryLog
from django.utils.timezone import localtime, now, localdate, timedelta
from django.db.models import Q
from itertools import chain
from django.db.models import F
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

# Create your views here.

# @login_required
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


# def dispatch_records(request):
#   dispatch_records = Dispatch.objects.order_by('-dispatched_at')

#   return render(request, 'vet/dispatch-records.html', {'dispatch_records' : dispatch_records})


# def dispatch_records_lazy(request):
#   page = request.GET.get('page', 1)
#   per_page = 10

#   dispatches = Dispatch.objects.order_by('-dispatched_at')
#   paginator = Paginator(dispatches, per_page)

#   current_page = paginator.get_page(page)

#   data = [
#       {
#           'drug': d.drug.drug_name,
#           'quantity': d.quantity,
#           'unit': d.unit.name,
#           'dispatched_at': d.dispatched_at.strftime('%Y-%m-%d %H:%M'),
#       }
#       for d in current_page
#   ]

#   return JsonResponse({'results': data, 'has_next': current_page.has_next()})

def dispatch_records_lazy(request):
    page = int(request.GET.get('page', 1))
    per_page = 10
    search = request.GET.get('search', '').strip()

    queryset = Dispatch.objects.select_related('drug', 'unit').order_by('-dispatched_at')

    if search:
        queryset = queryset.filter(drug__drug_name__icontains=search)

    paginator = Paginator(queryset, per_page)
    current_page = paginator.get_page(page)

    data = [
        {
            'drug': d.drug.drug_name,
            'quantity': d.quantity,
            'unit': d.unit.name,
            'dispatched_at': d.dispatched_at.strftime('%Y-%m-%d %H:%M'),
        }
        for d in current_page
    ]

    return JsonResponse({'results': data, 'has_next': current_page.has_next()})


def dispatch_view(request):
  return render(request, 'vet/dispatch-records.html')





def drugs_records_lazy(request):
  page = int(request.GET.get('page', 1))
  per_page = 10
  search = request.GET.get('search', '').strip()

  queryset = Drug.objects.select_related('unit').order_by('-entered_at')

  if search:
      queryset = queryset.filter(drug_name__icontains=search)

  paginator = Paginator(queryset, per_page)
  current_page = paginator.get_page(page)

  data = [
      {
        'manufacturer_name': d.manufacturer_name,
        'drug_name': d.drug_name,
        'batch_number': d.batch_number,
        'quantity': d.quantity,
        'unit': d.unit.name,
        'entered_at': d.entered_at.strftime('%Y-%m-%d %H:%M'),
      }
      for d in current_page
  ]

  return JsonResponse({'results': data, 'has_next': current_page.has_next()})





def drugs_view(request):
  return render(request, 'vet/drugs-records.html')
