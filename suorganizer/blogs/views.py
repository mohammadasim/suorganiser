from django.shortcuts import (
    render,
    get_object_or_404
)
from django.views.generic import View
from .models import Post


class PostList(View):
    template_name = 'post/post_list.html'

    def get(self, request):
        return render(request,
                      self.template_name,
                      {
                          'post_list': Post.objects.all()
                      })


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
