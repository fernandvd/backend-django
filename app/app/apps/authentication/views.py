from django.core.cache import cache
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import status 
from rest_framework.generics import RetrieveUpdateAPIView, ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .renderers import UserJSONRenderer
from .serializers import (
    LoginSerializer, RegistrationSerializer, UserSerializer,
)
from .models import User
from .tasks import join_mail_new_welcome_user


KEY_PREFIX_CACHE_LIST_USER = "list-user"

def delete_cache_list_user():
    redis_client = cache._cache.get_client()
    all_keys = list(redis_client.scan_iter(match=f'*{KEY_PREFIX_CACHE_LIST_USER}*'))
    cache.delete_many([key.decode('utf-8')[3:] for key in all_keys])


class RegistrationAPIView(APIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = RegistrationSerializer

    def post(self, request):
        user = request.data.get('user', {})

        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        delete_cache_list_user()
        join_mail_new_welcome_user.delay(user.pk)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
class LoginAPIView(APIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = LoginSerializer

    def post(self, request):
        user = request.data.get('user', {})

        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        
        return Response(serializer.data,)
    

class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated, )
    renderer_classes = [UserJSONRenderer,]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user 
    
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        user_data = request.data.get('user', {})

        serializer = self.serializer_class(instance, data=user_data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        delete_cache_list_user()

        return Response(serializer.data)


class UserListAPIView(ListAPIView):
    queryset = User.objects.select_related('profile').all()
    serializer_class = UserSerializer

    @method_decorator(cache_page(10*60, key_prefix=KEY_PREFIX_CACHE_LIST_USER))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

