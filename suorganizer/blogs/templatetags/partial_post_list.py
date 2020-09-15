"""
Module to create custom template tag
for posts.
Just as the name of the file must be
the same as the what we call load with,
the name of the function with simple_tag
decorator must be the same as the tag we
use in the template.
Inclusion tag, loads another template,
render it and then places the result
inside the template using the tag.
We create a template to use with the
inclusion tag. By convention we create
an includes direcotry in the blogs/templates/post
to store all our inclusion templates.
"""
from io import StringIO
from django import template

register = template.Library()


@register.inclusion_tag('post/includes/partial_post_list.html',
                        takes_context=True)
def format_post_list(context, detail_object):
    """
    Function that takes a python list and
    creates an unordered html list.
    The function passes the list to the
    template in the decorator.
    We get the context object and get
    the request objects from the context.
    We then check for permissions for the
    posts.
    """
    request = context.get('request')
    future_perms = request.user.has_perm(
        'blogs.view_future_post'
    )
    if future_perms:
        post_list = detail_object.blog_posts.all()
    else:
        post_list = detail_object.published_posts
    return {
        'post_list': post_list
    }
