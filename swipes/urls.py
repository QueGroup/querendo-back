from django.urls import path

from swipes import views

urlpatterns = [
    path('swipes/', views.QuestionnairesListView.as_view(), name='swipes'),
]
