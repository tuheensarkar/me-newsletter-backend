from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from newsletter.practicals.models import Practical
from newsletter.practicals.api.v1.serializers import PracticalListSerializer, PracticalDetailSerializer

class PracticalListView(APIView, PageNumberPagination):
    permission_classes = ()
    authentication_classes = ()
    queryset = Practical.objects.active()
    page_size = 10

    def get(self, request):
        articals = self.queryset.all()
        results = self.paginate_queryset(articals, request, view=self)
        serializer = PracticalListSerializer(results, many=True)
        return self.get_paginated_response(serializer.data)
        
class PracticalRecentView(APIView):
    permission_classes = ()
    authentication_classes = ()
    queryset = Practical.objects.active()

    def get(self, request):
        queryset = self.queryset.order_by("-created")[:2]
        serializer = PracticalListSerializer(queryset, many=True)
        return Response({"result":serializer.data}, status=status.HTTP_200_OK)
        

class PracticalDetailView(APIView):
    permission_classes = ()
    authentication_classes = ()
    queryset = Practical.objects.all()

    def get(self, request, slug):
        queryset = self.queryset.filter(slug=slug)
        serializer = PracticalDetailSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    