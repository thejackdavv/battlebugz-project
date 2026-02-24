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

    hp_points = forms.IntegerField(min_value=0, max_value=MAX_POINTS_PER_STAT)
    armor_points = forms.IntegerField(min_value=0, max_value=MAX_POINTS_PER_STAT)
    strength_points = forms.IntegerField(min_value=0, max_value=MAX_POINTS_PER_STAT)
    mobility_points = forms.IntegerField(min_value=0, max_value=MAX_POINTS_PER_STAT)
    healing_factor_points = forms.IntegerField(min_value=0, max_value=MAX_POINTS_PER_STAT)

    class Meta:
        model = Bug
        fields = (
            'name',
            'type',
            'natural_habitat',
            'image_url',
            'description',
        )

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
        return bug

class BugEditForm(forms.ModelForm):

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
            'type': forms.Select(attrs={'readonly':True, 'disabled':True}),
            'natural_habitat': forms.Select(attrs={'readonly':True, 'disabled':True}),
        }


class BugSearchForm(forms.Form):
    q = forms.CharField(
        max_length=100,
        required=False,
        label='',
    )
