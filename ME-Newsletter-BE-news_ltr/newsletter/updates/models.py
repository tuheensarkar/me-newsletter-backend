from django.db import models
from django.utils.translation import ugettext_lazy as _

from newsletter.newsletterapp.models import NewsLetter
from newsletter.core.behaviors import PostMixin


class Update(PostMixin):
    CHOICES = (
        ("MiddleEast", "MiddleEast"),
        ("Around The World", "Around The World")
    )
    newsletter = models.ForeignKey(NewsLetter, on_delete=models.CASCADE ,blank=True, null=True)
    region = models.CharField(_("Region"), choices=CHOICES, max_length=100 ,null=True, blank=True)
    country = models.CharField(_("Country"), max_length=100 ,null=True, blank=True)
    
    def __str__(self):
        return self.title
            
    class Meta:
        verbose_name = "Update"

