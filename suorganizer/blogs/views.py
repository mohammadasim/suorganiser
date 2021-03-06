"""
View file for blogs app
"""
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    CreateView,
    YearArchiveView,
    MonthArchiveView,
    ArchiveIndexView,
    DetailView,
    UpdateView,
    DeleteView,

)

from .forms import PostForm
from .mixins import DateObjectMixin, AllowFuturePermissionMixin, PostFormValidMixin
from .models import Post


class PostList(
    AllowFuturePermissionMixin,
    ArchiveIndexView):
    """List View"""
    allow_empty = True
    context_object_name = 'post_list'
    date_field = 'pub_date'
    make_object_list = True
    paginate_by = 5
    model = Post
    template_name = 'post/post_list.html'


class PostDetail(LoginRequiredMixin,DateObjectMixin, DetailView):
    """Detail view"""
    template_name = 'post/post_detail.html'
    date_field = 'pub_date'
    queryset = Post.objects. \
        select_related('author__profile') \
        .prefetch_related('startups') \
        .prefetch_related('tags')


class PostCreate(LoginRequiredMixin, PostFormValidMixin, CreateView):
    """Create view"""
    form_class = PostForm
    template_name = 'post/post_form.html'
    model = Post


class PostUpdate(LoginRequiredMixin, DateObjectMixin, PostFormValidMixin, UpdateView):
    """Update view"""
    form_class = PostForm
    date_field = 'pub_date'
    model = Post
    template_name = 'post/post_form_update.html'


class PostDelete(LoginRequiredMixin, DateObjectMixin, DeleteView):
    """Delete view"""
    template_name = 'post/post_confirm_delete.html'
    success_url = reverse_lazy('blogs_posts_list')
    model = Post
    date_field = 'pub_date'


class PostArchiveYear(AllowFuturePermissionMixin, YearArchiveView):
    """View showing posts in a given year"""
    model = Post
    date_field = 'pub_date'
    template_name = 'post/post_archive_year.html'
    make_object_list = True


class PostArchiveMonth(AllowFuturePermissionMixin, MonthArchiveView):
    """View showing posts in a given month"""
    model = Post
    date_field = 'pub_date'
    template_name = 'post/post_archive_month.html'
    month_format = '%m'
