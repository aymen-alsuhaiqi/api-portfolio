from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import *
from django.contrib.auth.models import User
from .serializer import *
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics
import jwt,datetime

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

@api_view(['POST'])
def login(request):
    if request.method == 'POST':
        data = request.data
        username = data.get('username')
        print("__🔻🔻🔻__ ~ file: views.py:47 ~ username:", username)
        password = data.get('password')
        print("__🔻🔻🔻__ ~ file: views.py:48 ~ password:", password)
        user = User.objects.get(username=username)
        print("__🔻🔻🔻__ ~ file: views.py:51 ~ user:", user.password)
        if user and user.check_password(password):
            paylod = {
                'id':user.pk,
                'username':user.username,
                # 'date':datetime.datetime.now(),
                # 'exp': datetime.datetime.now() + datetime.timedelta(days=1),
            }
            token = jwt.encode(paylod,'secret','HS256')
            print("__🔻🔻🔻__ ~ file: views.py:60 ~ token:", token)

            response = Response()
            response.set_cookie('token',token,httponly=True)

            response.data = {
                'token':token,
                'user_id':user.pk,
            }
            return response
        return Response({'error':'Invalid credentials'}, status=401)

class SkillsView(generics.ListCreateAPIView):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer

    def create(self,request, *args, **kwargs):
        serializer = SkillSerializer(data=request.data)
        
        if serializer.is_valid():
            token = request.COOKIES.get('token')
            
            if not token:
                return Response({'error': 'Token not provided'}, status=400)
            
            try:
                payload = jwt.decode(token, 'secret', algorithms=['HS256'])
            except jwt.ExpiredSignatureError:
                return Response({'error': 'Token has expired'}, status=401)
            except jwt.InvalidTokenError:
                return Response({'error': 'Invalid token'}, status=401)

            try:
                user = User.objects.get(id=payload['id'])
            except User.DoesNotExist:
                return Response({'error': 'User not found'}, status=404)
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
            
