from django.urls import path
from . import views
urlpatterns = [
    path('create', views.createQuestion),
    path('get', views.getQuestion),
    path('createFile', views.submit),
    path('createTestCase', views.createTestCase)
]
