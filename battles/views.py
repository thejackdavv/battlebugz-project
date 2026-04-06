from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
from django.views.generic import DetailView, ListView, DeleteView

from battles.models import Battle
from battles.tasks import run_battle_async
from bugs.models import Bug
from common.mixins import PaginatorMixin
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

    run_battle_async.delay(attacker.pk, defender.pk, location.pk)
    messages.info(request, 'Battle started! It will appear in your history shortly.')
    return redirect('battles:list')

class BattleDetailView(LoginRequiredMixin, DetailView):
    model = Battle
    template_name = 'battles/battle_detail.html'
    context_object_name = 'battle'

class BattleListView(PaginatorMixin, ListView):
    queryset = Battle.objects.select_related(
        'attacker', 'attacker__owner', 
        'defender', 'defender__owner', 
        'winner', 'location'
    ).order_by('-time_stamp')
    template_name = 'battles/battle_list.html'
    context_object_name = 'battles'
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        filter_type = self.request.GET.get('filter')
        if filter_type == 'my_battles' and self.request.user.is_authenticated:
            profile = self.request.user.profile
            queryset = queryset.filter(
                Q(attacker__owner=profile) | Q(defender__owner=profile)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_filter'] = self.request.GET.get('filter', 'all')
        return context

class BattleDeleteView(PermissionRequiredMixin, DeleteView):
    model = Battle
    success_url = reverse_lazy('battles:list')
    permission_required = 'battles.delete_battle'
