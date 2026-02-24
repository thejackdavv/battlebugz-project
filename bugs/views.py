from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from bugs.forms import BugCreateForm, BugEditForm
from bugs.models import Bug


# Create your views here.

class BugListView(ListView):
    queryset = Bug.objects.select_related('natural_habitat')
    context_object_name = 'bugs'
    paginate_by = 4

    def get_paginate_by(self, queryset):
        per_page = self.request.GET.get('per_page')
        if per_page:
            try:
                return int(per_page)
            except (TypeError, ValueError):
                pass
        return super().get_paginate_by(queryset)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['per_page_choices'] = [2, 4, 8, 16, 32]
        context['paginate_by'] = self.get_paginate_by(self.get_queryset())
        return context

    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.GET.get('q')
        if q:
            qs = qs.filter(name__icontains=q) | qs.filter(type__icontains=q)
        return qs


class BugDetailView(DetailView):
    model = Bug
    context_object_name = 'bug'

class BugCreateView(CreateView):
    model = Bug
    form_class = BugCreateForm
    template_name = 'bugs/bug_create.html'

    def get_success_url(self):
        return reverse_lazy('bugs:details', kwargs={'pk': self.object.pk})

def change_active_bug(request, pk):
    bug = Bug.objects.get(pk=pk)
    bug.is_active = not bug.is_active
    bug.save()
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