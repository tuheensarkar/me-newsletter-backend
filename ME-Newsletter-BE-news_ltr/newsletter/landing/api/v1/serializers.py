from rest_framework.serializers import ModelSerializer
from newsletter.landing.models import SubscribeEmail

class SubscribeEmailSerializer(ModelSerializer):
    class Meta:
        model = SubscribeEmail
        fields = ["email"]