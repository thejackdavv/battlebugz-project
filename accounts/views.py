from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView

from django.contrib.auth.models import Group
from accounts.forms import ProfileUpdateForm, CustomPasswordChangeForm, AssignGroupForm, CustomUserCreationForm
from accounts.models import Profile


# Create your views here.


class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('accounts:login-view')

    def form_valid(self, form):
        response = super().form_valid(form)
        if form.cleaned_data.get('is_moderator'):
            group = Group.objects.filter(name='Global Moderators').first()
            if group:
                self.object.groups.add(group)
            else:
                messages.warning(self.request, "Global Moderators group not found. Please contact an admin.")
        return response

class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = Profile


class ProfileUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Profile
    form_class = ProfileUpdateForm
    template_name = 'accounts/profile_form.html'

    def test_func(self):
        profile = self.get_object()
        return self.request.user == profile.user or self.request.user.has_perm('accounts.change_profile')

    def get_success_url(self):
        return reverse_lazy('accounts:profile-view', kwargs={'pk': self.object.pk})

class ProfileDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Profile
    template_name = 'accounts/profile_confirm_delete.html'
    success_url = reverse_lazy('common:welcome')

    def test_func(self):
        profile = self.get_object()
        return self.request.user == profile.user or self.request.user.has_perm('accounts.delete_profile')

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

class SetUnusablePasswordView(PermissionRequiredMixin, View):
    permission_required = 'accounts.can_set_unusable_password'

    def post(self, request, pk):
        profile = get_object_or_404(Profile, pk=pk)
        user = profile.user
        
        if user == request.user:
            messages.error(request, "You cannot ban yourself!")
        else:
            user.set_unusable_password()
            user.save()
            messages.success(request, f"Password for user {user.username} has been set to unusable. They can no longer log in.")
        
        return redirect('accounts:profile-view', pk=pk)

class AssignGroupView(PermissionRequiredMixin, View):
    permission_required = 'accounts.can_assign_groups'
    template_name = 'accounts/assign_group.html'

    def get(self, request, pk):
        profile = get_object_or_404(Profile, pk=pk)
        initial_groups = profile.user.groups.all()
        form = AssignGroupForm(initial={'groups': initial_groups})
        return render(request, self.template_name, {'form': form, 'profile': profile})

    def post(self, request, pk):
        profile = get_object_or_404(Profile, pk=pk)
        form = AssignGroupForm(request.POST)
        if form.is_valid():
            profile.user.groups.set(form.cleaned_data['groups'])
            messages.success(request, f"Groups for user {profile.user.username} have been updated.")
            return redirect('accounts:profile-view', pk=pk)
        return render(request, self.template_name, {'form': form, 'profile': profile})
