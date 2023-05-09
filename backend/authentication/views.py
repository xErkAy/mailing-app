# -*- coding: utf-8 -*-
from django.contrib.auth import login

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.views import JSONWebTokenAPIView

from authentication.exceptions import AuthenticationFailed, InvalidUsernameOrPassword
from project.models import User
from authentication.serializers import UserSerializer
from authentication.authentication import jwt_payload_handler, jwt_encode_handler


class AuthenticationAPIView(JSONWebTokenAPIView):
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user = User.objects.get(username=serializer.validated_data.get('username'))
        except User.DoesNotExist:
            raise InvalidUsernameOrPassword()

        if not user.check_password(serializer.validated_data.get('password')):
            raise InvalidUsernameOrPassword()

        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)

        try:
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        except Exception:
            raise AuthenticationFailed()

        payload['token'] = token

        return Response(payload, status=status.HTTP_200_OK)


class RegistrationAPIView(APIView):
    authentication_classes = ()
    serializer_class = UserSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({}, status=status.HTTP_200_OK)
