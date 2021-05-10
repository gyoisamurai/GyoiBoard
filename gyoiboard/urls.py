from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('atd/', include('atd.urls')),
    path('gyoithon/', include('gyoithon.urls')),
    path('admin/', admin.site.urls),
]
