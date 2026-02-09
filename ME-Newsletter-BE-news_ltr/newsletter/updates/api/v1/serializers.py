from rest_framework.serializers import ModelSerializer, SerializerMethodField

from newsletter.updates.models import Update
from newsletter.newsletterapp.models import NewsLetter


class UpdateListSerializer(ModelSerializer):
    class Meta:
        model = Update
        fields = ["id","title", "description","content", "image", "region", "author","country", "publish", "time_to_read"]

