from django import template

register = template.Library()

@register.filter
def get_attr(obj, attr_name):
    return getattr(obj, attr_name, '')


@register.filter
def get_fk_name(value, field_name):
    if not value:
        return ''

    # If it's already an object (current_value)
    if hasattr(value, 'name'):
        return value.name

    # If it's an ID (new_value), you need to fetch from DB
    from farmrecord.models import Animals, AnimalType  # adjust import

    try:
        if field_name == 'animal':
            return Animal.objects.get(pk=value).name
        elif field_name == 'animal_type':
            return AnimalType.objects.get(pk=value).name
    except:
        return str(value)

    return str(value)