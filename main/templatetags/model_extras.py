from django import template
from farmrecord.models import Animals, AnimalType

register = template.Library()

@register.filter
def get_attr(obj, attr_name):
    """Return attribute of object safely"""
    return getattr(obj, attr_name, '')

@register.filter
def resolve_fk(value, field_name):
    if not value:
        return ""

    try:
        if field_name == "animal":
            return Animals.objects.get(pk=value).animal_name

        if field_name == "animal_type":
            return AnimalType.objects.get(pk=value).animal_type_name

    except (Animals.DoesNotExist, AnimalType.DoesNotExist):
        return value

    return value

