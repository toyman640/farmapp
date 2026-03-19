from django import template
from farmrecord.models import Animals, AnimalType

register = template.Library()

@register.filter
def get_attr(obj, attr_name):
    """Return attribute of object safely"""
    return getattr(obj, attr_name, '')

@register.filter
def get_fk_name(value, field_name):
    """Convert foreign key ID to readable name"""
    if not value:
        return ""
    if field_name == "animal":
        try:
            return Animals.objects.get(pk=value).animal_name
        except Animals.DoesNotExist:
            return value
    if field_name == "animal_type":
        try:
            return AnimalType.objects.get(pk=value).animal_type_name
        except AnimalType.DoesNotExist:
            return value
    return value
