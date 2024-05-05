from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import AccessToken
from .models import (
    UserProfile,
    Country,
    UserType,
    Interest,
    WorkExperience,
    Education,
    Institution,
)


class UserSerializer(serializers.ModelSerializer):
    firstname = serializers.CharField(source="first_name", required=True)
    lastname = serializers.CharField(source="last_name", required=True)

    class Meta:
        model = User
        fields = ["firstname", "lastname", "email", "password", "username"]
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, attrs):
        # raise an error if the email already exists
        email = attrs.get("email")
        username = attrs.get("username")
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({"email": "Email already exists"})
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError({"username": "Username already exists"})

        return attrs

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = super().create(validated_data)
        user.set_password(password)
        user.save()
        return user

    def to_representation(self, instance):
        return {
            "user_id": instance.id,
            "access_token": str(AccessToken.for_user(instance)),
        }



class UserProfileSerializer(serializers.ModelSerializer):
    country = serializers.CharField(max_length=100)
    user_type = serializers.CharField(max_length=100)
    action = serializers.CharField(max_length=100, required=False)
    firstname = serializers.CharField(source="first_name", required=False)
    lastname = serializers.CharField(source="last_name", required=False)
    username = serializers.CharField(required=False)
    interests = serializers.ListField(child=serializers.CharField(), required=False)

    class Meta:
        model = UserProfile
        exclude = ["user"]

    def validate(self, data):
        request = self.context.get("request")
        country_name = data.get("country")
        user_type = data.get("user_type")
        action = data.pop("action")
        user = request.user
        if action == "create":
            if UserProfile.objects.filter(user=user).exists():
                raise serializers.ValidationError(
                    {"user": "User profile already exists"}
                )
        try:
            country_instance = Country.objects.get(label=country_name)
            data["country"] = country_instance
        except Country.DoesNotExist:
            raise serializers.ValidationError(
                {"Country": "Invalid country name provided"}
            )
        try:
            user_type_instance = UserType.objects.get(label=user_type)
            data["user_type"] = user_type_instance
        except UserType.DoesNotExist:
            raise serializers.ValidationError(
                {"User Type": "Invalid user type provided"}
            )

        interests = data.pop("interests", [])
        data["interests"] = []
        self.fields.pop("interests")
        for interest in interests:
            try:
                interest_instance = Interest.objects.get(label=interest)
                data["interests"].append(interest_instance)
            except Interest.DoesNotExist:
                pass
        return data

    def create(self, validated_data):
        request = self.context.get("request")
        validated_data["user"] = request.user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        user = instance.user
        try:
            user.username = validated_data.get("username", user.username)
            user.first_name = validated_data.get("first_name", user.first_name)
            user.last_name = validated_data.get("last_name", user.last_name)
            user.save()
        except Exception as e:
            raise serializers.ValidationError({"username": "Username already exists"})
        return super().update(instance, validated_data)
    
    def to_representation(self, instance):
        work = WorkExperience.objects.filter(user_profile=instance)
        education = Education.objects.filter(user_profile=instance)

        work_data = WorkExperienceSerializer(work, many=True).data
        education_data = EducationSerializer(education, many=True).data

        representation = {
            "user_id": instance.user.id,
            "username": instance.user.username,
            "first_name": instance.user.first_name,
            "last_name": instance.user.last_name,
            "email": instance.user.email,
            "country": instance.country.label,
            "description": instance.description,
            "profile_picture": instance.profile_picture if instance.profile_picture else "",
            "interests": [interest.label for interest in instance.interests.all()],
            "work_experience": work_data,
            "education": education_data,
        }
        return representation


class WorkExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkExperience
        fields = "__all__"
        


class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = "__all__"


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, attrs):
        email = attrs["email"]
        try:
            user = User.objects.get(email=email)
            attrs["username"] = user.username
        except User.DoesNotExist:
            attrs["username"] = None
        return attrs
