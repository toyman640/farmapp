from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Prefetch
from django.contrib import messages
from .models import Census, CensusRecord, ExoticAnimalCensus
from .forms import ExoticAnimalCensusForm
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.template.loader import render_to_string


@login_required
def supervisor_index(request):

  # Get latest census for each animal
  latest_pig = Census.objects.filter(
      animal__animal_name__iexact='pig'
  ).prefetch_related(
      Prefetch(
          'records',
          queryset=CensusRecord.objects.select_related('animal_type')
      )
  ).order_by('-census_date').first()


  latest_cattle = Census.objects.filter(
      animal__animal_name__iexact='cattle'
  ).prefetch_related(
      Prefetch(
          'records',
          queryset=CensusRecord.objects.select_related('animal_type')
      )
  ).order_by('-census_date').first()


  # Sheep + Goat stored together as sheep
  latest_small_ruminant = Census.objects.filter(
      animal__animal_name__iexact='sheep'
  ).prefetch_related(
      Prefetch(
          'records',
          queryset=CensusRecord.objects.select_related('animal_type')
      )
  ).order_by('-census_date').first()


  # Totals
  pig_total = latest_pig.total_animals if latest_pig else 0
  cattle_total = latest_cattle.total_animals if latest_cattle else 0

  sheep_total = 0
  goat_total = 0

  # Separate sheep/goat using animal_type
  if latest_small_ruminant:
      for record in latest_small_ruminant.records.all():

          animal_type = record.animal_type.animal_type_name.lower()
          count = record.number_of_animals

          # SHEEP
          if animal_type in [
              'ram',
              'ewe',
              'lamb',
              'weaner (sheep)'
          ]:
              sheep_total += count

          # GOAT
          elif animal_type in [
              'buck',
              'doe',
              'kid',
              'weaner (goat)'
          ]:
              goat_total += count


  context = {
      # Latest census objects
      'latest_pig': latest_pig,
      'latest_cattle': latest_cattle,
      'latest_small_ruminant': latest_small_ruminant,

      # Totals
      'pig_total': pig_total,
      'cattle_total': cattle_total,
      'sheep_total': sheep_total,
      'goat_total': goat_total,
  }

  return render(
      request,
      'exortic/index.html',
      context
  )



@login_required
def create_exotic_animal_census(request):

  if request.method == 'POST':
    form = ExoticAnimalCensusForm(request.POST)

    if form.is_valid():
      form.save()

      messages.success(
        request,
        'Census record created successfully.'
      )

      return redirect(
        'farmrecord:create_exotic_animal_census'
      )

  else:
    form = ExoticAnimalCensusForm()


  # Latest records
  latest_records = ExoticAnimalCensus.objects.order_by(
    '-census_date'
  )


  context = {
    'form': form,
    'latest_records': latest_records,
  }

  return render(
    request,
    'exortic/create_exotic_animal_census.html',
    context
  )

@login_required
def exotic_animal_census_records(request):

    records = ExoticAnimalCensus.objects.order_by(
        '-census_date',
        '-created_at'
    )

    animal_type = request.GET.get('animal_type')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    # FILTER BY ANIMAL TYPE
    if animal_type:
        records = records.filter(
            animal_name=animal_type
        )

    # FILTER BY START DATE
    if start_date:
        records = records.filter(
            census_date__gte=start_date
        )

    # FILTER BY END DATE
    if end_date:
        records = records.filter(
            census_date__lte=end_date
        )

    paginator = Paginator(records, 10)

    page_number = request.GET.get('page')

    page_obj = paginator.get_page(page_number)

    geese_total = sum(
        records.filter(
            animal_name='geese'
        ).values_list(
            'total_animals',
            flat=True
        )
    )

    crocodile_total = sum(
        records.filter(
            animal_name='crocodile'
        ).values_list(
            'total_animals',
            flat=True
        )
    )

    # AJAX REQUEST
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':

        html = render_to_string(
            'exortic/partials/exotic_animal_rows.html',
            {
                'records': page_obj,
                'page_obj': page_obj
            },
            request=request
        )

        return JsonResponse({
            'html': html,
            'has_next': page_obj.has_next()
        })

    context = {
        'records': page_obj,
        'page_obj': page_obj,
        'geese_total': geese_total,
        'crocodile_total': crocodile_total,

        'animal_type': animal_type,
        'start_date': start_date,
        'end_date': end_date,
    }

    return render(
        request,
        'exortic/exotic_animal_census_records.html',
        context
    )


# @login_required
# def exotic_animal_census_records(request):

#     records = ExoticAnimalCensus.objects.order_by(
#         '-census_date',
#         '-created_at'
#     )

#     search_query = request.GET.get('search')

#     if search_query:
#         records = records.filter(
#             animal_name__icontains=search_query
#         )

#     paginator = Paginator(records, 1)

#     page_number = request.GET.get('page')

#     page_obj = paginator.get_page(page_number)

#     geese_total = sum(
#         records.filter(
#             animal_name='geese'
#         ).values_list(
#             'total_animals',
#             flat=True
#         )
#     )

#     crocodile_total = sum(
#         records.filter(
#             animal_name='crocodile'
#         ).values_list(
#             'total_animals',
#             flat=True
#         )
#     )

#     # AJAX REQUEST
#     if request.headers.get('x-requested-with') == 'XMLHttpRequest':
#         print('AJAX HEADER:', request.headers.get('X-Requested-With'))
#         print('PAGE:', request.GET.get('page'))
#         html = render_to_string(
#             'exortic/partials/exotic_animal_rows.html',
#             {
#                 # 'records': page_obj.object_list
#                 'records': page_obj,
#                 'page_obj': page_obj
#             },
#             request=request
#         )

#         return JsonResponse({
#             'html': html,
#             'has_next': page_obj.has_next()
#         })

#     print('PAGE OBJECT:', list(page_obj))

#     context = {
#         'records': page_obj.object_list,
#         'page_obj': page_obj,
#         'geese_total': geese_total,
#         'crocodile_total': crocodile_total,
#         'search_query': search_query,
#     }

#     return render(
#         request,
#         'exortic/exotic_animal_census_records.html',
#         context
#     )

@login_required
def edit_exotic_animal_census(request, pk):

  record = get_object_or_404(
      ExoticAnimalCensus,
      pk=pk
  )

  if request.method == 'POST':

      form = ExoticAnimalCensusForm(
          request.POST,
          instance=record
      )

      if form.is_valid():

          form.save()

          messages.success(
              request,
              'Census record updated successfully.'
          )

          return redirect(
              'farmrecord:exotic_animal_census_records'
          )

  else:

      form = ExoticAnimalCensusForm(
          instance=record
      )

  context = {
      'form': form,
      'record': record,
  }

  return render(
      request,
      'exortic/edit_exotic_animal_census.html',
      context
  )



@login_required
def exotic_animal_census_detail(request, pk):

  record = get_object_or_404(
    ExoticAnimalCensus,
    pk=pk
  )

  print('record:', record)

  data = {
    'id': record.id,
    'animal_name': record.animal_name,
    'animal_display': record.get_animal_name_display(),
    'total_animals': record.total_animals,
    'census_date': record.census_date.strftime('%Y-%m-%d'),
    'notes': record.notes,
    'created_at': record.created_at.strftime('%Y-%m-%d %H:%M:%S'),
    'updated_at': record.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
  }
  print("Modal Data:", data)

  return JsonResponse(data)