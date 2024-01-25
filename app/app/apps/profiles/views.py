from rest_framework import serializers, status 
from rest_framework.exceptions import NotFound 
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Profile 
from .renderers import ProfileJSONRenderer
from .serializers import ProfileSerializer

class ProfileRetrieveAPIView(RetrieveAPIView):
    permission_classes = (AllowAny,)
    queryset = Profile.objects.select_related('user')
    renderer_classes = (ProfileJSONRenderer,)
    serializer_class = ProfileSerializer

    def retrieve(self, request, username, *args, **kwargs):
        try:
            profile = self.get_queryset().get(user__username=username)
        except Profile.DoesNotExist:
            raise NotFound('A profile with this username does not exist')
        
        serializer = self.get_serializer(profile)

        return Response(serializer.data)
    
class ProfileFollowAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (ProfileJSONRenderer,)
    serializer_class = ProfileSerializer

    def delete(self, request, username=None):
        follower = self.request.user.profile 

        try:
            followee = Profile.objects.get(user__username=username)
        except Profile.DoesNotExist:
            raise NotFound('A profile with this username was not found.')
        
        follower.unfollow(followee)

        return Response(status=status.HTTP_204_NO_CONTENT)


    def post(self, request, username=None):
        follower = self.request.user.profile 

        try:
            followee = Profile.objects.get(user__username=username)
        except Profile.DoesNotExist:
            raise NotFound('A profile with this username was not found.')
        
        if follower.pk == followee.pk:
            raise serializers.ValidationError('You can not follow yourself.')
        
        follower.follow(followee)

        serializer = self.serializer_class(followee, context={'request': request})

        return Response(serializer.data, status=status.HTTP_201_CREATED)
