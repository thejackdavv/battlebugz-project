from django import forms

from bugs.bug_constants import MAX_POINTS_PER_STAT
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

class BugSearchForm(forms.Form):
    q = forms.CharField(
        max_length=100,
        required=False,
        label='',
    )