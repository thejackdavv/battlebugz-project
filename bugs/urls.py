from django.urls import path

from bugs.views import BugListView, BugDetailView

app_name = 'bugs'
urlpatterns = [
    path('', BugListView.as_view(), name='list'),
    path('<int:pk>/', BugDetailView.as_view(), name='details'),
]