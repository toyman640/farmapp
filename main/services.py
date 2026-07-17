from django.db.models import Sum
from farmrecord.models import EventType, Census, PiggeryCensusRecord
from django.utils import timezone

# Mapping events for each section
EVENT_MAP = {
    'pig': {'birth': ['farrowing']},
    'cattle': {'birth': ['calving']},
    'sheep': {'birth': ['lambing', 'kidding']},
}
def run_projection_calculation(animal_obj, start_date, end_date, start_count=0):

    # Ensure dates are not None
    if start_date is None or end_date is None:
        print(f"ERROR: Invalid dates provided: {start_date} to {end_date}")
        return None # Or handle accordingly
        
    section = animal_obj.animal_name.lower()
    birth_terms = EVENT_MAP.get(section, {}).get('birth', [])
    
    if start_count is None:
        start_count = 0
        
    if end_date is None:
        end_date = timezone.now()

    # BOUNDED DATE RANGE: Must be on/after start_date AND before/on end_date
    events = EventType.objects.filter(
        animal=animal_obj, 
        event_date__gte=start_date,
        event_date__lte=end_date
    )

    print(f"Calculating projection for {section} from {start_date} to {end_date}. Start count: {start_count}. Events found: {events.count()}")
    print(f"Events: {list(events.values('event_name', 'number_of_animals', 'event_date'))}")

    def get_sum(names):
        return events.filter(event_name__in=names).aggregate(
            total=Sum('number_of_animals'))['total'] or 0

    births = get_sum(birth_terms)
    mortality = get_sum(['mortality', 'Mortality'])
    culling = get_sum(['culling', 'Culling'])
    sale = get_sum(['sale', 'Sale'])
    gift = get_sum(['gift', 'Gift'])
    procurement = get_sum(['procurement', 'Procurement'])

    projected = (start_count + births + procurement) - (mortality + culling + sale + gift)

    return {
        "start_count": start_count,
        "projected_count": projected,
        "total_mortality": mortality,
        "total_culling": culling,
        "total_sale": sale,
        "total_gift": gift,
        "total_births": births,
        "total_procurement": procurement
    }