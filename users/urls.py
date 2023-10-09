from django.urls import path

from users.views import users, auth, interest, photos

urlpatterns = [
    path('users/reg/', auth.RegistrationView.as_view(), name='registration'),
    path('users/telegram/reg/', auth.TelegramRegistrationView.as_view(), name='telegram-registration'),
    path('users/telegram-auth/', auth.TelegramTokenCreateView.as_view(), name='custom_token_create'),
    path('users/change-password/', auth.ChangePasswordView.as_view(), name='change_password'),
    path('users/me/', users.UserProfileView.as_view(), name='user_profile'),
    path('users/interests/', interest.InterestAPIView.as_view(), name='user_profile'),
    path('interests/', interest.InterestView.as_view(), name='interests'),
    path('brandbook/', photos.BrandBookView.as_view(), name='brandbook')
]
