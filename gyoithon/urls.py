from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from gyoithon import views

app_name = 'gyoithon'
urlpatterns = [
    path('top/', views.top_page, name='top_page'),
    path('organization/add', views.registration, name='registration'),
    path('organization/list', views.list_organization, name='list_organization'),
    path('organization/<int:organization_id>/edit', views.edit_organization, name='edit_organization'),
    path('organization/<int:organization_id>/del', views.delete_organization, name='delete_organization'),
    path('organization/<int:organization_id>/', views.detail_organization, name='detail_organization'),
    path('organization/<int:organization_id>/domain/add', views.registration_domain, name='registration_domain'),
    path('organization/<int:organization_id>/domain/<int:domain_id>/edit', views.edit_domain, name='edit_domain'),
    path('organization/<int:organization_id>/domain/<int:domain_id>/del', views.delete_domain, name='delete_domain'),
    path('organization/<int:organization_id>/domain/<int:domain_id>/', views.detail_domain, name='detail_domain'),
    path('organization/<int:organization_id>/domain/<int:domain_id>/subdomain/add', views.registration_subdomain, name='registration_subdomain'),
    path('organization/<int:organization_id>/domain/<int:domain_id>/subdomain/<int:subdomain_id>/edit', views.edit_subdomain, name='edit_subdomain'),
    path('organization/<int:organization_id>/domain/<int:domain_id>/subdomain/<int:subdomain_id>/del', views.delete_subdomain, name='delete_subdomain'),
    path('organization/<int:organization_id>/domain/<int:domain_id>/subdomain/<int:subdomain_id>/', views.detail_subdomain, name='detail_subdomain'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
