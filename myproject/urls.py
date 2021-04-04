from django.contrib import admin
from django.urls import include
from django.urls import path

urlpatterns = [
    path('', include('myproject.core.urls', namespace='core')),
    path('admin/', admin.site.urls),
]
