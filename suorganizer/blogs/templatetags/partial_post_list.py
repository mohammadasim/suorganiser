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
from django.utils.safestring import mark_safe

register = template.Library()


@register.inclusion_tag('post/includes/partial_post_list.html',
                        takes_context=True)
def format_post_list(context, detail_object,
                     *args, **kwargs):
    """
    Function that takes a python list and
    creates an unordered html list.
    The function passes the list to the
    template in the decorator.
    We get the context object and get
    the request objects from the context.
    We then check for permissions for the
    posts.
    CSS classes to be added to the html
    are passed as arguments to the tag
    in the template and are received by
    the function here as kwargs. As these
    kwargs might not always be defined
    we therefore check if they exist and
    update the functionality accordingly.
    We use marke_safe to ensure that Django
    won't escape the string we pass.
    We use the manager method published()
    instead of the individual model methods.
    Once we get the queryset we call the values()
    method to get all the values that we need.
    It means that when the template access post_list
    there won't be any database call made.
    This speeds up the process.
    """

    opposite = kwargs.get('opposite')
    perm_button = kwargs.get('perm_button')

    request = context.get('request')
    future_perms = request.user.has_perm(
        'blogs.view_future_post'
    )
    if future_perms:
        post_list = detail_object.blog_posts.all()
    else:
        post_list = detail_object.blog_posts.published()
    if opposite is None:
        section_attr = ''
    elif opposite or perm_button:
        section_attr = mark_safe(
            'class=meta one-third column'
        )
    else:  # opposite is an empty list
        section_attr = mark_safe(
            'class="meta offset-by-two '
            'two-thirds column"'
        )
    return {
        'section_attr': section_attr,
        'post_list': post_list.values(
            'title', 'slug', 'pub_date'
        )
    }
