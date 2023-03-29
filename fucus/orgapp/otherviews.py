
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .authentication import CustomAuthentication
from .util import get_user_from_token
import socket


class OtherView(APIView):
    authentication_classes = [CustomAuthentication, ]

    # authentication_classes = []

    def get(self, request):
        """
       GET /api/info/ Should return {`user_name`, `id`, `organization_name`, `public_ip`} Public Ip
        must be the internet public IP of the server where code is running
        """
        headers = request.headers
        token = headers.get('token')
        user = get_user_from_token(token)
        hostname = socket.gethostname()
        temp = {
            'user_name': user.name,
            'id': user.id,
            'organization_name': user.organization.name,
            'public_ip': socket.gethostbyname(hostname)
        }
        return Response(status=status.HTTP_200_OK, data=temp)
