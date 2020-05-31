from django.shortcuts import (
    render,
    get_object_or_404, redirect
)
from django.views.generic import (
    View,
    CreateView,
    YearArchiveView,
    MonthArchiveView,
    ArchiveIndexView,

)

from .mixins import GetObjectMixin
from .models import Post
from .forms import PostForm


class PostList(ArchiveIndexView):
    allow_empty = True
    allow_future = True
    context_object_name = 'post_list'
    date_field = 'pub_date'
    make_object_list = True
    paginate_by = 5
    model = Post
    template_name = 'post/post_list.html'


class PostDetail(View):
    template_name = 'post/post_detail.html'

    def get(self, request, slug, year, month):
        post = get_object_or_404(Post,
                                 pub_date__year=year,
                                 pub_date__month=month,
                                 slug=slug)
        return render(request,
                      self.template_name,
                      {
                          'post': post
                      })


class PostCreate(CreateView):
    form_class = PostForm
    template_name = 'post/post_form.html'
    model = Post


class PostUpdate(GetObjectMixin, View):
    form_class = PostForm
    model = Post
    template_name = 'post/post_form_update.html'

    def get(self, request, year, month, slug):
        post = self.get_object(year, month, slug)
        context = {
            'form': self.form_class(instance=post),
            'post': post
        }
        return render(request, self.template_name, context=context)

    def post(self, request, year, month, slug):
        post = self.get_object(year, month, slug)
        bound_form = self.form_class(
            request.POST,
            instance=post
        )
        if bound_form.is_valid():
            new_post = bound_form.save()
            return redirect(new_post)
        else:
            context = {
                'form': bound_form,
                'post': post
            }
            return render(request,
                          self.template_name, context=context)


class PostDelete(GetObjectMixin, View):
    template_name = 'post/post_confirm_delete.html'
    model = Post

    def get(self, request, slug, year, month):
        post = self.get_object(year=year, month=month, slug=slug)
        context = {
            'post': post
        }
        return render(request, self.template_name, context=context)

    def post(self, request, slug, year, month):
        post = self.get_object(year, month, slug)
        post.delete()
        return redirect('blogs_post_list')


class PostArchiveYear(YearArchiveView):
    model = Post
    date_field = 'pub_date'
    template_name = 'post/post_archive_year.html'
    make_object_list = True


class PostArchiveMonth(MonthArchiveView):
    model = Post
    date_field = 'pub_date'
    template_name = 'post/post_archive_month.html'
    month_format = '%m'

