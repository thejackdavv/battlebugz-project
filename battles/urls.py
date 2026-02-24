from django.urls import path

from battles.views import BattleDetailView, battle_start_view, BattleListView

app_name = 'battles'
urlpatterns = [
    path('', BattleListView.as_view(), name='list'),
    path('<int:pk>/', BattleDetailView.as_view(), name='detail'),
    path('start/<int:location_pk>/', battle_start_view, name='start'),

]