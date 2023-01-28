from django.urls import path
from . import views

urlpatterns = [
    path('account/<int:pk>/', views.UserQueView.as_view({'get': 'retrieve', 'put': 'update'})),
    path('<int:pk>/', views.UserQuePublicView.as_view({'get': 'retrieve'})),
]
