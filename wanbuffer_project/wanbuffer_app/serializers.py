from .models import *
from rest_framework import serializers


class UserRegistrationSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ['id', 'user_name', 'email', 'password']
        # fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True}
        }
    # creating the user object with in the serializer
    def create(self, validated_data):
        user = CustomUser.objects.create_user(email=validated_data["email"],
                                              user_name=validated_data["user_name"],
                                              password=validated_data["password"])

        return user


class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)

    class Meta:
        model = CustomUser
        fields = ["email", "password"]


class UserUpdateSerializer(serializers.ModelSerializer):
    # email = serializers.EmailField(max_length=255)
    # user_name = serializers.CharField(max_length=255)
    class Meta:
        model = CustomUser
        # fields = "__all__"
        fields = ['email', 'user_name']


class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()
