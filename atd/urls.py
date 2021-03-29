from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from atd import views

app_name = 'atd'
urlpatterns = [
    path('target/', views.target_list, name='target_list'),
    path('target/upload/', views.modelform_upload, name='target_upload'),
    path('target/mod/<int:target_id>/', views.target_edit, name='target_mod'),
    path('scan/target/<int:target_id>/', views.scan_target, name='scan_target'),
    path('scan/setting/<int:target_id>/', views.scan_setting, name='scan_setting'),
    path('scan/exec/<int:target_id>/', views.scan_exec, name='scan_exec'),
    path('fix/target/<int:target_id>/', views.ScanResultList.as_view(), name='fix_target'),
    path('target/del/<int:target_id>/', views.target_del, name='target_del'),
    path('scan_result/<int:target_id>/', views.ScanResultList.as_view(), name='scan_result_list'),
    path('scan_result/mod/<int:target_id>/<int:scan_result_id>/', views.scan_result_edit, name='scan_result_mod'),
    path('scan_result/del/<int:target_id>/<int:scan_result_id>/', views.scan_result_del, name='scan_result_del'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
