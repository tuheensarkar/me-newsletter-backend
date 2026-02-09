from rest_framework.serializers import ModelSerializer, Serializer

from newsletter.practicals.models import Practical

class PracticalListSerializer(ModelSerializer):
    class Meta:
        model = Practical
        fields = ["slug","title", "description", "image", "region", "author", "publish", "time_to_read"]

class PracticalDetailSerializer(ModelSerializer):
    class Meta:
        model = Practical
        fields = "__all__"