from django.urls import path
from . import views

urlpatterns = [
    path('', lambda r: views.redirect('/dashboard/')),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('campaigns/', views.campaign_list, name='campaign_list'),
    path('campaigns/create/', views.campaign_create, name='campaign_create'),
    path('campaigns/<int:pk>/edit/', views.campaign_edit, name='campaign_edit'),
    path('campaigns/<int:pk>/delete/', views.campaign_delete, name='campaign_delete'),
    path('subscribers/', views.subscriber_list, name='subscriber_list'),
    path('subscribers/create/', views.subscriber_create, name='subscriber_create'),
    path('subscribers/<int:pk>/edit/', views.subscriber_edit, name='subscriber_edit'),
    path('subscribers/<int:pk>/delete/', views.subscriber_delete, name='subscriber_delete'),
    path('emailtemplates/', views.emailtemplate_list, name='emailtemplate_list'),
    path('emailtemplates/create/', views.emailtemplate_create, name='emailtemplate_create'),
    path('emailtemplates/<int:pk>/edit/', views.emailtemplate_edit, name='emailtemplate_edit'),
    path('emailtemplates/<int:pk>/delete/', views.emailtemplate_delete, name='emailtemplate_delete'),
    path('settings/', views.settings_view, name='settings'),
    path('api/stats/', views.api_stats, name='api_stats'),
]
