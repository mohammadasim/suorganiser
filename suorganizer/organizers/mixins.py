from django.forms import forms
from django.shortcuts import redirect, render


class SlugCleanMixin:
    """
    Mixin class for slug cleaning method
    """

    def clean_slug(self):
        new_slug = self.cleaned_data['slug'].lower()
        if new_slug == 'create':
            raise forms.ValidationError('Slug may not be "create".')
        return new_slug


class ObjectCreateMixin:
    form_class = None
    template_name = ''

    def get(self, request):
        return render(request,
                      self.template_name,
                      {'form': self.form_class()})

    def post(self, request):
        bound_form = self.template_name(request.POST)
        if bound_form.is_valid():
            new_object = bound_form.save()
            return redirect(new_object)
        else:
            return render(request,
                          self.template_name,
                          {'form': bound_form})