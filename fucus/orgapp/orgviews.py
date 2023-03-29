from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .models import User, Organization
from .authentication import CustomAuthentication
from .util import get_user_from_token


class OrgListView(APIView):
    authentication_classes = [CustomAuthentication, ]

    # authentication_classes = []

    def get(self, request, id):
        """
        GET /api/organizations/{id}/ Retrieve organization information if request user is
        `Administrator` or `Viewer
        """
        headers = request.headers
        token = headers.get('token')
        user = get_user_from_token(token)
        if id:
            org = Organization.objects.filter(id=id).first()
            if org:
                info = list()
                users = User.objects.filter(organization=org)
                for u in users:
                    if u.groups.filter(name__in=['Administrator', 'Viewer']):
                        info.append({
                            'id': u.id,
                            'name': u.name,
                            'phone': u.phone,
                            'organization': u.organization,
                            'birthdate': u.birthdate
                        })
                return Response(status=status.HTTP_200_OK, data=info)
            else:
                return Response(status=status.HTTP_204_NO_CONTENT, data={'status': 'no records found'})
        # ------>

    def patch(self, request, id):
        """
        PATCH /api/organizations /{id} Update organization if request user is `Administrator`.
        """
        headers = request.headers
        token = headers.get('token')
        user = get_user_from_token(token)
        if id:
            org = Organization.objects.filter(id=id).first()
            if org:
                users = User.objects.filter(organization=org).first()
                group = users.groups.filter(name='Administrator')
                if group:
                    data = request.data
                    org_info = Organization.objects.filter(name=data.get('name')).first()
                    if org_info:
                        users.organization = org_info
                    return Response(status=status.HTTP_200_OK, data=data)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'status': 'no records found'})


class OrgDetailsView(APIView):
    authentication_classes = [CustomAuthentication, ]

    # authentication_classes = []

    def get(self, request, id):
        """
        • GET /api/organization/{id}/users List all the users for the user organization if user is
        `Administrator` or `Viewer`. Must return just id and name of the user
        """
        headers = request.headers
        token = headers.get('token')
        user = get_user_from_token(token)
        if id:
            org = Organization.objects.filter(id=id).first()
            if org:
                info = list()
                users = User.objects.filter(organization=org)
                for u in users:
                    if u.groups.filter(name__in=['Administrator', 'Viewer']):
                        info.append({
                            'id': u.id,
                            'name': u.name
                        })
                return Response(status=status.HTTP_200_OK, data=info)
            else:
                return Response(status=status.HTTP_204_NO_CONTENT, data={'status': 'no records found'})
        # ------>


class OrgDetailsLevelView(APIView):
    authentication_classes = [CustomAuthentication, ]

    # authentication_classes = []

    def get(self, request, org_id, user_id):
        """
        • GET /api/organization/{id}/users/{id}/ Retrieve user id and name if if user is `Administrator`
        or `Viewer
        """
        headers = request.headers
        token = headers.get('token')
        user = get_user_from_token(token)
        if id:
            org = Organization.objects.filter(id=org_id).first()
            if org:
                info = list()
                users = User.objects.filter(id=user_id, organization=org)
                for u in users:
                    if u.groups.filter(name__in=['Administrator', 'Viewer']):
                        info.append({
                            'id': u.id,
                            'name': u.name
                        })
                return Response(status=status.HTTP_200_OK, data=info)
            else:
                return Response(status=status.HTTP_204_NO_CONTENT, data={'status': 'no records found'})
        # ------>
