from django.urls import path

from users.views import user, auth, confirm, interest

urlpatterns = [
    path('users/reg/', auth.RegistrationView.as_view(), name='registration'),
    path('users/telegram/reg/', auth.TelegramRegistrationView.as_view(), name='telegram-registration'),
    path('users/change-password/', confirm.ChangePasswordView.as_view(), name='change_password'),
    path('users/telegram-auth/', auth.TelegramTokenCreateView.as_view(), name='custom_token_create'),
    path('users/me/', user.UserAPIView.as_view(), name='user_me'),
    path('users/interests/', interest.InterestAPIView.as_view(), name='user_profile'),
    path('interests/', interest.InterestView.as_view(), name='interests'),
]
