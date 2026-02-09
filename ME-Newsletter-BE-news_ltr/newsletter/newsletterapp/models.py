from django.db import models
from django.utils.translation import ugettext_lazy as _

from newsletter.core.behaviors import PostMixin


class NewsLetter(PostMixin):
    """
    News Letter Model
    """
    region = models.CharField(_("Region"), max_length=100 ,null=True, blank=True)
    country = models.CharField(_("Country"), max_length=100 ,null=True, blank=True)

    def __str__(self):
        return self.title
        
    class Mets:
        verbose_name = "News Letter"