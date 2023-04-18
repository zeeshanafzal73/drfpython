from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('',include("jobportal.urls")),
    path('api-auth/', include('rest_framework.urls')),
    path('rest_auth/', include('rest_auth.urls')),
    path('rest_auth/registration/', include('rest_auth.registration.urls')),
    path('admin/', admin.site.urls),
]
