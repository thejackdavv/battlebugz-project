from django.db.models import Count
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView

from bugs.models import Bug
from locations.models import Location


# Create your views here.

class HomePageView(TemplateView):
    template_name = 'common/welcome.html'

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        bugs = Bug.objects.select_related('natural_habitat').all()
        context['active_bug'] = bugs.filter(is_active=True).first()
        context['top_bug'] = max(bugs, key=lambda b: b.total_power, default=None)
        context['top_location'] = Location.objects.annotate(num_bugs=Count('bugs')).order_by('-num_bugs').first()
        return context


