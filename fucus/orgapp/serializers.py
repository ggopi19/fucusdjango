from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import (Organization, User)


class UserSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=255)
    phone = serializers.CharField(max_length=15)
    email = serializers.EmailField()
    organization = serializers.CharField(max_length=255)
    birthdate = serializers.DateField(format='%m-%d-%Y')
    password = serializers.CharField(max_length=20)

    class Meta:
        model = User
        fields = ('name', 'phone', 'email', 'organization', 'birthdate', 'password')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    def validate(self, attr):
        data = Organization.objects.filter(name__icontains=attr['organization']).first()
        print(f'data: {data}')
        if not data:
            list_of_orgs = Organization.objects.values_list('name', flat=True)
            if list_of_orgs:
                raise serializers.ValidationError(
                    f'Organization name not present in table, please provide one of -> [{",".join(list_of_orgs)}]'
                )
            else:
                raise serializers.ValidationError(
                    f'Organization name not present in table'
                )
        else:
            attr['organization'] = data
        attr['is_staff'] = True
        # As of now setting as admin, will be changed down the line
        attr['is_superuser'] = True
        return attr


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=20)
