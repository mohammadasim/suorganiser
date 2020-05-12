from django import forms

from .models import (
    Tag,
    NewsLink,
    Startup
)
from .mixins import SlugCleanMixin


class TagForm(SlugCleanMixin,
              forms.ModelForm):
    class Meta:
        model = Tag
        fields = '__all__'

    def clean_name(self):
        return self.cleaned_data['name'].lower()


class NewsLinkForm(forms.ModelForm):
    class Meta:
        model = NewsLink
        fields = '__all__'


class StartupForm(SlugCleanMixin,
                  forms.ModelForm):
    class Meta:
        model = Startup
        fields = '__all__'
