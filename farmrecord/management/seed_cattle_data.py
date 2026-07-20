import random
from datetime import date, timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from farmrecord.models import Animals, AnimalType, EventType, Census, CensusRecord

class Command(BaseCommand):
    help = 'Seed cattle paddock events and census records from Jan 2026 to July 2026'

    def handle(self, *args, **kwargs):
        cattle = Animals.objects.get(animal_name='cattle')
        animal_types = AnimalType.objects.filter(animal=cattle)
        
        start_date = date(2026, 1, 1)
        today = date.today()
        
        # 1. Generate one Census per month
        current_date = start_date
        while current_date <= today:
            if current_date.day == 1:
                census = Census.objects.create(
                    animal=cattle,
                    census_date=current_date,
                    notes=f"Auto-generated census for {current_date.strftime('%B %Y')}"
                )
                # Add a few records to the census
                for atype in animal_types[:3]: # Add a few random types
                    CensusRecord.objects.create(
                        census=census,
                        animal_type=atype,
                        number_of_animals=random.randint(10, 50)
                    )
                census.update_total()
                self.stdout.write(f"Created census for {current_date}")

            # 2. Generate 7 random events per month
            # We add 7 events randomly distributed within the current month
            for _ in range(7):
                event_day = random.randint(1, 28)
                event_date = date(current_date.year, current_date.month, event_day)
                
                # Pick a random location from the PADDOCK_LOCATIONS list
                location = random.choice([loc[0] for loc in EventType.PADDOCK_LOCATIONS])
                
                EventType.objects.create(
                    animal=cattle,
                    animal_type=random.choice(animal_types),
                    event_name=random.choice(['calving', 'mortality', 'treatment', 'vaccination', 'sale']),
                    location=location,
                    number_of_animals=random.randint(1, 5),
                    event_date=event_date,
                    designation="Auto-generated seed data"
                )
            
            # Move to next month
            current_date = (current_date.replace(day=1) + timedelta(days=32)).replace(day=1)

        self.stdout.write(self.style.SUCCESS("Successfully seeded data!"))