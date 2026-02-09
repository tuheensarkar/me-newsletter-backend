from rest_framework.serializers import ModelSerializer, SerializerMethodField

from newsletter.newsletterapp.models import NewsLetter
from newsletter.updates.models import Update
from newsletter.practicals.models import Practical
from newsletter.practicals.api.v1.serializers import PracticalListSerializer
from newsletter.updates.api.v1.serializers import UpdateListSerializer

class ListSerializer(ModelSerializer):
    updates = SerializerMethodField()
    practicals = SerializerMethodField()
    around_the_world = SerializerMethodField()

    class Meta:
        model = NewsLetter
        fields = ["title", "slug", "image", "description", "publish", "time_to_read", 'updates', 'practicals', "around_the_world"]

    def get_updates(self, obj):
        updates = Update.objects.filter(newsletter=obj, region="MiddleEast")
        return UpdateListSerializer(updates, many=True).data
    
    def get_practicals(self, obj):
        practicals = Practical.objects.filter(newsletter=obj)
        return PracticalListSerializer(practicals, many=True).data
    
    def get_around_the_world(self,obj):
        around_the_world = Update.objects.filter(newsletter=obj, region="Around The World")
        return UpdateListSerializer(around_the_world, many=True).data
    

class DetailSerializer(ModelSerializer):
    updates = SerializerMethodField()
    practicals = SerializerMethodField()
    around_the_world = SerializerMethodField()

    class Meta:
        model = NewsLetter
        fields = ["title", "slug", "image", "description", "publish", "time_to_read", 'updates', 'practicals', 'around_the_world']

    def get_updates(self, obj):
        updates = Update.objects.filter(newsletter=obj, region="MiddleEast")
        return UpdateListSerializer(updates, many=True).data
    
    def get_practicals(self, obj):
        practicals = Practical.objects.filter(newsletter=obj)
        return PracticalListSerializer(practicals, many=True).data

    def get_around_the_world(self,obj):
        around_the_world = Update.objects.filter(newsletter=obj, region="Around The World")
        return UpdateListSerializer(around_the_world, many=True).data