from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import AccessToken



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
