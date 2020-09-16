"""
A module containing form classes
for organizers app
"""
from django import forms
from django.forms import HiddenInput, SelectDateWidget

from .mixins import SlugCleanMixin
from .models import (
    Tag,
    NewsLink,
    Startup
)


class TagForm(SlugCleanMixin,
              forms.ModelForm):
    """Form class for tag"""

    class Meta:
        model = Tag
        fields = '__all__'

    def clean_name(self):
        return self.cleaned_data['name'].lower()


class NewsLinkForm(
    SlugCleanMixin,
    forms.ModelForm):
    """Form class for newslink"""
    pub_date = forms.DateField(label='Date Published', initial='yyyy-mm-dd')
    class Meta:
        model = NewsLink
        fields = '__all__'
        widgets = {'startup': HiddenInput()}


class StartupForm(SlugCleanMixin,
                  forms.ModelForm):
    """Form class for startup"""
    founded_date = forms.DateField(label='Date Founded', initial='yyyy-mm-dd')

    class Meta:
        model = Startup
        fields = '__all__'
