from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from common.mixins import CombinedMixin
from locations.forms import LocationCreateForm, LocationEditForm, FoodCreateForm
from locations.models import Location, Food


# Create your views here.


class LocationListView(CombinedMixin, ListView):
    queryset = Location.objects.prefetch_related('bugs', 'foods', 'battles')
    context_object_name = 'locations'
    template_name = 'locations/location_list.html'
    paginate_by = 4

class LocationDetailView(DetailView):
    model = Location
    context_object_name = 'location'
    template_name = 'locations/location_detail.html'


class LocationCreateView(CreateView):
    model = Location
    form_class = LocationCreateForm
    template_name = 'locations/location_create.html'

    def get_success_url(self):
        return reverse_lazy('locations:details', kwargs={'pk': self.object.pk})


class LocationEditView(UpdateView):
    model = Location
    form_class = LocationEditForm
    template_name = 'locations/location_edit.html'

    def get_success_url(self):
        return reverse_lazy('locations:details', kwargs={'pk': self.object.pk})

class LocationDeleteView(DeleteView):
    model = Location
    success_url = reverse_lazy('locations:list')


class FoodCreateView(CreateView):
    model = Food
    form_class = FoodCreateForm
    template_name = 'locations/foods/food_create.html'

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

class FoodDeleteView(DeleteView):
    model = Food
    template_name = 'locations/foods/food_confirm_delete.html'
    pk_url_kwarg = 'food_pk'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['location'] = get_object_or_404(Location, pk=self.kwargs['pk'])
        return context

    def get_success_url(self):
        return reverse_lazy('locations:details', kwargs={'pk': self.kwargs['pk']})

