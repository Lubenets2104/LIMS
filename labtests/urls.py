from django.urls import path, include
from django.contrib.auth import views as django_auth_views
from rest_framework.routers import DefaultRouter
from . import views, api_views, auth_views

# API Router
router = DefaultRouter()
router.register(r'materials', api_views.MaterialViewSet)
router.register(r'gosts', api_views.GOSTViewSet)
router.register(r'mixnames', api_views.MixNameViewSet)
router.register(r'indicators', api_views.IndicatorViewSet)
router.register(r'samples', api_views.TestSampleViewSet)

urlpatterns = [
    # Authentication views
    path('login/', django_auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', django_auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', views.register_view, name='register'),
    path('password-change/', django_auth_views.PasswordChangeView.as_view(
        template_name='registration/password_change.html',
        success_url='/profile/'
    ), name='password_change'),
    
    # Profile views
    path('profile/', views.profile_view, name='profile'),
    
    # Web views (original Django templates)
    path('', views.sample_list, name='sample_list'),
    path('add/', views.add_sample, name='add_sample'),
    
    # AJAX endpoints for cascading dropdowns
    path('ajax/load-gosts/', views.load_gosts, name='ajax_load_gosts'),
    path('ajax/load-mixes/', views.load_mixes, name='ajax_load_mixes'),
    path('ajax/load-indicators/', views.load_indicators, name='ajax_load_indicators'),
    
    # Sample actions
    path('samples/<int:pk>/delete/', views.delete_sample, name='delete_sample'),
    path('samples/<int:pk>/update_status/', views.update_sample_status, name='update_sample_status'),
    path('samples/<int:pk>/test/', views.sample_test_form, name='sample_test_form'),
    path('samples/<int:pk>/shchps/', views.shchps_test_form, name='sample_shchps_test_form'),
    path('samples/<int:pk>/asphalt-core/', views.asphalt_core_test_form, name='sample_asphalt_core_test_form'),
    path('samples/<int:pk>/results/', views.sample_test_results, name='sample_test_results'),
    path('samples/<int:pk>/autosave/', views.autosave_test_result, name='autosave_test_result'),
    
    # Test and debug pages
    path('test-js/', views.test_js, name='test_js'),
    path('samples/<int:pk>/debug/', views.debug_data, name='debug_data'),
    path('check-emulsion-data/', views.check_emulsion_data, name='check_emulsion_data'),
    
    # API endpoints
    path('api/', include(router.urls)),
    
    # Auth endpoints
    path('api-auth/login/', auth_views.api_login, name='api_login'),
    path('api-auth/logout/', auth_views.api_logout, name='api_logout'),
    path('api/auth/user/', auth_views.get_current_user, name='api_current_user'),
]
