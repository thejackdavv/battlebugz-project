from django.urls import path

from common import views

urlpatterns = [
    path('', views.welcome_view, name='welcome'),
]