from django.urls import path
from .views import createQuestion,getQuestion
urlpatterns = [
    path('create', createQuestion),
    path('get/:id', getQuestion),
]
