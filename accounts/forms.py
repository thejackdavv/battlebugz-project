from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordChangeForm, UserCreationForm
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError

from accounts.models import Profile

UserModel = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    is_moderator = forms.BooleanField(
        required=False,
        label="Register as Global Moderator",
        help_text="If checked, you will be added to the Global Moderators group."
    )

    class Meta(UserCreationForm.Meta):
        model = UserModel
        fields = UserCreationForm.Meta.fields + ('is_moderator',)

class AssignGroupForm(forms.Form):
    groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Select Groups",
        help_text="Choose one or more groups to assign to this user."
    )

class CustomPasswordChangeForm(PasswordChangeForm):
    def clean(self):
        cleaned_data = super().clean()
        old_password = cleaned_data.get("old_password")
        new_password1 = cleaned_data.get("new_password1")

        if old_password and new_password1 and old_password == new_password1:
            raise ValidationError(
                "Your new password must be different from your old password.",
                code='password_same',
            )
        return cleaned_data


class ProfileUpdateForm(forms.ModelForm):
    first_name = forms.CharField(
        max_length=150, 
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Enter your first name'})
    )
    last_name = forms.CharField(
        max_length=150, 
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Enter your last name'})
    )
    email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={'placeholder': 'Enter your email address'})
    )

    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'email', 'date_of_birth', 'bio')
        labels = {
            'date_of_birth': 'Birthday',
            'bio': 'Personal Bio',
        }
        help_texts = {
            'date_of_birth': 'Format: YYYY-MM-DD',
            'bio': 'Tell us a bit about yourself and your BattleBugz journey!',
        }
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'placeholder': 'YYYY-MM-DD'}),
            'bio': forms.Textarea(attrs={'placeholder': 'Share your story...', 'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.user:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['email'].initial = self.instance.user.email

    def save(self, commit=True):
        profile = super().save(commit=False)
        user = profile.user
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            profile.save()
        return profile
