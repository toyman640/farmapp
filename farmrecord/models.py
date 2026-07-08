from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from farmapp.utils import unique_slug_generator
from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver
from .validators import validate_file_size

# Create your models here.

class Userp(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    is_boss = models.BooleanField('Is boss', default=False)
    is_hr = models.BooleanField('Is hr', default=False)
    is_supervisor = models.BooleanField('Is supervisor', default=False)
    is_account = models.BooleanField('Is account', default=False)
    is_maintenance = models.BooleanField('Is maintenance', default=False)
    is_drug = models.BooleanField("Is drug", default=False)
    is_vet = models.BooleanField('Is vet', default=False)
    is_vet_piggery = models.BooleanField('Is vet piggery', default=False)
    is_vet_paddock = models.BooleanField('Is vet cattle', default=False)
    is_vet_smallruminant = models.BooleanField('Is vet small ruminant', default=False)


class Animals(models.Model):
    ANIMAL_CHOICES = [
        ('pig', 'Pig'),
        ('cattle', 'Cattle'),
        ('sheep', 'Sheep'),
        ('goat', 'Goat'),
    ]
    animal_name = models.CharField(max_length=20, choices=ANIMAL_CHOICES, unique=True)
    describe_animal = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.animal_name


class AnimalType(models.Model):
    ANIMAL_TYPE_CHOICES = [
        ('sow', 'Sow'),
        ('dry sow', "Dry Sow"),
        ('boar', 'Boar'),
        ('weaner (pig)', 'Weaner (Pig)'),
        ('piglet', 'Piglet'),
        ('cow', 'Cow'),
        ('bull', 'Bull'),
        ('gilt', 'Gilt'),
        ('hog', 'Hog'),
        ('weaner (cattle)', 'Weaner (Cattle)'),
        ('calf', 'Calf'),
        ('miniature cattle', 'Miniature Cattle'),
        ('donkey', 'Donkey'),
        ('ewe', 'Ewe'),
        ('ram', 'Ram'),
        ('weaner (sheep)', 'Weaner (Sheep)'),
        ('lamb', 'Lamb'),
        ('buck', 'Buck'),
        ('doe', 'Doe'),
        ('weaner (goat)', 'Weaner (Goat)'),
        ('kid', 'Kid'),
    ]
    animal = models.ForeignKey(Animals, on_delete=models.CASCADE, related_name="animal_types")
    animal_type_name = models.CharField(max_length=30, choices=ANIMAL_TYPE_CHOICES, unique=True)
    animal_type_description = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ['animal_type_name']  # alphabetical

    def __str__(self):
        return self.animal_type_name

class EventType(models.Model):
    EVENT_CHOICES = [
        ('mortality', 'Mortality'),
        ('farrowing', 'Farrowing'),
        ('calving', 'Calving'),
        ('lambing', 'Lambing'),
        ('kidding', 'Kidding'),
        ('procurement', 'Procurement'),
        ('culling', 'Culling'),
        ('sale', 'Sale'),
        ('treatment', 'Treatment'),
        ('vaccination', 'Vaccination'),
        ('gift', 'Gift'),
    ]

    # 🔹 Piggery Locations: Line + Block (A–Z)
    PIGGERY_LINES = [f"Line {i}" for i in range(1, 10)] + [ "Denmark",]
    PIGGERY_BLOCKS = [f"Block {chr(j)}" for j in range(65, 91)]  # A–Z
    PIGGERY_PENS = [f"Pen {i}" for i in range(1, 101)]  # 1–100

    PADDOCK_LOCATIONS = [(f"Paddock {i}", f"Paddock {i}") for i in range(1, 9)] + [
        ('Isolation', 'Isolation'), ('General Herd', 'General Herd')
    ]
    SMALL_RUMINANT_LOCATIONS = [(f"Pen {i}", f"Pen {i}") for i in range(1, 11)]

    LOCATION_CHOICES = {
        'cattle': PADDOCK_LOCATIONS,
        'sheep': SMALL_RUMINANT_LOCATIONS,
        'goat': SMALL_RUMINANT_LOCATIONS,
    }

    animal = models.ForeignKey('Animals', on_delete=models.CASCADE, related_name="events", null=True, blank=True)
    animal_type = models.ForeignKey('AnimalType', on_delete=models.CASCADE, related_name="events", null=True, blank=True)
    event_name = models.CharField(max_length=20, choices=EVENT_CHOICES)
    location = models.CharField(max_length=100, null=True, blank=True)
    number_of_animals = models.PositiveIntegerField(default=1)
    designation = models.TextField(max_length=500, null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    event_date = models.DateField(default=timezone.now)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.get_event_name_display()} - {self.event_date.strftime('%Y-%m-%d')}"

    def get_location_choices(self):
        """Return proper location list based on animal type"""
        if not self.animal_type or not self.animal_type.animal:
            return []
        key = self.animal_type.animal.animal_name.lower()
        return self.LOCATION_CHOICES.get(key, [])

class EventImage(models.Model):
    event = models.ForeignKey(EventType, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to='uploads/', validators=[validate_file_size], blank=True, null=True)  # Added validation
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for event: {self.event.event_name}"


class PendingEventEdit(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )

    event = models.ForeignKey(
        EventType,
        on_delete=models.CASCADE,
        related_name='pending_edits'
    )
    submitted_by = models.ForeignKey(User, on_delete=models.CASCADE)
    submitted_at = models.DateTimeField(auto_now_add=True)

    data = models.JSONField()

    # 🔹 NEW
    vet_note = models.TextField(blank=True)
    admin_note = models.TextField(blank=True)

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='pending'
    )

    reviewed_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reviewed_event_edits'
    )
    reviewed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Edit for {self.event} ({self.status})"



