
from rest_framework import serializers
from .models import (CustomUser, Company)
from django.contrib.auth import authenticate
from django.utils.translation import ugettext_lazy as _

class CompanySerializer(serializers.ModelSerializer):
    """
    Class for defining how blacklisted token request and response object should look like.
    """
    class Meta:
        """
        Class container containing information of the model.
        """
        model = Company
        fields = ("id", "company_name", "address", 'company_email', 'phone_number')

class UserCreationSerializer(serializers.ModelSerializer):
    company=CompanySerializer()
    class Meta:
        model = CustomUser
        fields = ['id', 'role_id', 'fullname', 'email',
                  'password', 'address', 'company','contact_number']
        extra_kwargs = {
            'fullname': {
                'error_messages': {
                    'blank': 'Fullname is required.',
                    'null': 'Fullname is required.',
                    'required': 'Fullname is required.'
                }},
            'email': {
                'error_messages': {
                    'blank': 'Email is required.',
                    'null': 'Email is required.',
                    'required': 'Email is required.'
                }
            },
            'password': {
                'write_only': True
            },
        }

    def validate(self, data):
        data['email'] = data['email'].strip()
        return data

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            fullname=validated_data.pop('fullname'),
            role_id=validated_data.pop('role_id'),
            email=validated_data.pop('email'),
            address=validated_data.pop('address'),
            password=validated_data.pop('password'),
            contact_number=validated_data.pop('contact_number'),
            company=validated_data.pop('company'),
        )
        return user

class UserLoginSerializer(serializers.Serializer):

    email = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    default_error_messages = {
        'inactive_account': _('User account is disabled.'),
        'invalid_credentials': _('Unable to login with provided credentials.')
    }

    def validate(self, attrs):
        self.user = authenticate(email=attrs.pop(
            "email"), password=attrs.pop('password'))

        if self.user:
            if not self.user.is_active:
                raise serializers.ValidationError(
                    self.error_messages['inactive_account'])
            return attrs
        else:
            raise serializers.ValidationError(
                self.error_messages['invalid_credentials'])
