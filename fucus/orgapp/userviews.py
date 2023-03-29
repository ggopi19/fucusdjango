import datetime

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth.models import Group
from .serializers import (UserSerializer)
from .models import User
from .authentication import CustomAuthentication
from .util import get_user_from_token


class UsersListView(APIView):
    authentication_classes = [CustomAuthentication, ]

    # authentication_classes = []

    def get(self, request, id):
        """
        GET /api/users/ List all the users for the user organization if user is `Administrator` or
        `Viewer`. Must return all the user model fields. Should support search by name, email.
        Should support filter by phone.
        • GET /api/users/{id}/ Retrieve user information, and the organization id and name
        """
        headers = request.headers
        token = headers.get('token')
        user = get_user_from_token(token)
        if id:
            user = User.objects.filter(id=id).first()
            if user:
                org = user.organization
                temp = {
                    'org_id': org.id,
                    'org_name': org.name
                }
                return Response(status=status.HTTP_200_OK, data=temp)
            else:
                return Response(status=status.HTTP_204_NO_CONTENT, data={'status': 'no records found'})
        # ------>
        groups = user.groups.filter(name__in=['Administrator', 'Viewer'])
        print(f'groups: {groups}')
        if groups:
            user_groups = User.objects.filter(
                organization=user.organization
            ).values('id', 'name', 'phone', 'email', 'organization', 'birthdate')
            return Response(status=status.HTTP_200_OK, data=user_groups)
        else:
            return Response(status=status.HTTP_204_NO_CONTENT,
                            data={'status': 'User not part of Administrator or Viewer'})

    def post(self, request):
        """
        POST /api/users/ Create an user for the organization, must set password as well. Request
        user must be Administrator
        """
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user_obj = serializer.save()
            admin_group = Group.objects.get(name='Administrator')
            admin_group.user_set.add(user_obj)
            data = serializer.data
            data.pop('password')
            return Response(status=status.HTTP_201_CREATED, data=data)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)

    def patch(self, request, id):
        """
        PATCH /api/users/{id} Update user information for the user_id if request user is
    `       Administrator` of his organization. Or request user is user_id
        """
        data = request.data
        headers = request.headers
        token = headers.get('token')
        user = get_user_from_token(token)
        if id:
            user_from_id = User.objects.filter(id=id).first()
            groups = user.groups.filter(name='Administrator')
            #
            if user.id == user_from_id.id or groups:
                user.name = data.get('name')
                user.phone = data.get('phone')
                user.birthdate = datetime.datetime.strptime(data.get('birthdate'), '%Y-%m-%d')
                user.save()
                return Response(status=status.HTTP_200_OK, data={'status': 'record has been updated'})
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data={'status': 'user not admin or authorized to update'})

    def delete(self, request, id):
        """
        DELETE /api/users/{id} Delete user for the user_id if request user is `Administrator` of his
        organization
        """
        headers = request.headers
        token = headers.get('token')
        user = get_user_from_token(token)
        if id:
            groups = user.groups.filter(name='Administrator')
            if groups:
                user.delete()
                return Response(status=status.HTTP_204_NO_CONTENT, data={'status': 'record has been deleted'})
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data={'status': 'user not admin or authorized to delete'})
