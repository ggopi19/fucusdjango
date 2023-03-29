from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.backends import TokenBackend
from rest_framework.exceptions import ValidationError
from .models import User
import jwt

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


def get_user_from_token(token):
    try:
        decoded_token = jwt.decode(token, options={'verify_signature': False})
        print(f'decoded_token: {decoded_token}')
        email = decoded_token.get('email', '')
        user = User.objects.get(email=email)
        return user
    except ValidationError as v:
        raise ValidationError('Token not found!')
