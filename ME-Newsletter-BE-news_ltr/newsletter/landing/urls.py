from django.urls import path

from newsletter.landing.api.v1 import views

urlpatterns = [
    path("subscribe/", views.SubscribeEmailView.as_view(), name = "subscribe email")
]