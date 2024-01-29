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


class RegistrationAPIView(APIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = RegistrationSerializer

    def post(self, request):
        user = request.data.get('user', {})

        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

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

        return Response(serializer.data)


class UserEmailListAPIView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = []

    def list(self, request, *args, **kwargs):
        random_user = User.objects.order_by('?').first()
        if random_user:
            with_welcome = request.query_params.get("with_welcome")
            with_welcome = with_welcome in ["true", True, "1", 1, "True"]
            #send_email_new_user.delay(random_user.username, random_user.email, random_user.created_at.isoformat(), with_welcome)
            join_mail_new_welcome_user.delay(random_user.pk)
        return super().list(request, *args, **kwargs)

