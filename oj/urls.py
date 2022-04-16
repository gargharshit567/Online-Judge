
from django.contrib import admin
from django.urls import path,include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('ojuser/', include('ojuser.urls')),
    path('question/', include('question.urls')),
]
