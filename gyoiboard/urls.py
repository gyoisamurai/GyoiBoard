from django.contrib import admin
from django.urls import path
from django.conf.urls import include, url


urlpatterns = [
    # Administrator.
    path('admin/', admin.site.urls),

    # Applications.
    path('atd/', include('atd.urls')),
    path('gyoithon/', include('gyoithon.urls')),

    # Authentication.
    path('api-auth/', include('rest_framework.urls')),
    url(r'^rest-auth/', include('rest_auth.urls')),
    url(r'^rest-auth/registration/', include('rest_auth.registration.urls')),
]
