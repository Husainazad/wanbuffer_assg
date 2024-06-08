from django.conf import settings
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .helpers import get_tokens_for_user
from .serializers import *
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from django.http import HttpResponse



# Create your views here.

class UserSignupView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data': serializer.data, 'msg': "User created successfully"},
                            status=status.HTTP_201_CREATED)
        return Response({
            "error": serializer.errors,
            "msg": "Something went wrong"
        }, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data.get('email')
        password = serializer.data.get('password')
        is_user = authenticate(email=email, password=password)
        if is_user is not None:
            token = get_tokens_for_user(is_user)
            return Response({
                "email": is_user.email,
                "user_id": is_user.id,
                "access_token": token,
                "msg": "user login successfully"
            }, status=status.HTTP_200_OK)
        return Response({
            "msg": "Unfortunately the credentials you are entering is not matching our records."
                   "Please try again later or try resetting the credentials"
        }, status=status.HTTP_400_BAD_REQUEST)


class UpdateUserDetailsView(APIView):
    permission_classes = [IsAuthenticated]
    def patch(self, request):
        user_email = request.user
        try:
            user = CustomUser.objects.get(email=user_email)
        except CustomUser.DoesNotExist:
            return Response({"msg": "User not found"},status=status.HTTP_404_NOT_FOUND)

        serializer = UserUpdateSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"data": serializer.data, "msg": "user details updated successfully!"}, status=status.HTTP_200_OK)

        return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class AdminPanelView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        data = CustomUser.objects.all()
        return render(request, 'wanbuffer_app/adminpanel.html', {"datas": data})



class PasswordResetRequestView(APIView):

    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            # user = get_object_or_404(CustomUser, email=email)
            user = CustomUser.objects.filter(email=email).first()
            if user is None:
                return Response({"msg": "No user found!"}, status=status.HTTP_404_NOT_FOUND)

            reset_token = PasswordResetToken.objects.create(user=user)
            FRONTEND_URL = 'http://localhost:8000'
            reset_link = f"{FRONTEND_URL}/api/reset-password/{reset_token.token}"

            # Send email
            subject = 'Password Reset Request'
            message = f'Click the link to reset your password: {reset_link}'
            # email_from = settings.EMAIL_HOST
            email_from = settings.EMAIL_HOST_USER
            send_mail(subject, message, email_from, [user.email])

            return Response({"detail": "Password reset link sent."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordView(APIView):
    def post(self, request, request_uuid):
        try:
            request_instance = PasswordResetToken.objects.get(token=request_uuid)

        except PasswordResetToken.DoesNotExist:
            return Response({"msg": "Reset Link is expired!"},
                            status=status.HTTP_404_NOT_FOUND)

        except ValidationError as e:
            return Response({"msg": "Invalid Reset Link!"}, status=status.HTTP_400_BAD_REQUEST)

        data = request.data
        user = CustomUser.objects.get(email=request_instance.user)
        if data['new_password'] == data['new_password_confirm']:
            user.set_password(data['new_password'])
            user.save()
            return Response({
                "msg": "Password Changed Successfully!"
            }, status=status.HTTP_200_OK)

        return Response({
            "msg": "Password didn't match, please try again!"
        }, status=status.HTTP_400_BAD_REQUEST)