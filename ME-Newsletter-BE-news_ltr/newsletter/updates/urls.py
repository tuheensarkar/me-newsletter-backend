from django.urls import path

from newsletter.updates.api.v1 import views

urlpatterns = [
    path('update-list/', views.UpdateAndAroundTheWorldListView.as_view(), name="Update-List-View"),
    path('update-recent-list/', views.UpdateRecentView.as_view(), name="Update Recent List View"),
]