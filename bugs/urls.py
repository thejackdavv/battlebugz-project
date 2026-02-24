from django.urls import path, include

from bugs.views import BugListView, BugDetailView, BugCreateView, change_active_bug, BugEditView, BugDeleteView

app_name = 'bugs'
urlpatterns = [
    path('', BugListView.as_view(), name='list'),
    path('<int:pk>/', include([
        path('', BugDetailView.as_view(), name='details'),
        path('change-active/', change_active_bug, name='change_active'),
        path('edit/', BugEditView.as_view(), name='edit'),
        path('delete/', BugDeleteView.as_view(), name='delete'),
    ])),
    path('create/', BugCreateView.as_view(), name='create'),

]