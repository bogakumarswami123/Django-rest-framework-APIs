from rest_framework import serializers
from .models import (Employee)


class getAllEmployeeCreationSer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['id', 'fullname', 'user_id', 'work_address', 'home_address',
                  'age', 'designation', 'salary', 'experience']