class Census(models.Model):
    animal = models.ForeignKey('Animals', on_delete=models.CASCADE, related_name='censuses')
    census_date = models.DateField(default=timezone.now)
    total_animals = models.PositiveIntegerField(default=0, editable=False)
    notes = models.TextField(null=True, blank=True)

    # Add this missing line right here:
    is_pending_review = models.BooleanField(default=False)

    def __str__(self):
        return f"Census for {self.animal} on {self.census_date}"

    def update_total(self):
        """Auto calculate total from sub-records"""
        self.total_animals = self.records.aggregate(total=models.Sum('number_of_animals'))['total'] or 0
        self.save()


class CensusRecord(models.Model):
    census = models.ForeignKey(Census, on_delete=models.CASCADE, related_name='records')
    animal_type = models.ForeignKey('AnimalType', on_delete=models.CASCADE)
    number_of_animals = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.animal_type} - {self.number_of_animals}"


@receiver([post_save, post_delete], sender=CensusRecord)
def update_census_total(sender, instance, **kwargs):
    instance.census.update_total()



class CensusApprovalQueue(models.Model):
    census = models.ForeignKey(Census, on_delete=models.CASCADE, related_name='pending_changes')
    requested_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Change 'help_with' to 'help_text' right here:
    form_data_payload = models.JSONField(help_text="Serialized form & formset data fields")

    # request_note = models.TextField(null=True, blank=True)
    request_note = models.TextField(null=True, blank=True, verbose_name="Vet's Request Note")
    admin_comment = models.TextField(null=True, blank=True, verbose_name="Admin's Feedback Note")
    
    is_processed = models.BooleanField(default=False)
    approved = models.BooleanField(null=True, blank=True)

    def __str__(self):
        return f"Pending edit for {self.census} by {self.requested_by}"

class ExoticAnimalCensus(models.Model):

    ANIMAL_CHOICES = [
        ('geese', 'Geese'),
        ('crocodile', 'Crocodile'),
    ]

    animal_name = models.CharField(max_length=20,choices=ANIMAL_CHOICES)

    census_date = models.DateField(default=timezone.now)

    total_animals = models.PositiveIntegerField()

    notes = models.TextField(null=True,blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-census_date']
        verbose_name = "Exotic Animal Census"
        verbose_name_plural = "Exotic Animal Census Records"

    def __str__(self):
        return f"{self.get_animal_name_display()} Census - {self.census_date}"


class PiggeryLine(models.Model):
    """Stores the definitions (e.g., Line 1 (Breeding), Line 2 (Nursing))"""
    name = models.CharField(max_length=50) # e.g., "Line 1"
    specification = models.CharField(max_length=100) # e.g., "Breeding"

    def __str__(self):
        return f"{self.name} ({self.specification})"

class PiggeryCensusRecord(models.Model):
    """The actual data recorded during a census"""
    census = models.ForeignKey(Census, on_delete=models.CASCADE, related_name='piggery_records')
    line = models.ForeignKey(PiggeryLine, on_delete=models.PROTECT)
    number = models.PositiveIntegerField(default=0)
    total_general = models.PositiveIntegerField(default=0)
    total_piglets = models.PositiveIntegerField(default=0)
    note = models.TextField(null=True, blank=True)

    def update_total(self):
        # Access the parent census object
        census = self.census
        records = census.piggery_records.all()
        
        # Calculate totals for the entire census
        total_gen = sum(r.number for r in records)
        total_pig = sum(r.total_piglets for r in records)
        
        # If you have fields on the Census model to store these:
        census.total_general = total_gen
        census.total_piglets = total_pig
        census.save()

    def __str__(self):
        return f"{self.line} - {self.number}"