import datetime

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.models import Group
from .serializers import (UserSerializer, LoginSerializer)
from .models import User

from .util import get_tokens_for_user

import jwt

class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            data = serializer.data
            data.pop('password')
            return Response(status=status.HTTP_201_CREATED, data=data)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)


class LoginView(APIView):
    def post(self, request):
        login_serializer = LoginSerializer(data=request.data)
        if login_serializer.is_valid():
            email = request.data.get('email')
            password = request.data.get('password')
        else:
            return Response(data=login_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.filter(email=email).first()
        if user is None:
            raise AuthenticationFailed('User not found!')
        if not user.check_password(password):
            raise AuthenticationFailed('Invalid password!')
        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }
        # token = jwt.encode(payload, 'secret', algorithm='HS256')
        token = get_tokens_for_user(user=user)
        # decode_token = jwt.decode(token, "secret", algorithms=["HS256"])
        # print(f'decode_token: {decode_token}')
        if token:
            return Response(data={'token': token}, status=status.HTTP_200_OK)
        else:
            return Response(data={'status': 'failed'}, status=status.HTTP_400_BAD_REQUEST)


class GroupView(APIView):
    def get(self, request):
        print(f'Group view')
        groups = Group.objects.values_list('name', flat=True)
        return Response(status=status.HTTP_200_OK, data=groups)
