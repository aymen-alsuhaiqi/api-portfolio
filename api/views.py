from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import *
from django.contrib.auth.models import User
from .serializer import *
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics

# Create your views here.
@swagger_auto_schema(
        method='post',
        request_body=UserSerializer
)
@api_view(['GET','POST'])
def cr_user(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            data = request.data
            user = User.objects.create(username=data.get('username'), email=data.get('email'))
            user.set_password(data['password'])
            user.save()
            return Response(UserSerializer(user).data, status=201)
        return Response(serializer.errors, status=400)
    else:
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
class cr_infromation(generics.ListCreateAPIView):
    queryset = UserInformation.objects.all()
    serializer_class = UserInfoSerializer
    # parser_classes = [MultiPartParser, JSONParser]
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

