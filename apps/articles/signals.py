import os
import binascii

from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify

from .models import Article, Tag


MAXIMUM_SLUG_LENGTH = 50


@receiver(pre_save, sender=Article)
def add_slug_before_article_save(sender, **kwargs):
    instance = kwargs.get('instance')
    # print('instance', instance)
    if instance is not None and instance.slug:
        return

    slug = slugify(instance.title)
    unique = binascii.hexlify(os.urandom(20)).decode()

    # print(len(slug))
    # print(len(unique))

    if len(slug) > MAXIMUM_SLUG_LENGTH:
        slug = slug[:MAXIMUM_SLUG_LENGTH]

    while len(slug + '-' + unique) > MAXIMUM_SLUG_LENGTH:
        parts = slug.split('-')

        if len(parts) is 1:
            # To append the unique string we must
            # arbitrarily remove `len(unique)` characters from the end of
            # `slug`. Subtract one to account for extra hyphen.
            slug = slug[:MAXIMUM_SLUG_LENGTH - len(unique) - 1]
        else:
            slug = '-'.join(parts[:-1])
    # print(slug)
    # print(unique)
    instance.slug = slug + '-' + unique


@receiver(pre_save, sender=Tag)
def add_slug_before_tag_save(sender, **kwargs):
    instance = kwargs.get('instance')
    if instance is not None and instance.slug:
        return

    slug = slugify(instance.tag)
    unique = binascii.hexlify(os.urandom(20)).decode()

    if len(slug) > MAXIMUM_SLUG_LENGTH:
        slug = slug[:MAXIMUM_SLUG_LENGTH]

    while len(slug + '-' + unique) > MAXIMUM_SLUG_LENGTH:
        parts = slug.split('-')

        if len(parts) is 1:
            slug = slug[:MAXIMUM_SLUG_LENGTH - len(unique) - 1]
        else:
            slug = '-'.join(parts[:-1])

    instance.slug = slug + '-' + unique
