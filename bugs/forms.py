from django import forms

from bugs.bug_constants import (
    MAX_POINTS_PER_STAT,
    ALLOCATION_POINTS,
    BASE_HP,
    BASE_ARMOR,
    BASE_STRENGTH,
    BASE_MOBILITY,
    BASE_HEALING_FACTOR)
from bugs.game_config import TYPE_BONUSES
from bugs.models import Bug


class BugCreateForm(forms.ModelForm):

    hp_points = forms.IntegerField(
        min_value=0, 
        max_value=MAX_POINTS_PER_STAT,
        label="HP Points",
        help_text=f"Points to add to base health. Max {MAX_POINTS_PER_STAT}.",
        widget=forms.NumberInput(attrs={'placeholder': '0', 'class': 'form-control'})
    )
    armor_points = forms.IntegerField(
        min_value=0, 
        max_value=MAX_POINTS_PER_STAT,
        label="Armor Points",
        help_text=f"Points to add to base armor. Max {MAX_POINTS_PER_STAT}.",
        widget=forms.NumberInput(attrs={'placeholder': '0', 'class': 'form-control'})
    )
    strength_points = forms.IntegerField(
        min_value=0, 
        max_value=MAX_POINTS_PER_STAT,
        label="Strength Points",
        help_text=f"Points to add to base strength. Max {MAX_POINTS_PER_STAT}.",
        widget=forms.NumberInput(attrs={'placeholder': '0', 'class': 'form-control'})
    )
    mobility_points = forms.IntegerField(
        min_value=0, 
        max_value=MAX_POINTS_PER_STAT,
        label="Mobility Points",
        help_text=f"Points to add to base mobility. Max {MAX_POINTS_PER_STAT}.",
        widget=forms.NumberInput(attrs={'placeholder': '0', 'class': 'form-control'})
    )
    healing_factor_points = forms.IntegerField(
        min_value=0, 
        max_value=MAX_POINTS_PER_STAT,
        label="Healing Points",
        help_text=f"Points to add to base healing factor. Max {MAX_POINTS_PER_STAT}.",
        widget=forms.NumberInput(attrs={'placeholder': '0', 'class': 'form-control'})
    )

    class Meta:
        model = Bug
        fields = (
            'name',
            'type',
            'natural_habitat',
            'image_url',
            'description',
        )
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter bug name', 'class': 'form-control'}),
            'type': forms.Select(attrs={'class': 'form-control'}),
            'natural_habitat': forms.Select(attrs={'class': 'form-control'}),
            'image_url': forms.URLInput(attrs={'placeholder': 'https://example.com/bug.png', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'placeholder': 'Describe your bug...', 'class': 'form-control', 'rows': 3}),
        }
        help_texts = {
            'name': 'Choose a unique name for your bug.',
            'type': 'The type determines elemental bonuses.',
            'natural_habitat': 'Where this bug naturally lives.',
            'image_url': 'Link to a valid image representing your bug.',
        }

    def clean(self):
        cleaned_data = super().clean()

        hp_points = cleaned_data.get('hp_points', 0)
        armor_points = cleaned_data.get('armor_points', 0)
        strength_points = cleaned_data.get('strength_points', 0)
        mobility_points = cleaned_data.get('mobility_points', 0)
        healing_factor_points = cleaned_data.get('healing_factor_points', 0)

        total = hp_points + armor_points + strength_points + mobility_points + healing_factor_points
        if total != ALLOCATION_POINTS:
            raise forms.ValidationError(
                f"Total points allocated must be exactly {ALLOCATION_POINTS}. Currently allocated: {total}."
            )
        return cleaned_data

    def save(self, commit = True):
        bug = super().save(commit=False)

        bug.max_health_points = BASE_HP + self.cleaned_data['hp_points']
        bug.armor = BASE_ARMOR + self.cleaned_data['armor_points']
        bug.strength = BASE_STRENGTH + self.cleaned_data['strength_points']
        bug.mobility = BASE_MOBILITY + self.cleaned_data['mobility_points']
        bug.healing_factor = BASE_HEALING_FACTOR + self.cleaned_data['healing_factor_points']

        if not bug.pk:
            bonuses = TYPE_BONUSES.get(bug.type, {})

            for stat, amount in bonuses.items():
                setattr(bug, stat, getattr(bug, stat) + amount)



        if commit:
            bug.save()
            # Automatically add bug to its natural habitat's inhabitants
            if bug.natural_habitat:
                bug.natural_habitat.inhabitants.add(bug)
        return bug

class BugEditForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['type'].disabled = True
        self.fields['natural_habitat'].disabled = True

    class Meta:
        model = Bug
        fields = (
            'name',
            'type',
            'natural_habitat',
            'image_url',
            'description',
        )
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Update bug name', 'class': 'form-control'}),
            'type': forms.Select(attrs={'class': 'form-control'}),
            'natural_habitat': forms.Select(attrs={'class': 'form-control'}),
            'image_url': forms.URLInput(attrs={'placeholder': 'Update image URL', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'placeholder': 'Update description', 'class': 'form-control', 'rows': 3}),
        }
        help_texts = {
            'type': 'Type cannot be changed after creation.',
            'natural_habitat': 'Natural habitat cannot be changed after creation.',
        }


class BugSearchForm(forms.Form):
    q = forms.CharField(
        max_length=100,
        required=False,
        label='',
        widget=forms.TextInput(attrs={'placeholder': 'Search bugs by name...', 'class': 'form-control'})
    )
