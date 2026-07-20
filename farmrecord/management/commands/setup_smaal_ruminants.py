import random
from datetime import date
from django.core.management.base import BaseCommand
from django.utils import timezone
from farmrecord.models import Animals, AnimalType, EventType, Census, CensusRecord

class Command(BaseCommand):
    help = 'Clear and repopulate Sheep data'

    def handle(self, *args, **kwargs):
        # 1. Cleanup: Target only 'sheep'
        animals = Animals.objects.filter(animal_name='sheep')
        
        EventType.objects.filter(animal__in=animals).delete()
        Census.objects.filter(animal__in=animals).delete()
        
        self.stdout.write("Old sheep data cleared.")

        # 2. Setup Loop
        event_types = ['mortality', 'culling', 'sale', 'procurement', 'lambing', 'kidding']
        
        for month in range(1, 8):  # Jan to July
            current_date = date(2026, month, 15)
            
            for animal in animals:
                # Create 5 events per month
                for _ in range(5):
                    EventType.objects.create(
                        animal=animal,
                        event_name=random.choice(event_types),
                        number_of_animals=random.randint(1, 5),
                        event_date=current_date,
                        location="Pen 1"
                    )
                
                # Create Census for the month
                c = Census.objects.create(animal=animal, census_date=current_date)
                
                # Add a record for each animal type
                for at in AnimalType.objects.filter(animal=animal):
                    CensusRecord.objects.create(
                        census=c,
                        animal_type=at,
                        number_of_animals=random.randint(72, 120)
                    )
                c.update_total()

        self.stdout.write(self.style.SUCCESS("Successfully repopulated Sheep data."))