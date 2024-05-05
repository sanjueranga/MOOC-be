from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import AccessToken
from .models import UserProfile, Country, UserType


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
        return data

    def create(self, validated_data):
        request = self.context.get("request")
        validated_data["user"] = request.user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        user = instance.user
        user.username = validated_data.get("username", user.username)
        user.first_name = validated_data.get("first_name", user.first_name)
        user.last_name = validated_data.get("last_name", user.last_name)
        user.save()
        return super().update(instance, validated_data)
       
