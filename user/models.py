from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.contrib.auth.models import BaseUserManager
from rest_framework_simplejwt.tokens import RefreshToken


class Company(models.Model):
    """
    Class for creating company model.
    """
    company_name = models.TextField(max_length=100, unique=True, null=False, blank=False, error_messages={'unique': 'Company name already exists.'})
    address = models.TextField(null=True, blank=True)
    company_email = models.TextField(_('email address'), unique=True, null=True, error_messages={'unique': 'Email already exists.'})
    phone_number = models.TextField(null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return str(self.company_name)


class CustomUserManager(BaseUserManager):
    def create_user(self, role_id, fullname, address, email, password, contact_number,
                    company_name,
                    **extra_fields):
        user = self.model(
            email=self.normalize_email(email)
        )
        user.role_id = role_id
        user.fullname = fullname
        user.password = password
        user.address = address
        user.company_name = company_name
        user.contact_number = contact_number
        user.is_active = True
        user.is_staff = False
        user.is_superuser = False
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(
            email,
            password=password,
        )
        user.is_superuser = True
        user.is_active = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    role_id = models.CharField(max_length=100, null=False, blank=False)
    fullname = models.CharField(max_length=200, null=False, blank=False)
    email = models.EmailField(_('email address'), unique=True)
    address = models.TextField(max_length=1000, null=True, blank=True)
    contact_number = models.TextField(max_length=40, null=True, blank=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="company",
                                null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateField(default=timezone.now)
    deleted = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'

    objects = CustomUserManager()

    def __str__(self):
        """
        Function to return email.
        """
        return self.email


def get_tokens_for_user(email):
    """
    function to creates and returns JWT token in response
    """
    refresh = RefreshToken.for_user(email)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class BlackListedToken(models.Model):
    """
    Class for creating blacklisted tokens which have already been used.
    """
    token = models.CharField(max_length=500)
    timestamp = models.DateTimeField(auto_now=True)


class ForgetPassword(models.Model):

    email = models.OneToOneField('user.CustomUser', on_delete=models.CASCADE)
    otp = models.TextField(unique=True)

    created_at = models.DateField(auto_now=True)


class Meta:
    """
    Class container containing information of the model.
    """
    unique_together = "token"



