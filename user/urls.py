from django.conf.urls import url
from .views import UserCreationAPIView, UserLoginAPIView



urlpatterns = [
    url('signup', UserCreationAPIView.as_view(), name='user-register'),
    url('login', UserLoginAPIView.as_view(), name='user-login'),
]