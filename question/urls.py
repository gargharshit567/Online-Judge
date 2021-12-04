from django.urls import path
from .views import createQuestion,getQuestion,submit,runCppFile,compileCppFile, createTestCase
urlpatterns = [
    path('create', createQuestion),
    path('get', getQuestion),
    path('createFile', submit),
    path('compileCpp', compileCppFile),
    path('createTestCase', createTestCase)
]
