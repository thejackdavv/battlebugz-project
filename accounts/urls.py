from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, include

from accounts.views import (
    RegisterView, ProfileDetailView, ProfileUpdateView, ProfileDeleteView,
    CustomPasswordChangeView, CustomPasswordChangeDoneView, SetUnusablePasswordView,
    AssignGroupView
)

app_name = 'accounts'

password_actions_patterns = [
    path('password_change/', CustomPasswordChangeView.as_view(), name='password-change-view'),
    path('password_change/done/', CustomPasswordChangeDoneView.as_view(), name='password_change_done'),
]
urlpatterns = [
    path('login/', LoginView.as_view(redirect_authenticated_user=True), name='login-view'),
    path('logout/', LogoutView.as_view(), name='logout-view'),
    path('register/', RegisterView.as_view(), name='register-view'),
    path('profile/<int:pk>/', include([
        path('', ProfileDetailView.as_view(), name='profile-view'),
        path('edit/', ProfileUpdateView.as_view(), name='edit-view'),
        path('delete/', ProfileDeleteView.as_view(), name='delete-view'),
        path('ban/', SetUnusablePasswordView.as_view(), name='set-unusable-password'),
        path('assign-group/', AssignGroupView.as_view(), name='assign-group'),
    ])),
    path('', include(password_actions_patterns))
]