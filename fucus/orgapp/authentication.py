from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import AccessToken
from .util import get_user_from_token


class CustomAuthentication(BaseAuthentication):

    def authenticate(self, request):
        try:
            headers = request.headers
            token = headers.get('token')
            if not token:
                token = headers.get('Token')
            print(f'token: {token}')
            if not token:
                raise AuthenticationFailed('Token not present in the header')
            user = get_user_from_token(token=token)
            if not user:
                raise AuthenticationFailed('Invalid token!')
        except Exception as e:
            print(f'Exception: {e}')
            raise AuthenticationFailed('Failed to decode the token!')
