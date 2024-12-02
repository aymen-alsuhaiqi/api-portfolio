from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import *
from django.contrib.auth.models import User
from .serializer import *
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics,status
import jwt,datetime
from rest_framework.exceptions import ValidationError
from rest_framework import serializers

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
    def get_queryset(self):
        token = self.request.headers.get('Authorization')
        if self.request.COOKIES.get('token'):
            token = self.request.COOKIES.get('token')

        if not token:
            raise ValidationError({'error': 'Token not provided'})

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise ValidationError({'error': 'Token has expired'})
        except jwt.InvalidTokenError:
            raise ValidationError({'error': 'Invalid token'})

        try:
            user = User.objects.get(id=payload['id'])
        except User.DoesNotExist:
            raise ValidationError({'error': 'User not found'})

        return UserInformation.objects.filter(user_id=user)
    
    def get(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    def create(self,request):
        serializer = UserInfoSerializer(data=request.data)
        
        if serializer.is_valid():
            token = request.headers.get('Authorization')
            if request.COOKIES.get('token'):
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
            serializer.validated_data['user_id'] = user
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=100)
# class Token(serializers.Serializer):
#     token = serializers.CharField(max_length=100)
    

@swagger_auto_schema(
        method='post',
        request_body=LoginSerializer,
        # responses={
        #     status.HTTP_200_OK: Token,}
)
@api_view(['POST'])
def login(request):
    if request.method == 'POST':
        data = request.data
        username = data.get('userName')
        password = data.get('password')
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({'error':'User not found'}, status=status.HTTP_401_UNAUTHORIZED)
        if user and user.check_password(password):
            paylod = {
                'id':user.pk,
                'username':user.username,
                'date':str(datetime.datetime.now()),
                'exp': (datetime.datetime.now() + datetime.timedelta(minutes=60)).timestamp(),
            }
            token = jwt.encode(paylod,'secret','HS256')

            response = Response()
            response.set_cookie('token',token,httponly=True)
            # response.headers.

            response.data = {
                'data':{'userName':username,'email':user.email,'authority':['user','admin'],'token':token},
            }
            response.status_code = 200
            return response
        return Response({'error':'Invalid credentials'}, status=401)

class SkillsView(generics.ListCreateAPIView):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer

    def get_queryset(self):
        token = self.request.headers.get('Authorization')
        if self.request.COOKIES.get('token'):
            token = self.request.COOKIES.get('token')

        if not token:
            raise ValidationError({'error': 'Token not provided'})

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise ValidationError({'error': 'Token has expired'})
        except jwt.InvalidTokenError:
            raise ValidationError({'error': 'Invalid token'})

        try:
            user = User.objects.get(id=payload['id'])
        except User.DoesNotExist:
            raise ValidationError({'error': 'User not found'})

        return Skill.objects.filter(user_id=user)
    
    def get(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self,request):
        serializer = SkillSerializer(data=request.data)
        
        if serializer.is_valid():
            token = request.headers.get('Authorization')
            if request.COOKIES.get('token'):
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
            serializer.validated_data['user_id'] = user
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    
class ExperienceView(generics.ListCreateAPIView):
    queryset = Experience.objects.all()
    serializer_class = ExperienceSerializer

    def get_queryset(self):
        token = self.request.headers.get('Authorization')
        if self.request.COOKIES.get('token'):
            token = self.request.COOKIES.get('token')

        if not token:
            raise ValidationError({'error': 'Token not provided'})

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise ValidationError({'error': 'Token has expired'})
        except jwt.InvalidTokenError:
            raise ValidationError({'error': 'Invalid token'})

        try:
            user = User.objects.get(id=payload['id'])
        except User.DoesNotExist:
            raise ValidationError({'error': 'User not found'})

        return Experience.objects.filter(user_id=user)
    
    def get(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self,request):
        serializer = ExperienceSerializer(data=request.data)
        
        if serializer.is_valid():
            token = request.headers.get('Authorization')
            if request.COOKIES.get('token'):
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
            serializer.validated_data['user_id'] = user
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
            
