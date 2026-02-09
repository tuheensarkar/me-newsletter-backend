from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from newsletter.updates.models import Update
from newsletter.newsletterapp.models import NewsLetter
from newsletter.newsletterapp.api.v1.serializers import ListSerializer, DetailSerializer
from newsletter.updates.api.v1.serializers import UpdateListSerializer


class UpdateAndAroundTheWorldListView(APIView):
    permission_classes = ()
    authentication_classes = ()

    def get(self, request):
        region = request.GET.get("region")
        page = request.GET.get("page")

        if region and page:
            try:
                page = int(page)
                current_page = page - 1
                news_letter = NewsLetter.objects.order_by("-publish")[current_page]
                if NewsLetter.objects.count() == 1:
                    previous_news_letter = None
                    previous_updates = []
                else:
                    previous_news_letter = NewsLetter.objects.order_by("-publish")[page]
                    previous_updates = Update.objects.active().filter(newsletter=previous_news_letter, region=region)
                    previous_updates_serilizer = UpdateListSerializer(previous_updates, many=True)
                    previous_updates = previous_updates_serilizer.data
                updates = Update.objects.active().filter(newsletter=news_letter, region=region)
                serializer = UpdateListSerializer(updates, many=True)
                return Response({"result":serializer.data, "previous_updates":previous_updates}, status=status.HTTP_200_OK)

            except Exception:
                return Response({"result":"Page doen't exist"}, status=status.HTTP_400_BAD_REQUEST)

        elif not region and not page:
            updates = Update.objects.active().order_by("-publish").filter(region="MiddleEast")
            arountheworld = Update.objects.active().order_by("-publish").filter(region="Around The World")
            updates_serializer = UpdateListSerializer(updates, many=True)
            atw_serilizer = UpdateListSerializer(arountheworld, many=True)
            return Response({"updates":updates_serializer.data, "around_the_world":atw_serilizer.data}, status=status.HTTP_200_OK)

        else:
            return Response({"result":"Either Page or Region Not Provided"}, status=status.HTTP_400_BAD_REQUEST )

class UpdateRecentView(APIView):
    permission_classes = ()
    authentication_classes = ()
    queryset = Update.objects.active()
    def get(self, request):
        queryset = self.queryset.all().order_by("-created")[:4]
        serializer = UpdateListSerializer(queryset, many=True)
        return Response({"result":serializer.data}, status=status.HTTP_200_OK)