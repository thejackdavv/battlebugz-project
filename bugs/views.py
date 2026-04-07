from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from bugs.forms import BugCreateForm, BugEditForm
from bugs.models import Bug
from common.mixins import CombinedMixin


# Create your views here.

class BugListView(CombinedMixin, ListView):
    queryset = Bug.objects.select_related('natural_habitat', 'owner')
    context_object_name = 'bugs'
    paginate_by = 4

    def get_queryset(self):
        queryset = super().get_queryset()
        filter_type = self.request.GET.get('filter')
        if filter_type == 'my_bugs' and self.request.user.is_authenticated:
            queryset = queryset.filter(owner=self.request.user.profile)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_filter'] = self.request.GET.get('filter', 'all')
        return context

class BugDetailView(LoginRequiredMixin, DetailView):
    model = Bug
    context_object_name = 'bug'

class BugCreateView(LoginRequiredMixin, CreateView):
    model = Bug
    form_class = BugCreateForm
    template_name = 'bugs/bug_create.html'

    def form_valid(self, form):
        if not self.request.user.is_staff:
            form.instance.owner = self.request.user.profile
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('bugs:details', kwargs={'pk': self.object.pk})

def change_active_bug(request, pk):
    bug = get_object_or_404(Bug, pk=pk)
    if request.user.profile == bug.owner:
        request.user.profile.active_bug = bug
        request.user.profile.save()
    return redirect('bugs:details', pk=pk)

class BugEditView(UpdateView):
    model = Bug
    form_class = BugEditForm
    template_name = 'bugs/bug_edit.html'

    def get_success_url(self):
        return reverse_lazy('bugs:details', kwargs={'pk': self.object.pk})

class BugDeleteView(DeleteView):
    model = Bug
    success_url = reverse_lazy('bugs:list')
