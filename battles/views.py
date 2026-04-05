from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
from django.views.generic import DetailView, ListView, DeleteView

from battles.battle_system import create_battle
from battles.models import Battle
from bugs.models import Bug
from locations.models import Location


# Create your views here.
@login_required
@require_POST
def battle_start_view(request, location_pk):
    location = get_object_or_404(Location, pk=location_pk)
    defender_id = request.POST.get('defender_id')
    if not defender_id:
        messages.error(request, 'Select an opponent!')
        return redirect('locations:details', pk=location_pk)

    defender = get_object_or_404(Bug, pk=defender_id)
    attacker = request.user.profile.active_bug

    if not attacker:
        messages.error(request, 'Activate a bug to start a battle!')
        return redirect('locations:details', pk=location_pk)

    if defender == attacker:
        messages.error(request, 'You cannot battle against yourself!')
        return redirect('locations:details', pk=location_pk)

    battle = create_battle(attacker, defender, location)
    return redirect('battles:detail' , pk=battle.pk)

class BattleDetailView(LoginRequiredMixin, DetailView):
    model = Battle
    template_name = 'battles/battle_detail.html'
    context_object_name = 'battle'

class BattleListView(ListView):
    queryset = Battle.objects.select_related('attacker', 'defender', 'winner', 'location').order_by('-time_stamp')
    template_name = 'battles/battle_list.html'
    context_object_name = 'battles'
    paginate_by = 5

class BattleDeleteView(PermissionRequiredMixin, DeleteView):
    model = Battle
    success_url = reverse_lazy('battles:list')
    permission_required = 'battles.delete_battle'
