from __future__ import unicode_literals, absolute_import

# python imports
from random import choice
from string import digits, ascii_lowercase

# django imports
from django.utils.text import slugify


def upload_location(instance, filename):
    model = str(instance.__class__.__name__).lower()
    if model == "document":
        return "%s/%s/%s" % (instance.matter.irn_no, instance.stage.stage_name.name, filename)
    return "%s/%s" % (model, filename)


def generate_random_string(length=5):
    digit_len = length // 2
    alpha_len = length - digit_len
    return "".join(
        [choice(digits) for _ in range(digit_len)]
        + [choice(ascii_lowercase) for _ in range(alpha_len)]
    )


def create_slug(instance, new_slug=None, append_string=None):
    if new_slug is not None:
        slug = new_slug
    elif instance.slug:
        slug = instance.slug
    elif hasattr(instance, "title"):
        slug = slugify(instance.title)
    elif hasattr(instance, "name"):
        slug = slugify(instance.name)
    else:
        slug = None
    if append_string and slug:
        slug = slugify(append_string + slug)
    if slug:
        qs = instance.__class__.objects.filter(slug=slug).order_by("-id")
        exists = True if qs.exists() and qs.first().id != instance.id else False
        if exists:
            # print qs
            # print "old_slug",slug
            new_slug = "%s-%s" % (slug, generate_random_string(length=5))
            # print "new_slug",new_slug
            return create_slug(instance, new_slug=new_slug)
        if len(slug) > 50:
            slug = slug[:44] + "-" + generate_random_string(length=5)
        if not slug:
            slug = generate_random_string(length=5)
        return slug
    else:
        return None