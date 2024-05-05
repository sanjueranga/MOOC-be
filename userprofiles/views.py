from rest_framework import generics, permissions, status, viewsets
from rest_framework.response import Response
from userprofiles.serializers import UserSerializer, UserProfileSerializer,WorkExperienceSerializer,EducationSerializer,UserLoginSerializer
from userprofiles.models import UserProfile,WorkExperience,Education
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import AccessToken


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
class UserLoginApiView(generics.GenericAPIView):
    serializer_class = UserLoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_name = serializer.validated_data["username"]
        password = serializer.validated_data["password"]
        user = authenticate(username=user_name, password=password)
        if user:
            respObj = {
                "status": "success",
                "data": {
                    "access_token": str(AccessToken.for_user(user)),
                    "user": {
                        "user_id": user.id,
                        "username": user.username,
                        "full_name": f"{user.first_name} {user.last_name}",
                        "email": user.email,
                    },
                },
            }
            return Response(respObj, status=status.HTTP_200_OK)
        else:
            respObj = {
                "status": "fail",
                "message": ["Invalid email or password"],
            }

        return Response(respObj, status=status.HTTP_403_FORBIDDEN)

class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

    def get_object(self):
        return self.request.user.userprofile

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

    def update(self, request, *args, **kwargs):
        request.data["user_type"] = request.user.userprofile.user_type.label
        request.data["action"] = self.action
        
        response = super().update(request, *args, **kwargs)
        respObj = {
            "status": "success",
            "message": "User data updated successfully",
            "data": "null",
        }
        return Response(
            respObj, status=status.HTTP_200_OK, headers=response.headers
        )
    
class WorkExperienceViewset(viewsets.ModelViewSet):
    queryset = WorkExperience.objects.all()
    serializer_class = WorkExperienceSerializer

    def get_queryset(self):
        return super().get_queryset().filter(user_profile=self.request.user.userprofile.id)

    def create(self, request):

        request.data["user_profile"]= request.user.userprofile.id
        response = super().create(request)
        respObj = {
            "status": "success",
            "message": "WorkExperience data added successfully",
            "data": "null",
        }
        return Response(
            respObj, status=status.HTTP_201_CREATED, headers=response.headers
        )

    def update(self, request, *args, **kwargs):

        response = super().update(request, *args, partial=True, **kwargs)
        respObj = {
            "status": "success",
            "message": "WorkExperience updated successfully",
            "data": "null",
        }
        return Response(
            respObj, status=status.HTTP_200_OK, headers=response.headers
        )
    
    def destroy(self, request, *args, **kwargs):
        response = super().destroy(request, *args, **kwargs)
        respObj = {
            "status": "success",
            "message": "WorkExperience deleted successfully",
            "data": "null",
        }
        return Response(
            respObj, status=status.HTTP_204_NO_CONTENT, headers=response.headers
        )
    

class EducationViewset(viewsets.ModelViewSet):
    queryset = Education.objects.all()
    serializer_class = EducationSerializer

    def get_queryset(self):
        return super().get_queryset().filter(user_profile=self.request.user.userprofile.id)

    def create(self, request):

        request.data["user_profile"]= request.user.userprofile.id
        response = super().create(request)
        respObj = {
            "status": "success",
            "message": "Education data added successfully",
            "data": "null",
        }
        return Response(
            respObj, status=status.HTTP_201_CREATED, headers=response.headers
        )

    def update(self, request, *args, **kwargs):

        response = super().update(request, *args, partial=True, **kwargs)
        respObj = {
            "status": "success",
            "message": "Education updated successfully",
            "data": "null",
        }
        return Response(
            respObj, status=status.HTTP_200_OK, headers=response.headers
        )
    
    def destroy(self, request, *args, **kwargs):
        response = super().destroy(request, *args, **kwargs)
        respObj = {
            "status": "success",
            "message": "Education deleted successfully",
            "data": "null",
        }
        return Response(
            respObj, status=status.HTTP_204_NO_CONTENT, headers=response.headers
        )