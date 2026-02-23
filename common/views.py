from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

# Create your views here.

def welcome_view(request: HttpRequest) -> HttpResponse:
    return render(request, 'common/welcome.html')