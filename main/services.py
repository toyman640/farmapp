from django.db.models import Sum
from farmrecord.models import EventType, Census, PiggeryCensusRecord

# Mapping events for each section
EVENT_MAP = {
    'pig': {'birth': ['farrowing']},
    'cattle': {'birth': ['calving']},
    'sheep': {'birth': ['lambing', 'kidding']},
}


def run_projection_calculation(animal_obj, start_date, start_count=None):
    section = animal_obj.animal_name.lower()
    birth_terms = EVENT_MAP.get(section, {}).get('birth', [])

    
    print(f"Searching for birth terms: {birth_terms}")

    # If start_count wasn't passed, fall back to standard logic
    if start_count is None:
        start_count = 0 # Or your default logic

    # Aggregate events
    events = EventType.objects.filter(animal=animal_obj, created_at__gt=start_date)

    def get_sum(names):
        return events.filter(event_name__in=names).aggregate(
            total=Sum('number_of_animals'))['total'] or 0

    births = get_sum(birth_terms)
    mortality = get_sum(['mortality'])
    culling = get_sum(['culling'])
    sale = get_sum(['sale'])
    gift = get_sum(['gift'])
    procurement = get_sum(['procurement'])

    # Calculation now uses the passed start_count (which is already accurate for Piggery)
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