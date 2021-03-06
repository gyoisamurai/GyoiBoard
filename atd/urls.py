from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from atd import views

app_name = 'atd'
urlpatterns = [
    path('top/', views.top_page, name='top'),
    path('target/', views.target_list, name='target_list'),
    path('target/upload/', views.modelform_upload, name='target_upload'),
    path('target/reupload/<int:target_id>/', views.modelform_reupload, name='target_reupload'),
    path('target/edit/<int:target_id>/', views.target_edit, name='target_edit'),
    path('scan/setting/<int:target_id>/', views.scan_setting, name='scan_setting'),
    path('scan/setting/update/<int:target_id>/', views.update_setting, name='update_setting'),
    path('scan/exec/<int:target_id>/', views.scan_exec, name='scan_exec'),
    path('scan/detail/<int:target_id>/', views.scan_detail, name='scan_detail'),
    path('report/', views.report, name='report'),
    path('fix/target/<int:target_id>/', views.scan_exec, name='fix_target'),
    path('target/del/<int:target_id>/', views.target_del, name='target_del'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
