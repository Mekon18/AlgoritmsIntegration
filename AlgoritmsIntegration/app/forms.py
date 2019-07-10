"""
Definition of forms.
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _
from Ants import const

class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'User name'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Password'}))

class BeesForm(forms.Form):
    scoutbeecount = forms.IntegerField(initial=10,min_value=1)
    bestbeecount = forms.IntegerField(initial=6,min_value=1)
    selectedbeecount = forms.IntegerField(initial=5,min_value=1)
    radius = forms.IntegerField(initial=5,min_value=1)
    iterations = forms.IntegerField(initial=100,min_value=1)
    function = forms.ChoiceField(choices=((1, "-x^2 - y^2"), (2, "Ekli"), (3, "Bukin"), (4, "Cross in tray")))

class FishForm(forms.Form):
    fish = forms.IntegerField(min_value = 1, max_value = 9999, initial = 20)
    iterations = forms.IntegerField(min_value = 1 ,max_value = 9999, initial = 100)
    weightMax = forms.IntegerField(min_value = 1, max_value = 9999, initial = 100)
    speed = forms.FloatField(min_value = 0, max_value = 9999, initial = 1)
    MinX = forms.FloatField(min_value = -9999, max_value = 9999, initial = -6)
    MaxX = forms.FloatField(min_value = -9999, max_value = 9999, initial = 6)
    MinY = forms.FloatField(min_value = -9999, max_value = 9999, initial = -6)
    MaxY = forms.FloatField(min_value = -9999, max_value = 9999, initial = 6)
    error = forms.FloatField(min_value = -9999, max_value = 9999, initial= 0.5)
    function =  forms.ChoiceField(choices = ((1, "Химмельблау"), (2, "Розенброка"), (3, "Сфера"),(4, "Растригина"), (5, "Экли")), initial = 1)

class AntsForm(forms.Form):
    model = const
    fields = ['numAnts', 'numFood', 'numObstacles']