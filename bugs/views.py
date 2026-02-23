from django.shortcuts import render
from django.views.generic import ListView, DetailView

from bugs.models import Bug


# Create your views here.

class BugListView(ListView):
    model = Bug
    context_object_name = 'bugs'

class BugDetailView(DetailView):
    model = Bug
    context_object_name = 'bug'
