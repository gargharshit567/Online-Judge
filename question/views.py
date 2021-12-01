from django.shortcuts import render
from ojuser.models import Ojuser
from django.contrib.auth.models import User
from .serializers import QuestionSerializer, FileSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from .models import Question, TestCase
import os.path, uuid, subprocess
import sys


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
@permission_classes([AllowAny])
def createQuestion(request):
    serializer= QuestionSerializer(data= request.data)
    serializer.is_valid(raise_exception= True)
<<<<<<< HEAD
    ojuser = Ojuser.objects.get(username = request.user.username)
=======
   # print(request.user.username)
   # print(type(request.user))
   # ojuser = Ojuser.objects.get(username = request.user.username)
>>>>>>> b48633518561a8a19e2c49d49bb5e799a9414e02
    question = Question.objects.create(**serializer.data)
   # question.creator = ojuser
   # question.save()
    return JsonResponse({
        'status': 'succeded',
        'code': 200,
        'data' : question.id
        })

@api_view(['POST'])
@permission_classes([AllowAny])
def createTestCase(request):
    #serializer

    print(request.data['testcase'])
    testCase = TestCase.objects.create(**request.data['testcase'])
    question = Question.objects.get(id = request.data['questionId'])
    testCase.questionId = question
    testCase.save()
    return JsonResponse({
        'status': 'succeded',
        'code': 200,
        'data' : testCase.id
    })
    


dirame = os.getcwd()
dirCodes = os.path.join(dirame, 'codes')
if os.path.isdir(dirCodes) == False:
    os.mkdir(dirCodes)

@api_view(['POST'])
@permission_classes([AllowAny])
def createFile(request):
    print(request.data['language'])
    language = request.data['language']
    code = request.data['code']
    print('1')
    jobId = uuid.uuid4().hex
    jobId = jobId + '.' + language
    filepath = os.path.join(dirCodes, jobId)
    f = open(filepath, 'w')
    f.write(code)
    print(filepath)
    return JsonResponse({'status':'succeeded', 
     'code':200, 
     'data':filepath})


dirOutputs = os.path.join(dirame, 'outputs')
if os.path.isdir(dirOutputs) == False:
    os.mkdir(dirOutputs)

@api_view(['POST'])
@permission_classes([AllowAny])
def compileCppFile(request):
    question = request.data['question']
    filepath = request.data['filepath']
    #jobId = os.path.basename(filepath).split('.')[0] + '.' + 'out'
    jobId = "a.out"
    outPath = os.path.join(dirOutputs, jobId)
    outPutt = os.path.join(dirOutputs, 'o.outp')
    #myop = open(outPutt, 'w')
    cmd = ['g++ ' + filepath + ' -o ' + outPath] #+ ' && cd ' + dirOutputs + ' && ./' + jobId]
    #cmd1 = ['cd ' + dirOutputs + ' && ./' + jobId]
    try:
        status = subprocess.run(cmd,timeout=2.1,shell = True,check=True, stderr=subprocess.PIPE)
        print("compiled success")
        print(status)
        if status.returncode == 0:
       # status1 = subprocess.run(cmd1,timeout=2.1, shell=True, check=True, stdout=myop)
            verdict = runCppFile(dirOutputs, jobId, outPutt, question)
            return JsonResponse({'status':'succeeded', 
            'code':200, 
            'data':verdict})
        else:
            return JsonResponse({'status':'succeeded', 
            'code':200, 
            'data':'Compilation Error'})
    except subprocess.TimeoutExpired:
        print('TLE timeout')
        return JsonResponse({'status':'succeeded', 
         'code':200, 
         'data':'TLE timeout'})
    except subprocess.CalledProcessError as e:
        print('Compilation Error')
        #print('stderr: {}'.format(e.stderr.decode(sys.getfilesystemencoding())))
        #print('stdout: {}'.format(e.output.decode(sys.getfilesystemencoding())))
        print(str(e.stderr.decode()))
        #print(STDOUT)
        return JsonResponse({'status':'succeeded', 
         'code':200, 
         'data':format(e.stderr.decode())})
        
         
        
        #status = subprocess
def runCppFile(dirOutputs,runFile,outputFile,question):
    myop = open(outputFile, 'w')
    cmd1 = ['cd ' + dirOutputs + ' && ./' + runFile]
    testcase = TestCase.objects.filter(questionId =  question)
    #testcase1 = TestCase.objects.get(questionId =  question)
    print(testcase)
    for case in testcase:
        print(case)
        myip = open(case.testcase_input)

        myop = open(outputFile, 'w')
        cmd1 = ['cd '+dirOutputs + ' && ./'+runFile]
        try:
            status1 = subprocess.run(cmd1,timeout=1, shell=True, check=True, stdout=myop, stdin = myip, stderr=subprocess.STDOUT)
            myop.close()
            myop = open(outputFile)
            testout = open(case.testcase_output)
            i =''
            j =''
            for l1 in testout:
                i +=l1
                print(i)
            for l2 in myop:
                j +=l2  
                print(j)
            if(i!=j):
                return "WA"
            
    
        except subprocess.TimeoutExpired:
            return "TLE"


    return "AC"

