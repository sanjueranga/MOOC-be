from rest_framework import generics, permissions, status
from rest_framework.response import Response
from userprofiles.serializers import UserSerializer

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