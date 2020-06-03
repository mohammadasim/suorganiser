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
)
from .models import Tag, Startup, NewsLink


class TagList(PageLinksMixin, ListView):
    template_name = 'tag/tag_list.html'
    paginate_by = 5
    model = Tag


class TagDetail(DetailView):
    model = Tag
    template_name = 'tag/tag_detail.html'


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


class StartupList(PageLinksMixin, ListView):
    template_name = 'startup/startup_list.html'
    paginate_by = 5
    page_kwarg = 'page'
    model = Startup


class StartupDetail(DetailView):
    model = Startup
    template_name = 'startup/startup_detail.html'


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


class NewsLinkUpdate(UpdateView):
    form_class = NewsLinkForm
    model = NewsLink
    template_name = 'newslink/newslink_form_update.html'


class NewsLinkDelete(DeleteView):
    template_name = 'newslink/newslink_confirm_delete.html'
    model = NewsLink

    def get_success_url(self):
        """
        Redirect to the startup that the newslink was associated with,
        when the newslink is deleted.
        :return:
        """
        return (self.object.startup.
                get_absolute_url())
