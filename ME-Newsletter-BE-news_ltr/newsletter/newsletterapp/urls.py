from django.urls import path
from newsletter.newsletterapp.api.v1.views import NewsLetterListView, NewstLetterDetailView, NewsLetterRecentListView, PreviousNewsLetterView

urlpatterns =[
    path("news-letter-list/", NewsLetterListView.as_view(), name="list"),
    path("news-letter-recent-list/", NewsLetterRecentListView.as_view(), name="list"),
    path("news-letter-detail/<str:slug>/", NewstLetterDetailView.as_view(), name = "Detail"),
    path("prev-news-letter-list/", PreviousNewsLetterView.as_view(), name="Previous list"),
]