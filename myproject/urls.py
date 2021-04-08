from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    # path('', include('myproject.core.urls', namespace='core')),
    #
    # path('accounts/', include('myproject.accounts.urls')),  # sem namespace
    path('admin/', admin.site.urls),
]
