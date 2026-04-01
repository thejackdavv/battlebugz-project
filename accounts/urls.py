from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, include

from accounts.views import RegisterView, ProfileDetailView, ProfileUpdateView, ProfileDeleteView

app_name = 'accounts'
urlpatterns = [
    path('login/', LoginView.as_view(redirect_authenticated_user=True), name='login-view'),
    path('logout/', LogoutView.as_view(), name='logout-view'),
    path('register/', RegisterView.as_view(), name='register-view'),
    path('profile/<int:pk>/', include([
        path('', ProfileDetailView.as_view(), name='profile-view'),
        path('edit/', ProfileUpdateView.as_view(), name='edit-view'),
        path('delete/', ProfileDeleteView.as_view(), name='delete-view'),
    ])),
]