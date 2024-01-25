from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify

from app.apps.core.utils import generate_random_string

from .models import Article

@receiver(pre_save, sender=Article)
def add_slug_to_article_if_not_exists(sender, instance, *args, **kwargs):
    MAXIMUN_SLUG_LENGTH = 255

    if instance and not instance.slug:
        slug = slugify(instance.title)
        unique = generate_random_string()

        if len(slug) > MAXIMUN_SLUG_LENGTH: 
            slug = slug[:MAXIMUN_SLUG_LENGTH]

        while len(slug + '-'+unique) > MAXIMUN_SLUG_LENGTH: 
            parts = slug.split('-')
            if len(parts) == 1:
                slug = slug[:MAXIMUN_SLUG_LENGTH - len(unique) -1]
            else:
                slug = '-'.join(parts[:-1])
        
        instance.slug = slug + '-' + unique