class EducationView(generics.ListCreateAPIView):
    queryset = Education.objects.all()
    serializer_class = EducationSerializer

    def get_queryset(self):
        token = self.request.headers.get('Authorization')
        if self.request.COOKIES.get('token'):
            token = self.request.COOKIES.get('token')

        if not token:
            raise ValidationError({'error': 'Token not provided'})

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise ValidationError({'error': 'Token has expired'})
        except jwt.InvalidTokenError:
            raise ValidationError({'error': 'Invalid token'})

        try:
            user = User.objects.get(id=payload['id'])
        except User.DoesNotExist:
            raise ValidationError({'error': 'User not found'})

        return Education.objects.filter(user_id=user)
    
    def get(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self,request):
        serializer = EducationSerializer(data=request.data)
        
        if serializer.is_valid():
            token = request.headers.get('Authorization')
            if request.COOKIES.get('token'):
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
            serializer.validated_data['user_id'] = user
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

class WorkView(generics.ListCreateAPIView):
    queryset = Works.objects.all()
    serializer_class = WorkSerializer

    def get_queryset(self):
        token = self.request.headers.get('Authorization')
        if self.request.COOKIES.get('token'):
            token = self.request.COOKIES.get('token')

        if not token:
            raise ValidationError({'error': 'Token not provided'})

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise ValidationError({'error': 'Token has expired'})
        except jwt.InvalidTokenError:
            raise ValidationError({'error': 'Invalid token'})

        try:
            user = User.objects.get(id=payload['id'])
        except User.DoesNotExist:
            raise ValidationError({'error': 'User not found'})

        return Works.objects.filter(user_id=user)
    
    def get(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self,request):
        serializer = WorkSerializer(data=request.data)
        
        if serializer.is_valid():
            token = request.headers.get('Authorization')
            if request.COOKIES.get('token'):
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
            serializer.validated_data['user_id'] = user
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    
@api_view(['GET'])
def logout(request):
    try:
        token = request.COOKIES['token']
    except Exception as e:
        return Response({'error': 'Invalid token'}, status=401)
    response = Response({'message': 'Logged out successfully'},status=status.HTTP_200_OK)
    response.delete_cookie('token')
    return response
class SkillViewUD(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SkillSerializer
    queryset = Skill.objects.all()
    lookup_field = 'id'

    def get_queryset(self):
        token = self.request.headers.get('Authorization')
        if self.request.COOKIES.get('token'):
            token = self.request.COOKIES.get('token')

        if not token:
            raise ValidationError({'error': 'Token not provided'})

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise ValidationError({'error': 'Token has expired'})
        except jwt.InvalidTokenError:
            raise ValidationError({'error': 'Invalid token'})

        try:
            user = User.objects.get(id=payload['id'])
        except User.DoesNotExist:
            raise ValidationError({'error': 'User not found'})

        try:
            query = Skill.objects.get(id=self.kwargs['id'],user_id=user)
        except Skill.DoesNotExist:
            raise ValidationError({'error': 'Skill not found'})
        return query
    
    def get(self, request,id):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=False)
        return Response(serializer.data)
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object() 
        serializer = self.get_serializer(instance, data=request.data, partial=True)

        if serializer.is_valid():
            token = request.headers.get('Authorization')
            if request.COOKIES.get('token'):
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

            if 'user_id' in serializer.validated_data:
                del serializer.validated_data['user_id'] 

            serializer.validated_data['user_id'] = user
            serializer.save()
            return Response(serializer.data, status=200)
        
        return Response(serializer.errors, status=400)

class ExperienceViewUD(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ExperienceSerializer
    queryset = Experience.objects.all()
    lookup_field = 'id'

    def get_queryset(self):
        token = self.request.headers.get('Authorization')
        if self.request.COOKIES.get('token'):
            token = self.request.COOKIES.get('token')

        if not token:
            raise ValidationError({'error': 'Token not provided'})

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise ValidationError({'error': 'Token has expired'})
        except jwt.InvalidTokenError:
            raise ValidationError({'error': 'Invalid token'})

        try:
            user = User.objects.get(id=payload['id'])
        except User.DoesNotExist:
            raise ValidationError({'error': 'User not found'})

        try:
            query = Experience.objects.get(id=self.kwargs['id'],user_id=user)
        except Experience.DoesNotExist:
            raise ValidationError({'error': 'Experience not found'})
        return query
    
    def get(self, request,id):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=False)
        return Response(serializer.data)
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object() 
        serializer = self.get_serializer(instance, data=request.data, partial=True)

        if serializer.is_valid():
            token = request.headers.get('Authorization')
            if request.COOKIES.get('token'):
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

            if 'user_id' in serializer.validated_data:
                del serializer.validated_data['user_id'] 

            serializer.validated_data['user_id'] = user
            serializer.save()
            return Response(serializer.data, status=200)
        
        return Response(serializer.errors, status=400)

