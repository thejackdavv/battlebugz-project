from django import forms

from locations.models import Location, Food


class LocationBaseForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = '__all__'
        error_messages = {
            'name': {
                'required' : 'How would you visit a place without a name?'
            },
            'description': {
                'required' : 'A place without a description is like a book without words.'
            }
        }

        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter location name'}),
            'description': forms.Textarea(attrs={'placeholder': 'Describe the location'}),
        }

class LocationCreateForm(LocationBaseForm):
    pass

class LocationEditForm(LocationBaseForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['type'].disabled = True
        self.fields['type'].required = False


class FoodBaseForm(forms.ModelForm):
    class Meta:
        model = Food
        fields = ['name', 'stat']
        error_messages = {
            'name': {
                'required' : 'Please give the food a name.'
            },
            'stat': {
                'required' : 'Do you want pointless food? Please select a stat.'
            }
        }

        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'What\'s the name of the food?'}),
            'stat': forms.Select(attrs={'placeholder': 'Which stat does the food increase?'}),
        }

class FoodCreateForm(FoodBaseForm):
    def __init__(self, *args, **kwargs):
        self.location = kwargs.pop('location', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        food = super().save(commit=False)
        if commit:
            food.save()
            if self.location:
                food.location.add(self.location)
        return food
