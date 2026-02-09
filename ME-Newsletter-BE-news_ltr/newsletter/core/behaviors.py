# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.core.validators import RegexValidator

from ckeditor_uploader.fields import RichTextUploadingField
from model_utils.models import TimeStampedModel

from newsletter.core.managers import StatusMixinManager
from newsletter.core.utils import upload_location, create_slug
from newsletter.core.validators import validator_ascii


class StatusMixin(models.Model):
    is_active = models.BooleanField(_("active"), default=True, blank=False, null=False)
    is_deleted = models.BooleanField(
        _("deleted"), default=False, blank=False, null=False
    )

    objects = StatusMixinManager()

    def activate(self):
        if not self.is_active:
            self.is_active = True
            self.save()

    def deactivate(self):
        if self.is_active:
            self.is_active = False
            self.save()

    def remove(self):
        if not self.is_deleted:
            self.is_deleted = True
            self.save()

    def has_changed(self, field):
        model = self.__class__.__name__
        return getattr(self, field) != getattr(
            self, "_" + model + "__original_" + field
        )

    def save(self, *args, **kwargs):
        """
        Makes sure that the ``is_active`` is ``False`` when ``is_deleted`` is ``True``.
        """
        if self.is_deleted:
            self.is_active = False
        super(StatusMixin, self).save(*args, **kwargs)

    class Meta:
        abstract = True


class SlugMixin(models.Model):
    slug = models.SlugField(blank=True, null=True, max_length=255)

    def save(self, *args, **kwargs):
        """
        slug  shouldn't have spaces
        """
        if not self.slug:
            self.slug = create_slug(self)
        if self.slug:
            self.slug = self.slug.replace(" ", "")
        super(SlugMixin, self).save(*args, **kwargs)

    class Meta:
        abstract = True


class ImageMixin(models.Model):
    image = models.ImageField(
        _("image"), upload_to=upload_location, null=True, blank=True
    )
    image_alt = models.CharField(
        _("image alt"), max_length=100, null=True, blank=True, validators=[validator_ascii]
    )

    class Meta:
        abstract = True


class MetaTagMixin(models.Model):
    meta_title = models.TextField(
        _("Meta Title"), blank=True, null=True, validators=[validator_ascii]
    )
    meta_description = models.TextField(
        _("Meta Description"), blank=True, null=True, validators=[validator_ascii]
    )
    meta_keywords = models.TextField(
        _("Meta Keywords"), blank=True, null=True, validators=[validator_ascii]
    )

    class Meta:
        abstract = True


# COMPOUND MIXINS
#   ---------------------------------------------------------------------------------------------------------------


class PostMixin(SlugMixin, ImageMixin, MetaTagMixin, StatusMixin, TimeStampedModel):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, models.SET_NULL, blank=True, null=True
    )
    title = models.CharField(
        _("title"), default='',
        max_length=255,
        null=False,
        blank=False,
    )
    description = models.TextField(
            _("short description"), max_length=500, null=True, blank=True, validators=[validator_ascii]
    )
    content = RichTextUploadingField(_("content"), blank=True, null=True)
    publish = models.DateTimeField(
        _("publish datetime"), auto_now=False, auto_now_add=False, default=timezone.now
    )
    time_to_read = models.IntegerField(default=5)

    def __str__(self):
        return self.title

    class Meta:
        abstract = True
        ordering = ["-created", "-modified"]


class EmailMixin(models.Model):
    email = models.EmailField(max_length=70,blank=True,unique=True)

    def __str__(self):
        return self.email

    class Meta:
        abstract = True
