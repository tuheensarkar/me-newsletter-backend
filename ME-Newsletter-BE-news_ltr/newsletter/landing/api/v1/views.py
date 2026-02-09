from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample

from newsletter.landing.models import SubscribeEmail
from newsletter.landing.api.v1.serializers import SubscribeEmailSerializer

class SubscribeEmailView(APIView):
    permission_classes = ()
    authentication_classes = ()

    @extend_schema(
        summary="Subscribe to newsletter",
        description="Add email address to newsletter subscription list",
        request=SubscribeEmailSerializer,
        responses={
            201: OpenApiTypes.STR,
            400: OpenApiTypes.OBJECT,
            500: OpenApiTypes.OBJECT
        },
        examples=[
            OpenApiExample(
                'Success Response',
                summary='Subscription successful',
                description='Email successfully subscribed',
                value="Email subscribed successfully",
                status_codes=['201']
            ),
            OpenApiExample(
                'Error Response',
                summary='Invalid email',
                description='Email validation failed',
                value={"email": ["Enter a valid email address."]},
                status_codes=['400']
            )
        ]
    )
    def post(self, request):
        serilizer = SubscribeEmailSerializer(data=request.data)
        if serilizer.is_valid(raise_exception=True):
            serilizer.save()
            return Response("Email subscribed successfully", status=status.HTTP_201_CREATED)
        return Response(serilizer.errors, status=status.HTTP_400_BAD_REQUEST)

