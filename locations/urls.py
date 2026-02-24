from django.urls import path, include

from locations.views import LocationListView, LocationDetailView, LocationCreateView, LocationEditView, \
    LocationDeleteView, FoodCreateView, FoodDeleteView

app_name = 'locations'

foodpatterns = [
    path('create/', FoodCreateView.as_view(), name='food-create'),
    path('<int:food_pk>/delete/', FoodDeleteView.as_view(), name='food-delete'),
]
urlpatterns = [
    path('', LocationListView.as_view(), name='list'),
    path('<int:pk>/', include([
            path('', LocationDetailView.as_view(), name='details'),
            path('edit/', LocationEditView.as_view(), name='edit'),
            path('delete/', LocationDeleteView.as_view(), name='delete'),
            path('foods/', include(foodpatterns)),
    ])),
    path('create/', LocationCreateView.as_view(), name='create'),
]

