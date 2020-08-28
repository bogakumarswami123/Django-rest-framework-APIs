from django.db import models
from user.models import CustomUser


class Employee(models.Model):

    fullname = models.TextField(max_length=200, null=False, blank=False)
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE,
                                null=False, blank=False, related_name="request_user_id")
    designation = models.TextField(max_length=1000, null=False, blank=False)
    work_address = models.TextField(max_length=1000, null=True, blank=True)
    home_address = models.TextField(max_length=1000, null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    salary = models.IntegerField(null=True, blank=True)
    experience = models.IntegerField(null=True, blank=True)

    def __str__(self):
        """
        Function to return fullname.
        """
        return self.fullname

