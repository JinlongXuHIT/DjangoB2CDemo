from django.shortcuts import render

# Create your views here.

from rest_framework.generics import CreateAPIView

from rest_framework.response import Response
from rest_framework.views import APIView

from . import serializers
from .models import User

# url(r'^usernames/(?P<username>\w{5,20})/count/$',views.UsernameCountView.as_view())
class UsernameCountView(APIView):
    """
    判断用户名是否存在
    """

    def get(self, request, username):
        username_count = User.objects.filter(username=username).count()

        data = {
            'username': username,
            'count': username_count,
        }
        return Response(data)


# url(r'^mobiles/(?P<mobile>1[3-9]\d{9})/count/$',views.UsernameCountView.as_view())
class MobileCountView(APIView):
    def get(self, request, mobile):
        count = User.objects.filter(mobile=mobile).count()
        data = {
            'mobile': mobile,
            'count': count,
        }
        return Response(data)


class UserView(CreateAPIView):
    serializer_class = serializers.CreateUserSerializer