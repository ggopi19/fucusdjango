from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from .managers import CustomUserManager

phone_regex = RegexValidator(
    regex=r'^\+?1?\d{9,15}$',  # +1 480 845 7793 example
    message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
)


class Organization(models.Model):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=15, validators=[phone_regex])
    address = models.CharField(max_length=500)

    def __str__(self):
        return f'{self.name}'


class User(AbstractUser, PermissionsMixin):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=15, validators=[phone_regex])
    email = models.EmailField(unique=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    birthdate = models.DateField()
    username = None  # Override the username filed, marking not required
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    class Meta:
        unique_together = ('email', 'organization')

    def __str__(self):
        return f'User {self.name}, {self.phone}, {self.email}'
