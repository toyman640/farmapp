from django.core.management.base import BaseCommand
from django.db.models import Sum
from farmrecord.models import Census, CensusProjection, PiggeryCensusRecord
from main.services import run_projection_calculation

class Command(BaseCommand):
    help = 'Populate missing or inaccurate CensusProjection records'

    def handle(self, *args, **kwargs):
        # 1. Fetch all censuses in chronological order
        censuses = Census.objects.all().order_by('census_date')

        for census in censuses:
            # Find the baseline census immediately before this one
            prev_census = Census.objects.filter(
                animal=census.animal, 
                census_date__lt=census.census_date
            ).order_by('-census_date').first()

            if prev_census:
                # Calculate starting baseline count
                if census.animal.animal_name.lower() == 'pig':
                    piggery_data = PiggeryCensusRecord.objects.filter(census=prev_census)\
                        .exclude(line__name__icontains='croc').exclude(line__name__icontains='goose')\
                        .aggregate(gen=Sum('number'), pig=Sum('total_piglets'))
                    start_count = (piggery_data['gen'] or 0) + (piggery_data['pig'] or 0)
                else:
                    start_count = prev_census.total_animals

                # Calculate projection math using the baseline date
                # data = run_projection_calculation(census.animal, prev_census.census_date, start_count)
                data = run_projection_calculation(
                    animal_obj=census.animal, 
                    start_date=prev_census.census_date, 
                    end_date=census.census_date, # Explicitly pass the end date
                    start_count=start_count
                )

                # Use update_or_create to overwrite buggy/null projections
                projection, created = CensusProjection.objects.update_or_create(
                    census=census,
                    defaults={
                        'start_count': data['start_count'],
                        'projected_count': data['projected_count'],
                        'total_mortality': data['total_mortality'],
                        'total_culling': data['total_culling'],
                        'total_sale': data['total_sale'],
                        'total_gift': data['total_gift'],
                        'total_births': data['total_births'],
                        'total_procurement': data['total_procurement']
                    }
                )
                status = "Created" if created else "Updated"
                self.stdout.write(self.style.SUCCESS(f'{status} projection for census dated {census.census_date}'))