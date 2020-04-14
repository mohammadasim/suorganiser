from django.shortcuts import render, get_object_or_404

from .models import Tag, Startup


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
