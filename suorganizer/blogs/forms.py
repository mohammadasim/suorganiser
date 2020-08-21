from django.contrib.auth import get_user
from django.forms import ModelForm

from .models import Post


class PostForm(ModelForm):
    class Meta:
        model = Post
        exclude = ('author',)
        fields = '__all__'

    def clean_slug(self):
        return self.cleaned_data['slug'].lower()

    def save(self, request, commit=True):
        """
        Overriding save method to contain
        http request object so we get
        the author of the blog
        :param request:
        :param commit:
        :return:
        """
        post = super().save(commit=False)
        # if post is not already saved
        # add the current user as author
        if not post.pk:
            post.author = get_user(request)
        if commit:
            post.save()
            self.save_m2m()
        return post
