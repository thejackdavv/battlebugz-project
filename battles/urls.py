from django.urls import path, include

from battles.views import BattleDetailView, battle_start_view, BattleListView, BattleDeleteView

app_name = 'battles'
urlpatterns = [
    path('', BattleListView.as_view(), name='list'),
    path('<int:pk>/',include([
        path('', BattleDetailView.as_view(), name='detail'),
        path('delete/', BattleDeleteView.as_view(), name='delete'),
     ])),
    path('start/<int:location_pk>/', battle_start_view, name='start'),

]