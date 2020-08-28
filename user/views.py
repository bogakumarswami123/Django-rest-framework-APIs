from .serializers import UserCreationSerializer,CompanySerializer,UserLoginSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import (CreateAPIView, GenericAPIView)
from .models import CustomUser, get_tokens_for_user, Company
from .utils import ResponseInfo
from django.contrib.auth.hashers import make_password

class UserCreationAPIView(CreateAPIView):
    """
    Class for creating API view for users registration.
    """
    def __init__(self, **kwargs):
        """
         Constructor function for formatting the web response to return.
        """
        self.response_format = ResponseInfo().response
        super(UserCreationAPIView, self).__init__(**kwargs)

    authentication_classes = ()
    permission_classes = ()
    serializer_class = UserCreationSerializer

    def create(self, request, *args, **kwargs):
        """
        Function for validating and creating the users if valid.
        """
        try:
            temp_password = request.data['password']
            password = make_password(temp_password)
            check_user = CustomUser.objects.filter(email=request.data['email'])

            check_company = Company.objects.filter(company_name=request.data['company_name'])
            if not check_user :
                if not check_company:
                    Company.objects.create(company_name=request.data['company_name'])
                company_id = Company.objects.filter(company_name=request.data['company_name'])

                CustomUser.objects.create(role_id=1, fullname=request.data['fullname'],
                                          email=request.data['email'],
                                          password=password, address=request.data['address'],
                                          contact_number=request.data['contact_number'])

                obj = CustomUser.objects.exclude().get(email=request.data['email'])
                jwt_token = get_tokens_for_user(obj)
                email_data = request.data['email']
                user_data = CustomUser.objects.get(email=email_data)

                data = {
                    "token": jwt_token,
                    "document_verification_status": "Approved",
                    "custom_user": UserCreationSerializer(user_data).data,
                }

                self.response_format["data"] = data
                self.response_format["status_code"] = status.HTTP_201_CREATED
                self.response_format["error"] = None
                self.response_format['message'] = "User registered successfully."
                return Response(self.response_format, status.HTTP_201_CREATED)

            else:
                self.response_format["data"] = None
                self.response_format["status_code"] = status.HTTP_409_CONFLICT
                self.response_format["error"] = "Failure"
                self.response_format['message'] = "User email already exist."
                return Response(self.response_format, status.HTTP_409_CONFLICT)
        except Exception as e:
            self.response_format["status_code"] = status.HTTP_500_INTERNAL_SERVER_ERROR
            self.response_format["message"] = "Something went wrong, please try again"
            return Response(self.response_format, status.HTTP_500_INTERNAL_SERVER_ERROR)

class UserLoginAPIView(GenericAPIView):
    """
    Class for creating API view for users login.
    """

    def __init__(self, **kwargs):
        """
         Constructor function for formatting the web response to return.
        """
        self.response_format = ResponseInfo().response
        super(UserLoginAPIView, self).__init__(**kwargs)

    authentication_classes = ()
    permission_classes = ()
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        """
        Function for validating and logging in the users if valid.
        """
        serializer = self.get_serializer(data=request.data)
        print('data', request.data)
        if serializer.is_valid():
            users = serializer.user
            email_data = request.data['email']
            user_data = CustomUser.objects.get(email=email_data)

            if user_data.deleted:
                self.response_format["status_code"] = status.HTTP_404_NOT_FOUND
                self.response_format["error"] = None
                self.response_format['message'] = "User does not exist."
                return Response(self.response_format, status.HTTP_404_NOT_FOUND)

            else:
                obj = users
                jwt_token = get_tokens_for_user(obj)
                data = {
                    "token": jwt_token,
                    "document_verification_status": "Approved",
                    "custom_user": UserCreationSerializer(user_data).data,
                }

                self.response_format["data"] = data
                self.response_format["status_code"] = status.HTTP_200_OK
                self.response_format["error"] = None
                self.response_format['message'] = "Logged in successfully."
                return Response(self.response_format, status.HTTP_200_OK)

        else:
            self.response_format["data"] = None
            self.response_format["status_code"] = status.HTTP_500_INTERNAL_SERVER_ERROR
            self.response_format["error"] = "Failure"
            self.response_format['message'] = "Invalid email id or password."
            return Response(self.response_format, status.HTTP_500_INTERNAL_SERVER_ERROR)
