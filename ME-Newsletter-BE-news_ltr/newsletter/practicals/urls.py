from django.urls import path

from newsletter.practicals.api.v1 import views

urlpatterns = [
    path('practical-list/', views.PracticalListView.as_view(), name="Practical List View"),
    path('practical-recent-list/', views.PracticalRecentView.as_view(), name="Practical Recent View"),
    path('practical-detail/<str:slug>/', views.PracticalDetailView.as_view(), name="Practical Detail View")
]