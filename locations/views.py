from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, FormView

from bugs.models import Bug
from common.mixins import CombinedMixin
from locations.forage_service import forage
from locations.forms import LocationCreateForm, LocationEditForm, FoodCreateForm, FoodAddForm
from locations.models import Location, Food


# Create your views here.


class LocationListView(CombinedMixin, ListView):
    queryset = Location.objects.prefetch_related('bugs', 'foods', 'battles')
    context_object_name = 'locations'
    template_name = 'locations/location_list.html'
    paginate_by = 4

class LocationDetailView(LoginRequiredMixin, DetailView):
    model = Location
    context_object_name = 'location'
    template_name = 'locations/location_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_bug'] = self.request.user.profile.active_bug if self.request.user.is_authenticated else None
        return context


class LocationCreateView(PermissionRequiredMixin, CreateView):
    model = Location
    form_class = LocationCreateForm
    template_name = 'locations/location_create.html'
    permission_required = 'locations.add_location'

    def get_success_url(self):
        return reverse_lazy('locations:details', kwargs={'pk': self.object.pk})


class LocationEditView(PermissionRequiredMixin, UpdateView):
    model = Location
    form_class = LocationEditForm
    template_name = 'locations/location_edit.html'
    permission_required = 'locations.change_location'

    def get_success_url(self):
        return reverse_lazy('locations:details', kwargs={'pk': self.object.pk})

class LocationDeleteView(PermissionRequiredMixin, DeleteView):
    model = Location
    success_url = reverse_lazy('locations:list')
    permission_required = 'locations.delete_location'


class FoodCreateView(PermissionRequiredMixin, CreateView):
    model = Food
    form_class = FoodCreateForm
    template_name = 'locations/foods/food_create.html'
    permission_required = 'locations.add_food'

    def dispatch(self, request, *args, **kwargs):
        self.location = get_object_or_404(Location, pk=kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['location'] = self.location
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['location'] = self.location
        return context

    def get_success_url(self):
        return reverse_lazy('locations:details', kwargs={'pk': self.location.pk})

class FoodAddView(PermissionRequiredMixin, FormView):
    form_class = FoodAddForm
    template_name = 'locations/foods/food_add.html'
    permission_required = 'locations.add_food'

    def dispatch(self, request, *args, **kwargs):
        self.location = get_object_or_404(Location, pk=kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['location'] = self.location
        return kwargs

    def form_valid(self, form):
        food = form.cleaned_data['food']
        self.location.foods.add(food)
        return redirect('locations:details', pk=self.location.pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['location'] = self.location
        return context


class FoodDeleteView(PermissionRequiredMixin, DeleteView):
    model = Food
    template_name = 'locations/foods/food_confirm_delete.html'
    pk_url_kwarg = 'food_pk'
    permission_required = 'locations.delete_food'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['location'] = get_object_or_404(Location, pk=self.kwargs['pk'])
        return context

    def get_success_url(self):
        return reverse_lazy('locations:details', kwargs={'pk': self.kwargs['pk']})


class FoodRemoveFromLocationView(PermissionRequiredMixin, View):
    permission_required = 'locations.delete_food'
    def post(self, request, pk, food_pk):
        location = get_object_or_404(Location, pk=pk)
        food = get_object_or_404(Food, pk=food_pk)
        food.location.remove(location)
        return redirect('locations:details', pk=pk)


@login_required
def forage_view(request, pk):
    location = get_object_or_404(Location, pk=pk)
    active_bug = request.user.profile.active_bug

    if not active_bug:
        messages.error(request, "You need to activate a bug first")
        return redirect('locations:details', pk=pk)

    food = forage(active_bug, location)

    if food:
        messages.success(
            request,
            f"{active_bug.name} found {food.name} "
            f"(+{food.increase_amount} {food.get_stat_display()})"
        )
    else:
        messages.warning(request, 'No food found this time. Try again!')

    return redirect('locations:details', pk=pk)
