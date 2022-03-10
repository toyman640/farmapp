from pyexpat import model
from django.utils.text import slugify


def unique_slug_generator(model_instance, location, slug_field):
    slug = slugify(location)
    model_class = model_instance.__class__
    while model_class._default_manager.filter(slug=slug).exists():
        object_pk = model_class._default_manager.latest('pk')
        object_pk = object_pk.pk + 1

        slug = f'{slug}-{object_pk}'
    return slug


def unique_slug_generatorM(model_instance, subject, slug_field):
    slug = slugify(subject)
    model_class = model_instance.__class__
    while model_class._default_manager.filter(slug=slug).exists():
        object_pk = model_class._default_manager.latest('pk')
        object_pk = object_pk.pk + 1

        slug = f'{slug}-{object_pk}'
    return slug