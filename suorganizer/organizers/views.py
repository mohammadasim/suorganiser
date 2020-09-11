"""
view module for organizers app
"""
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
)
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DetailView,
    UpdateView,
    DeleteView,
    ListView,
)

from .forms import (
    TagForm,
    StartupForm,
    NewsLinkForm
)
from .mixins import (
    PageLinksMixin,
    StartupContextMixin,
    NewsLinkGetObjectMixin,
)
from .models import Tag, Startup, NewsLink


class TagList(PageLinksMixin, ListView):
    """Tag list view"""
    template_name = 'tag/tag_list.html'
    paginate_by = 5
    model = Tag


class TagDetail(DetailView):
    """Tag detail view"""
    template_name = 'tag/tag_detail.html'
    queryset = Tag.objects. \
        prefetch_related('startup_set')


class TagCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """Tag create view"""
    form_class = TagForm
    template_name = 'tag/tag_form.html'
    permission_required = 'organizers.change_tag'


class TagUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """Tag update view"""
    form_class = TagForm
    model = Tag
    template_name = 'tag/tag_form_update.html'
    permission_required = 'organizers.change_tag'


class TagDelete(DeleteView):
    """Tag delete view"""
    template_name = 'tag/tag_confirm_delete.html'
    model = Tag
    success_url = reverse_lazy('organizers_tag_list')


class StartupList(PageLinksMixin, ListView):
    """Startup list view"""
    template_name = 'startup/startup_list.html'
    paginate_by = 5
    page_kwarg = 'page'
    model = Startup


class StartupDetail(DetailView):
    """Startup detail view"""
    template_name = 'startup/startup_detail.html'
    queryset = Startup.objects. \
        prefetch_related('tags') \
        .prefetch_related('newslink_set')


class StartupCreate(CreateView):
    """Startup create view"""
    form_class = StartupForm
    template_name = 'startup/startup_form.html'


class StartupUpdate(UpdateView):
    """startup update view"""
    form_class = StartupForm
    model = Startup
    template_name = 'startup/startup_form_update.html'


class StartupDelete(DeleteView):
    """Startup delete view"""
    model = Startup
    template_name = 'startup/startup_confirm_delete.html'
    success_url = reverse_lazy('organizers_startup_list')


class NewsLinkCreate(NewsLinkGetObjectMixin,
                     StartupContextMixin,
                     CreateView):
    """Newslink create view"""
    form_class = NewsLinkForm
    template_name = 'newslink/newslink_form.html'
    # Django by default will use get_absolute_url
    # to redirect to the newly created object detail view
    # however in our case newslink doesn't have that view
    success_url = reverse_lazy('organizers_startup_list')
    model = NewsLink

    # noinspection PyAttributeOutsideInit
    def get_initial(self):
        """
        Overriding method to add startup to
        the initial.
        Initial is then passed to the form as initial parameters
        :return:
        """
        startup_slug = self.kwargs.get(
            self.startup_slug_url_kwarg
        )
        self.startup = get_object_or_404(Startup,
                                         slug__iexact=startup_slug)
        initial = {
            self.startup_context_object_name: self.startup,
        }
        initial.update(self.initial)
        return initial


class NewsLinkUpdate(
    StartupContextMixin,
    NewsLinkGetObjectMixin,
    UpdateView):
    """Newslink update view"""
    form_class = NewsLinkForm
    model = NewsLink
    template_name = 'newslink/newslink_form_update.html'
    # override the slug_url_kwarg so that the view knows to accept
    # newslink_slug instead of just slug
    slug_url_kwarg = 'newslink_slug'


class NewsLinkDelete(
    StartupContextMixin,
    NewsLinkGetObjectMixin,
    DeleteView):
    """Newslink Delete view"""
    template_name = 'newslink/newslink_confirm_delete.html'
    model = NewsLink
    slug_url_kwarg = 'newslink_slug'

    def get_success_url(self):
        """
        Redirect to the startup that the newslink was associated with,
        when the newslink is deleted.
        :return:
        """
        return (self.object.startup.
                get_absolute_url())
