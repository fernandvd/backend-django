from django.urls import re_path

from .views import (
    LoginAPIView, RegistrationAPIView, UserRetrieveUpdateAPIView,
)

app_name = 'authentication'

urlpatterns = [
    re_path(r'^user/?$', UserRetrieveUpdateAPIView.as_view(), name='user-retrieve-update'),
    re_path(r'^users/?$', RegistrationAPIView.as_view(), name='register-user'),
    re_path(r'^users/login/?$', LoginAPIView.as_view(), name='auth-login'),
]