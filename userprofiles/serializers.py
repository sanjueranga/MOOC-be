from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import AccessToken
from .models import UserProfile, Country



class UserSerializer(serializers.ModelSerializer):
    firstname = serializers.CharField(source="first_name", required=True)
    lastname = serializers.CharField(source="last_name", required=True)

    class Meta:
        model = User
        fields = ["firstname", "lastname", "email", "password","username"]
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

    class Meta:
        model = UserProfile
        exclude = ["user"]

    def validate(self, data):
        request = self.context.get("request")
        country_name = data.get("country")
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
        return data

    def create(self, validated_data):
        request = self.context.get("request")
        validated_data["user"] = request.user
        return super().create(validated_data)