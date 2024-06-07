from django.urls import path
from .views import *

urlpatterns = [
    path('signup', UserSignupView.as_view(), name='user-signup'),
    path('login', UserLoginView.as_view(), name='user-login'),
    path('update', UpdateUserDetailsView.as_view(), name='user-update'),
    path('adminpanel', AdminPanelView.as_view(), name='admin-panel'),
    path('password-reset', PasswordResetRequestView.as_view(), name='password-reset'),
]