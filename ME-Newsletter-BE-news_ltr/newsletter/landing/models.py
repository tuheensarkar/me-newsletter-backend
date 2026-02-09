from django.db import models
from newsletter.core.behaviors import EmailMixin
# Create your models here.
class SubscribeEmail(EmailMixin):
    """
    Subscribe email model
    """
    class Meta:
        verbose_name = "SUbscribe Email"