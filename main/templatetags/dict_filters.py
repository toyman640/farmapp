# Example of what your custom filter must look like
from django import template
register = template.Library()

@register.filter
def get(dictionary, key):
  return dictionary.get(key)