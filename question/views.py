from django.shortcuts import render
from ojuser.models import Ojuser
from django.contrib.auth.models import User
from .serializers import QuestionSerializer
from rest_framework.decorators import api_view,permission_classes
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from .models import Question
# Create your views here.

@api_view(['GET'])
@permission_classes([AllowAny])
def getQuestion(request):
    try:
        question = Question.objects.get(id =request.query_params.get('id'))
    except ObjectDoesNotExist:
        return JsonResponse({
            'status' : 'failed',
            'code' :404,
            'Error Message': 'Question not Found!'
            })
    
    return JsonResponse({
        'status': 'succeded',
        'code': 200,
        'data': question,
        })
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createQuestion(request):
    serializer= QuestionSerializer(data= request.data)
    serializer.is_valid(raise_exception= True)
    ojuser = Ojuser.objects.get(username = request.user.username)
    question = Question.objects.create(**serializer.data)
    question.creator = request.user
    question.save()
    return JsonResponse({
        'status': 'succeded',
        'code': 200,
    
        })