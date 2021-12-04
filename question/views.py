from django.shortcuts import render
from django.forms.models import model_to_dict   
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
        'data': model_to_dict( question ),
        })
    
@api_view(['POST'])
@permission_classes([AllowAny])
def createQuestion(request):
    serializer= QuestionSerializer(data= request.data)
    serializer.is_valid(raise_exception= True)
    question = Question.objects.create(**serializer.data)
    return JsonResponse({
        'status': 'succeded',
        'code': 200,
        'data' : question.id
        })

dirame = os.getcwd()
dirTests = os.path.join(dirame, 'testcase_i_o')
if os.path.isdir(dirTests) == False:
    os.mkdir(dirTests)
@api_view(['POST'])
@permission_classes([AllowAny])
def createTestCase(request):
    #serializer
    try:
    
        fin= request.FILES['input']
        fout= request.FILES['output']
        question = Question.objects.get(id = request.data['questionId'])
        cnt= question.test_case_cnt +1 
        input_file_name=  f'./testcase_i_o/in_{question.code}_{cnt}'
        output_file_name= f'./testcase_i_o/out_{question.code}_{cnt}'

        input_file= open(input_file_name,'w')
        for f in fin.chunks():
            input_file.write(f.decode('ascii'))

        output_file= open(output_file_name,'w')
        for f in fout.chunks():
            output_file.write(f.decode('ascii'))

        testCase = TestCase.objects.create(testcase_input= input_file_name, testcase_output= output_file_name)
        testCase.questionId= question
        testCase.save()
        question.test_case_cnt= cnt
        question.save()
    except Exception as e:
        print(e)
    
    return JsonResponse({
        'status': 'succeded',
        'code': 200,
    })
    


dirame = os.getcwd()
dirCodes = os.path.join(dirame, 'codes')
if os.path.isdir(dirCodes) == False:
    os.mkdir(dirCodes)

queue=[]
@api_view(['POST'])
@permission_classes([AllowAny])
def submit(request):
    print(request.data['language'])
    language = request.data['language']
    solution = request.data['solution']
    question = request.data['question']
    print('1')
    jobId = uuid.uuid4().hex
    jobId = jobId + '.' + language
    filepath = os.path.join(dirCodes, jobId)
    f = open(filepath, 'w')
    f.write(solution)
    f.close()
    queue.append(1)
    loop()
    print(filepath)
    ans = compileCppFile(filepath, question,jobId)
    print(ans)
    return JsonResponse({'status':'succeeded', 
     'code':200, 
     'data':ans})


dirOutputs = os.path.join(dirame, 'outputs')
if os.path.isdir(dirOutputs) == False:
    os.mkdir(dirOutputs)

def loop():
    while(queue):
        ans= queue.pop(0)
        print(ans)
        

def compileCppFile(filepath, question, jodId):
    
    try:

        flag= False
        status= subprocess.run("docker ps -aq -f name='^try$'",shell=True, check= True,stdout=subprocess.PIPE, stderr= subprocess.PIPE)
        #print(status)
        if(status.stdout):
            result=  subprocess.run("docker ps -aq -f name='^try$' -f status='running'",shell=True, check= True, stdout=subprocess.PIPE ,stderr= subprocess.PIPE)
            if not result.stdout:
                flag=True
                id=str(status.stdout)[2:-3]

                status=  subprocess.run(f"docker rm {id}",shell=True, check= True, stderr= subprocess.PIPE)
        else:
            flag= True
        
        if(flag):
            subprocess.run("docker run -dt --name try ojgcc /bin/bash",shell=True, check= True, stderr= subprocess.PIPE)
        
        copyCmd= ['docker cp '+filepath+' try:/compile/main.cpp']
        status = subprocess.run(copyCmd,shell = True,executable="/bin/bash",check=True, stderr=subprocess.PIPE)
        status= subprocess.run('docker exec -w /compile try g++ -o a.out main.cpp',timeout=2.1,shell = True,executable="/bin/bash",check=True, stderr=subprocess.PIPE)
        print("compiled success")

        testcase = TestCase.objects.filter(questionId =  question)
        outputFile= './outputs/out.txt'
        for case in testcase:
            print(case)

            myin= open(case.testcase_input)
            myop = open(outputFile, 'w')
            
            status1 = subprocess.run("docker exec -i -w /compile try ./a.out",timeout=1, shell=True, check=True,stdin= myin, stdout=myop, stderr=subprocess.PIPE)
            myop.close()
            myop = open(outputFile)
            testout = open(case.testcase_output)
            i =myop.readlines()
            j =testout.readlines()
            if(i!=j):
                return "WA"
        return "AC"

    except subprocess.TimeoutExpired:
        print('TLE timeout')
        return "TLE"

    except subprocess.CalledProcessError as e:
        return e.stderr.decode()
