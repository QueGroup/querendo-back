from django.urls import path

from users.views import users

urlpatterns = [
    path('users/reg/', users.RegistrationView.as_view(), name='registration'),
    path('users/change-password/', users.ChangePasswordView.as_view(), name='change_password'),
    path('users/me/', users.MyView.as_view(), name='user_profile'),
]
