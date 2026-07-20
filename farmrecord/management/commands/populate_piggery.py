import random
from datetime import date
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from farmrecord.models import Animals, EventType, Census, PiggeryCensusRecord, PiggeryLine

class Command(BaseCommand):
    help = 'Populate Piggery data'

    def handle(self, *args, **kwargs):
        user = get_user_model().objects.get(email='chat-test@skaalfarms.com')
        pig_animal = Animals.objects.get(animal_name='pig')
        lines = list(PiggeryLine.objects.all())
        event_types = ['mortality', 'farrowing', 'procurement', 'culling', 'sale', 'treatment', 'vaccination']

        for month in range(1, 8):  # Jan to July
            current_date = date(2026, month, 15)

            # 1. Create 7 Events
            for _ in range(7):
                EventType.objects.create(
                    animal=pig_animal,
                    event_name=random.choice(event_types),
                    number_of_animals=random.randint(1, 5),
                    event_date=current_date,
                    logged_by=user,
                    location="Line 1" # Default location for piggery
                )

            # 2. Create Census
            c = Census.objects.create(animal=pig_animal, census_date=current_date, logged_by=user)
            
            # Create records for random lines
            for line in random.sample(lines, min(len(lines), 3)):
                PiggeryCensusRecord.objects.create(
                    census=c,
                    line=line,
                    number=random.randint(100, 500),
                    total_piglets=random.randint(5, 20)
                )
            
            # 3. Update Totals (Trigger the custom update logic)
            c.update_total()

        self.stdout.write(self.style.SUCCESS("Successfully populated Piggery data."))