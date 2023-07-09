from django.urls import path
from matches.views import MatchesView

urlpatterns = [
    path('matches/', MatchesView.as_view(), name='matches-list'),
]
