from django import forms

from locations.models import Location, Food


class LocationBaseForm(forms.ModelForm):
    class Meta:
        model = Location
        exclude = ['deleted_at']
        error_messages = {
            'name': {
                'required' : 'How would you visit a place without a name?',
                'unique': 'This location already exists!'
            },
            'type': {
              'required' : 'Please specify what kind of location this is.'
            },
            'image_url': {
                'required' : 'We need an image to show how this place looks.'
            },
            'description': {
                'required' : 'A place without a description is like a book without words.'
            },
        }

        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter location name', 'class': 'form-control'}),
            'type': forms.Select(attrs={'class': 'form-control'}),
            'image_url': forms.URLInput(attrs={'placeholder': 'https://example.com/location.jpg', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'placeholder': 'Describe the location...', 'class': 'form-control', 'rows': 4}),
            'inhabitants': forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        }
        
        help_texts = {
            'type': 'Elemental type affects which bugs thrive here.',
            'image_url': 'A visual representation of the location.',
            'inhabitants': 'Select the bugs that naturally inhabit this area.',
        }

class LocationCreateForm(LocationBaseForm):
    pass

class LocationEditForm(LocationBaseForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['type'].disabled = True
        self.fields['type'].required = False
        self.fields['type'].help_text = "The location type cannot be changed once established."


class FoodBaseForm(forms.ModelForm):
    class Meta:
        model = Food
        fields = ['name', 'stat', 'increase_amount']
        labels = {
            'stat': 'Stat to Boost',
            'increase_amount': 'Boost Amount',
        }
        error_messages = {
            'name': {
                'required' : 'Please give the food a name.',
                'unique': 'This food already exists!'
            },
            'stat': {
                'required' : 'Do you want pointless food? Please select a stat.'
            },
            'increase_amount': {
                'min_value': 'The boost amount must be positive.'
            }
        }

        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'e.g. Juicy Apple', 'class': 'form-control'}),
            'stat': forms.Select(attrs={'class': 'form-control'}),
            'increase_amount': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
        }
        
        help_texts = {
            'stat': 'Which attribute will this food improve?',
            'increase_amount': 'How many points will be added to the stat?',
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


class FoodAddForm(forms.Form):
    food = forms.ModelChoiceField(
        queryset=Food.objects.none(),
        label="Select Food",
        help_text="Choose an existing food to add to this location.",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    def __init__(self, *args, **kwargs):
        location = kwargs.pop('location')
        super().__init__(*args, **kwargs)

        self.fields['food'].queryset = Food.objects.exclude(location=location)
