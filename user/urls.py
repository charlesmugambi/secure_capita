from django.urls import path
from django.contrib.auth.views import (PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView)

from . import views


app_name = 'user'

urlpatterns = [
    path('', views.homepage, name="homepage"),
    path('register', views.register, name="register"),
    path('login_user', views.login_user, name="login_user"),
    path('dashboard', views.dashboard, name="dashboard"),
    
    path('logout', views.logout, name="logout"),
    path('password_reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    # profile paths
    path('profile/update/',views.update_profile, name='update_profile'),
    path('profile/delete/', views.delete_account, name='delete_account'),
    path('view_profile', views.view_profile, name='view_profile'),
    path('change_password/', views.change_password, name='change_password'),
    
]
