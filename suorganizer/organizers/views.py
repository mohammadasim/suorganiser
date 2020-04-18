from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View

from .models import Tag, Startup
from .mixins import ObjectCreateMixin
from .forms import (
    TagForm,
    StartupForm,
    NewsLinkForm
)


def tag_list(request):
    return render(request,
                  'tag/tag_list.html',
                  {'tag_list': Tag.objects.all()})


def tag_detail(request, slug):
    tag = get_object_or_404(Tag,
                            slug__iexact=slug)
    return render(request,
                  'tag/tag_detail.html',
                  {'tag': tag})


class TagCreate(ObjectCreateMixin, View):
    form_class = TagForm
    template_name = 'tag/tag_form.html'


def startup_list(request):
    return render(request,
                  'startup/startup_list.html',
                  {
                      'startup_list': Startup.objects.all()
                  })


def startup_detail(request, slug):
    startup = get_object_or_404(Startup, slug__iexact=slug)
    return render(request,
                  'startup/startup_detail.html',
                  {
                      'startup': startup
                  })


class StartupCreate(ObjectCreateMixin, View):
    form_class = StartupForm
    template_name = 'startup/startup_form.html'


class NewsLinkCreate(ObjectCreateMixin, View):
    form_class = NewsLinkForm
    template_name = 'newslink/newslink_form_html'
