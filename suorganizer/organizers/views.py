from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import (
    Paginator,
    PageNotAnInteger,
    EmptyPage
)
from django.urls import reverse_lazy
from django.views.generic import (
    View,
    CreateView,
    DetailView,
    UpdateView,
    DeleteView,
)

from .models import Tag, Startup, NewsLink
from .mixins import (
    ObjectPaginateMixin,
)
from .forms import (
    TagForm,
    StartupForm,
    NewsLinkForm
)


class TagList(View):
    template_name = 'tag/tag_list.html'

    def get(self, request):
        return render(request,
                      self.template_name,
                      {'tag_list': Tag.objects.all()})


class TagPageList(ObjectPaginateMixin, View):
    template_name = 'tag/tag_list.html'
    reverse_url_name = 'organizers_tag_page'
    paginate_by = 5

    def get(self, request, page_number):
        prev_url = None
        next_url = None
        tags = Tag.objects.all()
        paginator = Paginator(tags,
                              self.paginate_by)
        try:
            page = paginator.page(page_number)
            prev_url = self.get_previous_url(page)
            next_url = self.get_next_url(page)

        except PageNotAnInteger:
            page = paginator.page(1)
            next_url = self.get_next_url(page)
        except EmptyPage:
            page = paginator.page(
                paginator.num_pages
            )
        context = {
            'is_paginated': page.has_next(),
            'tag_list': page,
            'paginator': paginator,
            'next_page_url': next_url,
            'previous_page_url': prev_url
        }
        return render(request,
                      self.template_name,
                      context)


class TagDetail(DetailView):
    model = Tag


class TagCreate(CreateView):
    form_class = TagForm
    template_name = 'tag/tag_form.html'


class TagUpdate(UpdateView):
    form_class = TagForm
    model = Tag
    template_name = 'tag/tag_form_update.html'


class TagDelete(DeleteView):
    template_name = 'tag/tag_confirm_delete.html'
    model = Tag
    success_url = reverse_lazy('organizers_tag_list')


class StartupList(View):
    template_name = 'startup/startup_list.html'
    paginate_by = 5
    page_kwarg = 'page'

    def get(self, request):
        startup = Startup.objects.all()
        paginator = Paginator(startup, self.paginate_by)
        page_number = request.GET.get(
            self.page_kwarg
        )
        try:
            page = paginator.page(page_number)
        except PageNotAnInteger:
            page = paginator.page(1)
        except EmptyPage:
            page = paginator.page(
                paginator.num_pages
            )

        context = {
            'is_paginated': page.has_other_pages(),
            'startup_list': page,
            'paginator': paginator
        }
        return render(request,
                      self.template_name,
                      context)


class StartupDetail(DetailView):
    model = Startup


class StartupCreate(CreateView):
    form_class = StartupForm
    template_name = 'startup/startup_form.html'


class StartupUpdate(UpdateView):
    form_class = StartupForm
    model = Startup
    template_name = 'startup/startup_form_update.html'


class StartupDelete(DeleteView):
    model = Startup
    template_name = 'startup/startup_confirm_delete.html'
    success_url = reverse_lazy('organizers_startup_list')


class NewsLinkCreate(CreateView):
    form_class = NewsLinkForm
    template_name = 'newslink/newslink_form.html'
    # Django by default will use get_absolute_url to redirect to the newly created object detail view
    # however in our case newslink doesn't have that view
    success_url = reverse_lazy('organizers_startup_list')


class NewsLinkUpdate(View):
    form_class = NewsLinkForm
    model = NewsLink
    template_name = 'newslink/newslink_form_update.html'

    def get(self, request, pk):
        news_link = get_object_or_404(self.model, pk=pk)
        context = {
            'form': self.form_class(instance=news_link),
            'newslink': news_link
        }
        return render(request,
                      self.template_name,
                      context=context)

    def post(self, request, pk):
        news_link = get_object_or_404(self.model, pk=pk)
        bound_form = self.form_class(
            request.Post,
            instance=news_link
        )
        if bound_form.is_valid():
            new_newslink = bound_form.save()
            return redirect(new_newslink)
        else:
            context = {
                'form': bound_form,
                'newslink': news_link
            }
            return render(request, self.template_name, context=context)


class NewsLinkDelete(View):
    template_name = 'newslink/newslink_confirm_delete.html'
    model = NewsLink

    def get(self, request, pk):
        news_link = get_object_or_404(self.model, pk=pk)
        context = {
            'newslink': news_link
        }
        return render(request,
                      self.template_name,
                      context=context)

    def post(self, request, pk):
        news_link = get_object_or_404(self.model, pk=pk)
        startup = news_link.startup
        news_link.delete()
        return redirect(startup)
