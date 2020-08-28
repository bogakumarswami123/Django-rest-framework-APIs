from django.conf.urls import url
from .views import CreateEmployeeAPIView,GetEmployeesAPIView,EmployeeDeletionAPIView,EditEmployeeAPIView



urlpatterns = [
    url('employeeList', GetEmployeesAPIView.as_view(), name='employee-list'),
    url('createEmployee', CreateEmployeeAPIView.as_view(), name='create-employee'),
    url('deleteEmployee', EmployeeDeletionAPIView.as_view(), name='delete-employee'),
    url('updateEmployee', EditEmployeeAPIView.as_view(), name='update-employee'),
]