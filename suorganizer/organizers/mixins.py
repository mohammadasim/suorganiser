from django.forms import forms
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render, get_object_or_404


class SlugCleanMixin:
    """
    Mixin class for slug cleaning method
    """

    def clean_slug(self):
        new_slug = self.cleaned_data['slug'].lower()
        if new_slug == 'create':
            raise forms.ValidationError('Slug may not be "create".')
        return new_slug


class GetObjectMixin:
    """
    Mixin class to retrieve Tag or Startup object from DB
    """
    model = None

    def get_object(self, slug):
        return get_object_or_404(self.model,
                                 slug__iexact=slug)


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


class ObjectUpdateMixin(GetObjectMixin):
    form_class = None
    model = None
    template_name = ''

    def get(self, request, slug):
        obj = self.get_object(slug=slug)
        context = {
            'form': self.form_class(obj),
            self.model.__name__.lower(): obj
        }
        return render(request, self.template_name, context=context)

    def post(self, request, slug):
        obj = self.get_object(slug=slug)
        bound_form = self.form_class(request.POST, instance=obj)
        if bound_form.is_valid():
            new_obj = bound_form.save()
            return redirect(new_obj)
        else:
            context = {
                'form': bound_form,
                self.model.__name__.lower(): obj
            }
            return render(request, self.template_name, context=context)


class ObjectDeleteMixin(GetObjectMixin):
    model = None
    success_url = ''
    template_name = ''

    def get(self, request, slug):
        obj = self.get_object(slug=slug)
        context = {
            self.model.__name__.lower(): obj
        }
        return render(request, self.template_name, context=context)

    def post(self, request, slug):
        obj = self.get_object(slug=slug)
        obj.delete()
        return HttpResponseRedirect(self.success_url)
