from django.forms import ModelForm

from .models import (
    Tag,
    NewsLink,
    Startup
)
from .mixins import SlugCleanMixin


class TagForm(SlugCleanMixin,
              ModelForm):
    class Meta:
        model = Tag
        fields = '__all__'

    def clean_name(self):
        return self.cleaned_data['name'].lower()


class NewsLinkForm(ModelForm):
    class Meta:
        model = NewsLink
        fields = '__all__'


class StartupForm(SlugCleanMixin,
                  ModelForm):
    class Meta:
        model = Startup
        fields = '__all__'
