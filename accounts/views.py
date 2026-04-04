from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView

from accounts.forms import ProfileUpdateForm, CustomPasswordChangeForm
from accounts.models import Profile


# Create your views here.


class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('accounts:login-view')

class ProfileDetailView(DetailView):
    model = Profile


class ProfileUpdateView(UpdateView):
    model = Profile
    form_class = ProfileUpdateForm
    template_name = 'accounts/profile_form.html'

    def get_success_url(self):
        return reverse_lazy('accounts:profile-view', kwargs={'pk': self.object.pk})

class ProfileDeleteView(DeleteView):
    model = Profile
    template_name = 'accounts/profile_confirm_delete.html'
    success_url = reverse_lazy('common:welcome')

    def form_valid(self, form):
        user = self.object.user
        success_url = self.get_success_url()
        user.delete()
        return HttpResponseRedirect(success_url)


class CustomPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    form_class = CustomPasswordChangeForm
    success_url = reverse_lazy('accounts:password_change_done')
    template_name = 'registration/password_change_form.html'


class CustomPasswordChangeDoneView(LoginRequiredMixin, PasswordChangeDoneView):
    template_name = 'registration/password_change_done.html'