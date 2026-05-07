from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.db.models import Prefetch

from .models import Census, CensusRecord


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
      'other/index.html',
      context
  )