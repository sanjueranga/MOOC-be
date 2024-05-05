from rest_framework import generics, permissions, status, viewsets
from rest_framework.response import Response
from userprofiles.serializers import UserSerializer, UserProfileSerializer
from userprofiles.models import UserProfile
from django.contrib.auth.models import User


class UserRegistrationAPIView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        resp = super().create(request, *args, **kwargs)
        respObj = {
            "status": "success",
            "data": resp.data,
        }

        return Response(respObj, status=status.HTTP_201_CREATED, headers=resp.headers)


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

    def get_object(self, request):
        username = request.query_params.get("username")
        if username is None:
            return self.request.user
        return User.objects.get(username=username)

    def create(self, request):
        request.data["action"] = self.action
        response = super().create(request)
        respObj = {
            "status": "success",
            "message": "User data added successfully",
            "data": "null",
        }
        return Response(
            respObj, status=status.HTTP_201_CREATED, headers=response.headers
        )
