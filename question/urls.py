from django.urls import path
from .views import createQuestion,getQuestion,createFile,runCppFile,compileCppFile, createTestCase
urlpatterns = [
    path('create', createQuestion),
    path('get', getQuestion),
    path('createFile', createFile),
    path('compileCpp', compileCppFile),
    path('createTestCase', createTestCase)
]
