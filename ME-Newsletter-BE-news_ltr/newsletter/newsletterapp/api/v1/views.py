from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes

from newsletter.newsletterapp.models import NewsLetter
from newsletter.newsletterapp.api.v1.serializers import ListSerializer, DetailSerializer
    


class NewsLetterListView(APIView):
    authentication_classes = ()
    permission_classes = ()

    @extend_schema(
        summary="List all newsletters",
        description="Returns a paginated list of all active newsletters ordered by creation date",
        responses={200: ListSerializer(many=True)},
        examples=[
            OpenApiExample(
                'Success Response',
                summary='Newsletter list',
                description='Example response showing newsletter data',
                value={
                    "result": [
                        {
                            "id": 1,
                            "title": "Weekly Tech Update",
                            "slug": "weekly-tech-update",
                            "description": "Latest technology news and updates",
                            "publish": "2023-02-15T10:00:00Z",
                            "created": "2023-02-15T10:00:00Z",
                            "modified": "2023-02-15T10:00:00Z"
                        }
                    ]
                }
            )
        ]
    )
    def get(self,request):
        queryset=NewsLetter.objects.active().all()
        serializer = ListSerializer(queryset, many=True)
        return Response({"result":serializer.data}, status=status.HTTP_200_OK)

class NewsLetterRecentListView(APIView):
    authentication_classes = ()
    permission_classes = ()

    def get(self,request):
        queryset=NewsLetter.objects.active().order_by("-created")[:4]
        serializer = ListSerializer(queryset, many=True)
        return Response({"result":serializer.data}, status=status.HTTP_200_OK)        

class NewstLetterDetailView(APIView):
    authentication_classes = ()
    permission_classes = ()

    def get(self, request, slug):
        if slug:
            queryset=NewsLetter.objects.active().filter(slug=slug)
            serilaizer = DetailSerializer(queryset, many=True)
            return Response({"result":serilaizer.data}, status=status.HTTP_200_OK)
        return Response({"result":"slug is not given"}, status=status.HTTP_400_BAD_REQUEST)
    
class PreviousNewsLetterView(APIView):
    authentication_classes = ()
    permission_classes = ()
    def get(self,request):
        queryset=NewsLetter.objects.active().order_by("-created")[1:]
        serializer = ListSerializer(queryset, many=True)
        return Response({"result":serializer.data}, status=status.HTTP_200_OK)        