class WorkViewUD(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = WorkSerializer
    queryset = Works.objects.all()
    lookup_field = 'id'

    def get_queryset(self):
        token = self.request.headers.get('Authorization')
        if self.request.COOKIES.get('token'):
            token = self.request.COOKIES.get('token')

        if not token:
            raise ValidationError({'error': 'Token not provided'})

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise ValidationError({'error': 'Token has expired'})
        except jwt.InvalidTokenError:
            raise ValidationError({'error': 'Invalid token'})

        try:
            user = User.objects.get(id=payload['id'])
        except User.DoesNotExist:
            raise ValidationError({'error': 'User not found'})

        try:
            query = Works.objects.get(id=self.kwargs['id'],user_id=user)
        except Works.DoesNotExist:
            raise ValidationError({'error': 'Works not found'})
        return query
    
    def get(self, request,id):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=False)
        return Response(serializer.data)
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object() 
        serializer = self.get_serializer(instance, data=request.data, partial=True)

        if serializer.is_valid():
            token = request.headers.get('Authorization')
            if request.COOKIES.get('token'):
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

            if 'user_id' in serializer.validated_data:
                del serializer.validated_data['user_id'] 

            serializer.validated_data['user_id'] = user
            serializer.save()
            return Response(serializer.data, status=200)
        
        return Response(serializer.errors, status=400)

class EducationViewUD(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = EducationSerializer
    queryset = Education.objects.all()
    lookup_field = 'id'

    def get_queryset(self):
        token = self.request.headers.get('Authorization')
        if self.request.COOKIES.get('token'):
            token = self.request.COOKIES.get('token')

        if not token:
            raise ValidationError({'error': 'Token not provided'})

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise ValidationError({'error': 'Token has expired'})
        except jwt.InvalidTokenError:
            raise ValidationError({'error': 'Invalid token'})

        try:
            user = User.objects.get(id=payload['id'])
        except User.DoesNotExist:
            raise ValidationError({'error': 'User not found'})

        try:
            query = Education.objects.get(id=self.kwargs['id'],user_id=user)
        except Education.DoesNotExist:
            raise ValidationError({'error': 'Education not found'})
        return query
    
    def get(self, request,id):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=False)
        return Response(serializer.data)
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object() 
        serializer = self.get_serializer(instance, data=request.data, partial=True)

        if serializer.is_valid():
            token = request.headers.get('Authorization')
            if request.COOKIES.get('token'):
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

            if 'user_id' in serializer.validated_data:
                del serializer.validated_data['user_id'] 

            serializer.validated_data['user_id'] = user
            serializer.save()
            return Response(serializer.data, status=200)
        
        return Response(serializer.errors, status=400)
class CRInformationUD(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserInfoSerializer
    queryset = UserInformation.objects.all()
    lookup_field = 'id'

    def get_queryset(self):
        token = self.request.headers.get('Authorization')
        if self.request.COOKIES.get('token'):
            token = self.request.COOKIES.get('token')

        if not token:
            raise ValidationError({'error': 'Token not provided'})

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise ValidationError({'error': 'Token has expired'})
        except jwt.InvalidTokenError:
            raise ValidationError({'error': 'Invalid token'})

        try:
            user = User.objects.get(id=payload['id'])
        except User.DoesNotExist:
            raise ValidationError({'error': 'User not found'})

        try:
            query = UserInformation.objects.get(id=self.kwargs['id'],user_id=user)
        except UserInformation.DoesNotExist:
            raise ValidationError({'error': 'UserInformation not found'})
        return query
    
    def get(self, request,id):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=False)
        return Response(serializer.data)
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object() 
        serializer = self.get_serializer(instance, data=request.data, partial=True)

        if serializer.is_valid():
            token = request.headers.get('Authorization')
            if request.COOKIES.get('token'):
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

            if 'user_id' in serializer.validated_data:
                del serializer.validated_data['user_id'] 

            serializer.validated_data['user_id'] = user
            serializer.save()
            return Response(serializer.data, status=200)
        
        return Response(serializer.errors, status=400)