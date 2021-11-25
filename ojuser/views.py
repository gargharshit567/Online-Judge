from django.shortcuts import render
from ojuser.models import Ojuser
from .serializers import UserSerializer,LoginSerializer
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.decorators import api_view,permission_classes
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    
    serializer= UserSerializer(data= request.data)
    serializer.is_valid(raise_exception= True)
    serializer.save()
    return JsonResponse({
        'status': 'succeded',
        'code': 200,
        'data': serializer.data,
        })

@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):   
    
    serializer= LoginSerializer(data= request.data)
    serializer.is_valid(raise_exception= True)
    try:
        ojuser= Ojuser.objects.get(email= serializer.data['email'])
    
    except ObjectDoesNotExist:
        raise AuthenticationFailed('User not Found! ')
    if not ojuser.check_password(serializer.data['password']):
        raise AuthenticationFailed('Wrong Password !')
    
    return JsonResponse({
        'status': 'succeded',
        'code': 200,
        'data': {
            'token': str(AccessToken().for_user(ojuser)),
            'username': ojuser.username,
        },
        })
    