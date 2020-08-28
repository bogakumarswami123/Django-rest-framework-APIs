from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.generics import (GenericAPIView)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import getAllEmployeeCreationSer
from user.permissions import IsTokenValid
from user.utils import ResponseInfo
from mysite.settings import SECRET_KEY
from user.models import CustomUser
from .models import Employee
from rest_framework.decorators import APIView



class CreateEmployeeAPIView(GenericAPIView):
    """
    Class for creating API view for create a new Request .
    """
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated, IsTokenValid)
    serializer_class = getAllEmployeeCreationSer

    def __init__(self, **kwargs):
        """
         Constructor function for formatting the web response to return.
        """
        self.response_format = ResponseInfo().response
        super(CreateEmployeeAPIView, self).__init__(**kwargs)

    def post(self, request, *args, **kwargs):
        """
        Function for creating new request if valid.
        """
        try:
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                self.response_format["status_code"] = status.HTTP_201_CREATED
                self.response_format["error"] = None
                self.response_format['message'] = "Request created successfully."
                return Response(self.response_format, status.HTTP_201_CREATED)
            else:
                self.response_format["status_code"] = status.HTTP_500_INTERNAL_SERVER_ERROR
                self.response_format["error"] = serializer.errors
                self.response_format['message'] = "Something went wrong please try again."
                return Response(self.response_format, status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            self.response_format["status_code"] = status.HTTP_500_INTERNAL_SERVER_ERROR
            self.response_format["message"] = "Something went wrong, please try again"
            return Response(self.response_format, status.HTTP_500_INTERNAL_SERVER_ERROR)


class  GetEmployeesAPIView(GenericAPIView):
    """
    Class for creating API view for getting the Requests for particular status .
    """
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated, IsTokenValid)
    serializer_class = getAllEmployeeCreationSer

    def __init__(self, **kwargs):
        """
         Constructor function for formatting the web response to return.
        """
        self.response_format = ResponseInfo().response
        super(GetEmployeesAPIView, self).__init__(**kwargs)

    def post(self, request, *args, **kwargs):
        """
        Function for getting the requests for particular status if valid.
        """
        # token = request.META['HTTP_AUTHORIZATION'].split(" ")[1]
        # user_id = jwt.decode(token, SECRET_KEY)['user_id']
        # company_data = CustomUser.objects.get(id=user_id)
        # print("company_data", company_data.company.id)
        #
        # serializer = self.get_serializer(data=request.data.user_id)
        try:
            ordered_data = Employee.objects.filter()

            data = getAllEmployeeCreationSer(ordered_data, many=True).data
            self.response_format["status_code"] = status.HTTP_200_OK
            self.response_format["error"] = None
            self.response_format['data'] = data
            return Response(self.response_format, status.HTTP_200_OK)

        except Exception as e:
            print(e)
            self.response_format["status_code"] = status.HTTP_500_INTERNAL_SERVER_ERROR
            self.response_format["message"] = "Something went wrong, please try again"
            return Response(self.response_format, status.HTTP_500_INTERNAL_SERVER_ERROR)

        # if serializer.is_valid():
        #
        #
        # else:
        #     self.response_format["status_code"] = status.HTTP_500_INTERNAL_SERVER_ERROR
        #     self.response_format["error"] = "Failure"
        #     self.response_format['message'] = "Something went wrong please try again."
            return Response(self.response_format, status.HTTP_500_INTERNAL_SERVER_ERROR)


class EmployeeDeletionAPIView(APIView):
    """
    Class for creating API view for Lender user deletion
    """
    permission_classes = (IsAuthenticated, IsTokenValid)
    authentication_classes = (JWTAuthentication,)
    serializer_class = getAllEmployeeCreationSer

    def __init__(self, **kwargs):
        """
         Constructor function for formatting the web response to return.
        """
        self.response_format = ResponseInfo().response
        super(EmployeeDeletionAPIView, self).__init__(**kwargs)

    def delete(self, request):
        """
        Function for creating function for Employee deletion
        """
        try:
            employee_id = request.data['id']
            employee_object = Employee.objects.get(id=employee_id)
            if employee_object:
                employee_object.delete()
                self.response_format["status_code"] = status.HTTP_200_OK
                self.response_format["error"] = None
                self.response_format['message'] = "Employee successfully deleted."
                return Response(self.response_format, status.HTTP_200_OK)
            else:
                self.response_format["status_code"] = status.HTTP_404_NOT_FOUND
                self.response_format["error"] = "Failure"
                self.response_format['message'] = "User does not exist."
                return Response(self.response_format, status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(e)
            self.response_format['status_code'] = status.HTTP_500_INTERNAL_SERVER_ERROR
            self.response_format['message'] = "Something went wrong please try again."
            return Response(self.response_format, status.HTTP_500_INTERNAL_SERVER_ERROR)


class EditEmployeeAPIView(GenericAPIView):
    """
       Class for creating API view for editing employee details.
       """

    def __init__(self, **kwargs):
        """
         Constructor function for formatting the web response to return.
        """
        self.response_format = ResponseInfo().response
        super(EditEmployeeAPIView, self).__init__(**kwargs)

    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated, IsTokenValid)
    serializer_class = getAllEmployeeCreationSer

    def put(self, request, *args, **kwargs):
        """
        Function for Updating the user details if the user is valid.
        """
        try:

            user_id = request.data['id']
            fullname = request.data['fullname']
            work_address = request.data['work_address']
            home_address = request.data['home_address']
            age = request.data['age']
            designation = request.data['designation']
            salary = request.data['salary']
            experience = request.data['experience']
            Employee.objects.filter(id=user_id).update(fullname=fullname, work_address=work_address,
                                                         home_address=home_address,
                                                         designation=designation, age=age,
                                                         salary=salary, experience=experience)
            self.response_format["status_code"] = status.HTTP_200_OK
            self.response_format["error"] = None
            self.response_format['message'] = "Successfully updated user details."
            return Response(self.response_format, status.HTTP_200_OK)
            # if id_check:
            #     if not email_check:
            #
            #     else:
            #         self.response_format['message'] = "Email already exist."
            #         self.response_format["status_code"] = status.HTTP_409_CONFLICT
            #         self.response_format["error"] = "Failure"
            #         return Response(self.response_format, status.HTTP_409_CONFLICT)
            # else:
            #     self.response_format['message'] = "User does not exist."
            #     self.response_format["status_code"] = status.HTTP_404_NOT_FOUND
            #     self.response_format["error"] = "Failure"
            #     return Response(self.response_format, status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(e)
            self.response_format["status_code"] = status.HTTP_500_INTERNAL_SERVER_ERROR
            self.response_format["message"] = "Something went wrong, please try again"
            return Response(self.response_format, status.HTTP_500_INTERNAL_SERVER_ERROR)
